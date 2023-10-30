import os
import json
import pandas as pd


class RequestHandler():

    def __init__(self, stores):
        self.stores = stores
        self.app_path = self.get_app_path()
        
        print("Working path:")
        print(self.app_path)

        self.df = pd.DataFrame(columns=["store", "name", "id", "unit", "imageURL", "original_link", "category", "price_changes"])

        self.store_data = {}


    def get_app_path(self):
        cwd = os.getcwd()
        if "home" in cwd:
            return "/home/SebastianChristoph/mysite/"
        else:
            return cwd
        
    def load_data2(self, stores):

        for store in stores:
            print("Loading Json for", store)
            current_dir = os.path.dirname(__file__)

            cwd = os.getcwd()
            if "home" in cwd:
                file_relative_path = os.path.join("static", "crawler", "jsons", store+".json")
            else:
                file_relative_path = os.path.join("crawler", "jsons", store+".json")
            file_path = os.path.abspath(os.path.join(current_dir, file_relative_path))

            with open(file_path, "r", encoding = "UTF-8") as file:
                content = file.read()
                store_data = json.loads(content)
            
            self.store_data[store] = store_data



    def search2(self,searchterm, search_in_which_stores, selected_stores):

        output = {}
        
        for store in self.store_data:
            found_products_store = []
            print("search in", store)
            if search_in_which_stores != "all" and store not in selected_stores:
                print("continue")
                continue
        
            for product in self.store_data[store]["products"]:
                if searchterm not in product["name"] and searchterm.lower() not in product["name"] and searchterm.upper() not in product["name"]:
                    continue
                else:
                    
                    price_changes = []

                    first_price_bulk = product["price_changes"][0]["price_bulk"]
                    
                    for i in range(0, len(product["price_changes"])):

                        if i == 0:
                            price_change = [0, 100, "down"]
                        else:
                            
                            absolute_price_difference = float(product["price_changes"][i]["price_bulk"]) - float(product["price_changes"][i-1]["price_bulk"])
                            relative_price_difference = round( 100 +(
                                ((float(product["price_changes"][i]["price_bulk"]) - float(first_price_bulk)) / float(first_price_bulk)) * 100),2)
                            
                            # Berechnung des Trends
                            trend = "up" if absolute_price_difference > 0 else ("down" if absolute_price_difference < 0 else "no_change")

                            price_change = [absolute_price_difference, relative_price_difference, trend]
                        
                        price_event = {
                            "date" : product["price_changes"][i]["date"],
                            "price_single" : product["price_changes"][i]["price_single"],
                            "price_bulk" : product["price_changes"][i]["price_bulk"],
                            "price_change" : price_change
                        }
                        price_changes.append(price_event)



                    product_dict = {
                        "name" : product["name"],
                        "id" : product["id"],
                        "imageURL" : product["imageURL"],
                        "original_link" : product["original_link"],
                        "unit" : product["unit"],
                        "category" : product["category"],
                        "price_changes" : price_changes
                    }


                    found_products_store.append(product_dict)

             # sort list
            sorted_products = sorted(found_products_store, key=lambda x: x["name"])        
            output[store] =sorted_products


        
        # with open("output.json", "w", encoding="UTF-8") as file:
        #     json.dump(output, file)

        
        return output
        
        

    def load_data(self, stores):

        for store in stores:

            current_dir = os.path.dirname(__file__)
            file_relative_path = os.path.join("crawler", "jsons", store+".json")
            file_path = os.path.abspath(os.path.join(current_dir, file_relative_path))

            with open(file_path, "r", encoding = "UTF-8") as file:
                content = file.read()
                store_data = json.loads(content)

                store_name = store_data["name"]
                products = store_data["products"]
                
                for product in products:
                    product_data = {
                        "store": store_name,
                        "name": product["name"],
                        "id": product["id"],
                        "unit": product["unit"],
                        "imageURL": product["imageURL"],
                        "original_link": product["original_link"],
                        "category": product["category"],
                        "price_changes": [pc for pc in product["price_changes"]],
                    }
                    self.df = self.df.append(product_data, ignore_index=True)


    def search(self,searchterm, search_in_which_stores, selected_stores):
        # Erstellen eines leeren Dictionaries für die Ausgabe
        output_data = {}

        # Iterieren über eindeutige Store-Namen in Ihrem DataFrame
        for store_name in self.df['store'].unique():
            
            if search_in_which_stores != "all" and store_name not in selected_stores:
                continue

            found_products =  []

            # Filtern der Zeilen, die das Wort "Milch" in 'name', 'category' oder 'id' enthalten
            filtered_rows = self.df[self.df['store'] == store_name]
            filtered_rows = filtered_rows[filtered_rows['name'].str.contains(searchterm, case=False) | filtered_rows['category'].str.contains(searchterm, case=False) | filtered_rows['id'].str.contains(searchterm, case=False)]
        
            if not filtered_rows.empty:
                for _, row in filtered_rows.iterrows():

                    product_data = {
                        "name": row['name'],
                        "id" : row["id"],
                        "imageURL": row['imageURL'],
                        "original_link": row['original_link'],
                        "category": row['category'],
                        "unit": row['unit'],
                        "price_changes": []
                    }

                    # Erstellen einer Variablen zur Verfolgung des ersten "price_change_entry"
                    first_price_change = None

                    for pc in row['price_changes']:
                        price_change_entry = {
                            "date": pc['date'],
                            "price_single": pc['price_single'],
                            "price_bulk": pc['price_bulk'],
                            "price_change": [0, 100, "down"] 
                            
                        }

                        if first_price_change is None:
                            first_price_change = pc  # Speichern des ersten "price_change_entry"
                        else:
                            # Berechnung der absoluten Preisänderung zum Vorgänger
                            absolute_price_difference = round(float(pc['price_bulk']) - float(first_price_change['price_bulk']),2)
                            # Berechnung der relativen Preisänderung zum ersten Eintrag in der Liste
                            relative_price_difference = round( 100 +(
                                ((float(pc['price_bulk']) - float(first_price_change['price_bulk'])) / float(first_price_change['price_bulk'])) * 100),
                                
                                2)
                            # Berechnung des Trends
                            trend = "up" if absolute_price_difference > 0 else ("down" if absolute_price_difference < 0 else "no_change")

                            # Aktualisieren der "price_change" mit den berechneten Werten
                            price_change_entry["price_change"] = [absolute_price_difference, relative_price_difference, trend]

                        product_data["price_changes"].append(price_change_entry)
                        
                    if product_data not in found_products:
                        found_products.append(product_data)


            output_data[store_name] = found_products
                
        # Speichern des extrahierten Daten in einem JSON-Datei
        # with open("output.json", "w") as json_file:
        #     json.dump(output_data, json_file, indent=4)
        
        return output_data

    
    def handle_request2(self, searchterm, search_in_which_stores, selected_stores):
        
        selected_products = self.combined_df[self.combined_df['product_name'].str.contains('Milch', case=False) |
                               self.combined_df['product_category'].str.contains('Milch', case=False) |
                               self.combined_df['product_id'].str.contains('Milch', case=False)]
    
        found_products_by_store = {}

        # Iterieren Sie über die ausgewählten Produkte und gruppieren Sie sie nach dem Storenamen.
        for index, row in selected_products.iterrows():
            store_name = row["store_name"]
            if store_name not in found_products_by_store:
                found_products_by_store[store_name] = {}

            product_id = row["product_id"]
            if product_id not in found_products_by_store[store_name]:
                product_info = {
                    "name": row["product_name"],
                    "id": row["product_id"],
                    "imageURL": row["product_imageURL"],
                    "original_link": row["product_original_link"],
                    "category": row["product_category"],
                    "unit": row["product_unit"],
                    "price_changes": []
                }

                # Iterieren Sie über die Preisänderungen und erstellen Sie das JSON-Format für jede Änderung.
                for price_change in row["product_price_changes"]:
                    price_change_info = {
                        "date": price_change["date"],
                        "price_single": price_change["price_single"],
                        "price_bulk": price_change["price_bulk"],
                        "price_change": float(price_change["price_single"]) - float(price_change["price_bulk"])
                    }
                    product_info["price_changes"].append(price_change_info)

                found_products_by_store[store_name][product_id] = product_info

        # Schreiben Sie die gefundenen Produkte nach Stores in eine JSON-Datei.
        with open("found_products_by_store.json", "w") as outfile:
            json.dump(found_products_by_store, outfile, indent=4)
        
        return found_products_by_store

       

    def handle_request(self, searchterm, search_in_which_stores, selected_stores):
        print(f"Search in {search_in_which_stores} stores ({selected_stores}) for {searchterm}")

        if search_in_which_stores == "all":
            found_products = self.df[self.df['name'].str.contains(searchterm, case=False) | self.df['id'].str.contains(searchterm, case=False) | self.df['category'].str.contains(searchterm, case=False)]
        else:
            #parse string
            search_string = ""
            for store in selected_stores:
                search_string+= store.upper() + "|"
            search_string = search_string[0:-1]            
       
            found_products = self.df[(self.df['store'].str.contains(search_string, case=False)) & (self.df['name'].str.contains(searchterm, case=False) | self.df['id'].str.contains(searchterm, case=False) | self.df['category'].str.contains(searchterm, case=False))]

        for col in found_products.columns:
            found_products[col] = found_products[col].combine_first(found_products.iloc[1::2][col])

       
        
        # found_products = found_products.dropna(subset=['date'])
        # print(found_products)


        grouped = found_products.groupby(['store', 'name'])
        result = {}
     
        # Iterieren durch die gruppierten Daten
        for (store, name), group in grouped:

            # print("store:")
            # print(store)
            # print("name:")
            # print(name)
            
            # # Übernehme die Informationen aus der vorherigen Zeile der Gruppe, wenn sie NaN sind
            
            # print("original_link:")
            # print(original_link)

            # Weitere Informationen wie "unit" und "imageURL" können auf die gleiche Weise behandelt werden
            original_link = group['original_link'].fillna(method='bfill').iloc[0]
            unit = group['unit'].fillna(method='bfill').iloc[0]
            imageURL = group['imageURL'].fillna(method='bfill').iloc[0]

            # Erstelle ein Dictionary-Eintrags für jedes Produkt
            product_data = {
                "name": name,
                "original_link": original_link,
                "imageURL": imageURL,
                "unit": unit,
                "price_changes": {}
            }

            # Sortieren der Gruppendaten nach 'date', um die Reihenfolge sicherzustellen
            group = group.sort_values(by='date')
 # Iterieren durch die Preisänderungen für dieses Produkt
            first_bulk_price = None
            prev_bulk_price = None
            # Iterieren durch die Preisänderungen für dieses Produkt
            for index, row in group.iterrows():
                date = row['date']
                price_single = row['price_single']
                price_bulk = row['price_bulk']
                
                # Erstellen eines Eintrags für die Preisänderung an diesem Datum
                if first_bulk_price is not None:
                    rel_price_change = round(( float(price_bulk) / float(first_bulk_price)) * 100, 2)
                else:
                    rel_price_change = 100
                
                # Berechnen des Trendwerts (up oder down)
                if prev_bulk_price is not None:
                    trend = "up" if float(price_bulk) > float(prev_bulk_price) else "down"
                else:
                    trend = "down"
                
                price_entry = [price_single, price_bulk, rel_price_change, trend]
                
                # Hinzufügen der Preisänderung zum Produkt-Dict (wenn Datum nicht NaN ist)
                if not pd.isna(date):
                    product_data['price_changes'][date] = price_entry
                
                if first_bulk_price is None:
                    first_bulk_price = price_bulk
                  
                prev_bulk_price = price_bulk
                
            
            # Überprüfen, ob der Store bereits im Ergebnis-Dict existiert
            if store in result:
                result[store].append(product_data)
            else:
                result[store] = [product_data]



        return result
    