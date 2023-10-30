
import mapper
import json
from datetime import datetime, timedelta
import os
import re
import time

class CrawlerHandler:
    def __init__(self, store, mapping_cat = mapper.mapping, with_id = False, show_prints =False):
        self.STORE_JSON = {}
        self.STORE_JSON_CURRENT_PRODUCTS = []
        self.STORE_JSON_CURRENT_IDS = []
        self.NEW_ADDED_IDS = []
        self.with_id = with_id
        self.show_prints = show_prints
        self.store = store
        self.updated = 0
        self.new = 0
        self.added_ids = 0
        self.max_length = 0
        self.mapping_cat = mapping_cat
        self.path_to_store_json = ""
        self.mapper_categories = {
            "drogerie" : mapper.mapping_drogerie,
            "baumarkt" : mapper.mapping_baumarkt,
            "biocompany" : mapper.mapping_biocompany,
            "rewe" : mapper.mapping_rewe,
            "ikea" : mapper.mapping_ikea,
            "superstore" : mapper.mapping_superstore,
            "kaufland_api" : mapper.mapping_kaufland_api,
            "dm" : mapper.mapping_dm,
            "mueller_api" : mapper.mapping_mueller_api,
            "aldisued" : mapper.mapping_aldisued,
            "fressnapf_api" : mapper.mapping_fressnapf_api,
            "babywalz_api" : mapper.mapping_babywalz_api,
            "dummy_store_type" : mapper.dummy_store_type
        }
        self.path_to_log = ""

        if self.show_prints:
            print("\n\n")
            print("##############################################")
            print("######## START ###############################")
            print("##############################################")

        try:
            self.mapping = self.mapper_categories[self.mapping_cat]
        except:
            if self.show_prints:
                print("Found no special mapping, use default mapping")
            self.mapping = mapper.mapping

        self.PRODUCTS_TO_CHECK = list(self.mapping.keys())

        # quick and dirty solution for different paths in Flask / local
        cwd = os.getcwd()
        if self.show_prints:
            print(cwd)
        if "home" in cwd:
            #flask path
            if self.show_prints:
                print("RUNNING IN FLASK")
            self.path_to_store_json = "/home/SebastianChristoph/mysite/static/crawler/jsons/" + self.store + ".json"
            self.path_to_log = "/home/SebastianChristoph/mysite/static/crawler/logging/dailylog.txt"
        else:
            # local path
            if self.show_prints:
                print("RUNNING LOCALLY")
            self.path_to_store_json = "crawler/jsons/" + self.store + ".json"
            self.path_to_log = "crawler/logging/dailylog.txt"

        #method calls
        self.current_date = self.get_current_date()
        self.getting_store_json()
        #self.add_current_date_to_json()
        #self.clear_webshop_links_for_all_products()
        self.get_all_products_form_JSON()

    def print_message(self, message):
        done_position = 70
        message_length = len(message)
        padding = done_position - message_length
        dots = '.' * padding
        if self.show_prints:
            print(message + dots, end = "")

    def getting_store_json(self):
        self.print_message("Getting Store JSON for " + self.store)
        with open(self.path_to_store_json, encoding="utf-8") as json_file:
            self.STORE_JSON = json.load(json_file)
        if self.show_prints:
            print("Done")

    def get_current_time(self):
        current_time = datetime.now()
        current_time_format = current_time.strftime("%d-%m  %H:%M")
        return current_time_format

    def get_current_date(self):
        self.t0 = time.time()
        today = datetime.now()
        return today.strftime("%d-%m-%Y")

    def get_yesterday_date(self):
        yesterday = datetime.now() - timedelta(days=1)
        return yesterday.strftime("%d-%m-%Y")

    def add_current_date_to_json(self):
        self.print_message("Adding current date to STORE_JSON")
        for product in self.STORE_JSON["products"]:
            if product["dates"].get(self.current_date) != None :
                pass
            else:
               product["dates"][self.current_date] = "0"
        if self.show_prints:
            print("Done")
        self.print_message("Adding current date to STORE_JSON historical labels")
        if self.current_date not in self.STORE_JSON["historical_labels"]:
            self.STORE_JSON["historical_labels"].append(self.current_date)

        if self.show_prints:
            print("Done")

    def clear_webshop_links_for_all_products(self):
        if self.show_prints:
            self.print_message("Clear WebShop-Link for all " + str(len(self.STORE_JSON["products"]))+ " products ...")

        for product in self.STORE_JSON["products"]:
            product["original_link"] = "#"
        if self.show_prints:
            print("Done")

    def get_all_products_form_JSON(self):
        error_loading_ids = 0
        if self.with_id:
            if self.show_prints:
                self.print_message("Getting IDs from STORE_JSON...")
            for product in self.STORE_JSON["products"]:
                if product.get("id") != None:
                    self.STORE_JSON_CURRENT_IDS.append(product["id"])
                    self.added_ids += 1
                else:
                    error_loading_ids += 1

            if self.show_prints:
                print("Done")
                print("   Already", len(self.STORE_JSON_CURRENT_IDS), "IDs in json, errors in loading ids:", error_loading_ids)

            # HANDLE PRODUCT NAMES
        else:
            self.print_message("Getting products from STORE_JSON...")
            for product in self.STORE_JSON["products"]:
                self.STORE_JSON_CURRENT_PRODUCTS.append(product["name"])
            if self.show_prints:
                print("Done")

    def is_product_already_in_json(self, product):
        return product in self.STORE_JSON_CURRENT_PRODUCTS

    def is_product_id_already_in_json(self, product_id):
        return product_id in self.STORE_JSON_CURRENT_IDS

    def is_product_already_in_dict(self, product):
        return product in self.STORE_JSON["products"]

    def get_file_size(self, path):
        file_size_in_bytes = os.path.getsize(path)
        file_size_in_mb = file_size_in_bytes / (1024 * 1024)
        return file_size_in_mb

    def save_data(self):
        self.print_message("Save data to " + self.store + ".json ...")
        if self.store == "Testing":
            with open("testingoutput.json", 'w', encoding="utf-8") as textfile:
                json.dump(self.STORE_JSON, textfile)
        else:
            with open(self.path_to_store_json, 'w', encoding="utf-8") as textfile:
                json.dump(self.STORE_JSON, textfile)

        if self.show_prints:
            print("Done")

    def clean_price_text(self, price_text):
        try:

            cleaned_price = str(price_text)
            cleaned_price = cleaned_price.replace(",",".")

            if "=" in cleaned_price:
                cleaned_price = cleaned_price.split("=")[-1]

            match = re.search(r'\d+(\.\d*)?', cleaned_price)

            if match:
                cleaned_price = match.group()
                cleaned_price = float(cleaned_price)
                cleaned_price = round(cleaned_price, 2)
                cleaned_price = format(cleaned_price, '.2f')
                if(cleaned_price[-1] == "."):
                    cleaned_price = cleaned_price[:-1]
              
                return cleaned_price
            else:
                print("No cleaning possible for:", price_text)
                self.not_cleaned_prices += 1
                return "0"

        except Exception as e:
            if self.show_prints:
                print("ERROR IN CLEANING")
                print(e)
                print("PRICE IN:", price_text, " / PRICE IN TYPE:", type(price_text))
                print("----------------")
            return "0"

    def get_historical_labels(self):
        return self.STORE_JSON["historical_labels"]

    def handle_historical_labels(self, product):

        historical_labels = self.get_historical_labels()
        for historical_date in historical_labels:
            if product["dates"].get(historical_date) == None:
                product["dates"][historical_date] = "0"
            product["dates"] = dict(sorted(product["dates"].items(), key=lambda x: x[0]))
    
    def clean_name(self, name):

        forbidden_characters = ["%", "|", '"', "&", "\\", "/", "#"]

        for char in forbidden_characters:
            name = name.replace(char, "")
        
        return name

    def clean_unit_text(self,unittext):
        return unittext.upper()

    def clean_data(self):
        if self.show_prints:
            self.print_message("Cleaning up")

        for product in self.STORE_JSON["products"]:
            # self.handle_historical_labels(product)
            for price_change in product["price_changes"]:
                price_change["price_single"]= self.clean_price_text( price_change["price_single"])
                price_change["price_bulk"]= self.clean_price_text( price_change["price_bulk"])
                product["unit"] = self.clean_unit_text(product["unit"])
                product["name"] = self.clean_name(product["name"])

        if self.show_prints:
            print("Done")

    def handle(self, found_products, product_to_find):
        for found_product in found_products:
            if(self.is_product_already_in_json(found_product["name"])):

                # product already in JSON
                # find it in JSON
                for entry in self.STORE_JSON["products"]:
                    if entry["name"] == found_product["name"]:
                        entry["dates"][self.current_date] = found_product["price"]
                        entry["original_link"] = found_product["original_link"]
                        self.updated += 1
                        break
            else:
                new_product = {
                    "name": found_product["name"],
                    "category" : self.mapping[product_to_find],
                    "image" : found_product["imageURL"],
                    "dates" : {
                        self.current_date :  found_product["price"]
                            },
                    "found_by_keyword" : product_to_find,
                    "original_link" : found_product["original_link"]
                }

                self.STORE_JSON["products"].append(new_product)
                self.new += 1

    def handle_with_id(self, found_products, product_to_find = "no data"):
        
        for found_product in found_products:

            if found_product.get("category") != None:
                cat = found_product["category"]
            else:
                cat = self.mapping[product_to_find]

            name = self.clean_name(found_product["name"])

            if found_product["id"] in self.NEW_ADDED_IDS:
                continue

            if(self.is_product_id_already_in_json(found_product["id"])):
                # ID already in JSON ; find ID in JSON
                for product_in_json in self.STORE_JSON["products"]:
                    if product_in_json["id"] == found_product["id"]:

                        # update image

                        product_in_json["imageURL"] = found_product["imageURL"]
                        
                        #HAT BEREITS eINTRAG VON HEUTE?

                        if product_in_json["price_changes"][-1]["date"] == self.get_current_date():
                            continue
                        
                        # get last price-change
                        last_price_bulk = product_in_json["price_changes"][-1]["price_bulk"]

                        # new price change
                        if self.clean_price_text(found_product["baseprice"]) != last_price_bulk:
                            print(found_product["baseprice"], last_price_bulk)

                            new_price_change = {
                                "date" : self.get_current_date(),
                                "price_single" : self.clean_price_text(found_product["price"]),
                                "price_bulk" : self.clean_price_text(found_product["baseprice"])
                            }

                            product_in_json["price_changes"].append(new_price_change)

                            self.updated += 1
                            self.NEW_ADDED_IDS.append(product_in_json["id"])
                            break

                        # entry["dates"][self.current_date] = found_product["price"]
                        # entry["original_link"] = found_product["original_link"]
                        # entry["category"] = cat
                        # self.updated += 1
                        # self.NEW_ADDED_IDS.append(entry["id"])
                        # break
            else:
                new_product = {
                    "id" : found_product["id"],
                    "name": name,
                    "category" : cat,
                    "unit" : found_product["unit"],
                    "imageURL" : found_product["imageURL"],
                    "price_changes" : [
                            { 
                                "date" :  self.get_current_date(),
                                "price_single" : found_product["price"],
                                "price_bulk" : found_product["baseprice"]
                            }
                        ],
                    "original_link" : found_product["original_link"]
                }
 
               

                if not self.is_product_already_in_dict(new_product) and new_product["id"] not in self.NEW_ADDED_IDS:
                    self.NEW_ADDED_IDS.append(new_product["id"])
                    self.STORE_JSON["products"].append(new_product)
                    self.STORE_JSON_CURRENT_IDS.append(new_product["id"])
                    self.new += 1

    def savelog(self, took_time, not_touched):
        if self.show_prints:
            self.print_message("Saving log")
        filesize = self.get_file_size(self.path_to_store_json)
    
        current_time = self.get_current_time()

        with open(self.path_to_log, "a", encoding="UTF-8") as file:
            file.write("\n-----------------------------------------------------")
            file.write("\n" + self.store+ "(finished at " + str(current_time)+", took " + str(took_time)+ " )\n")
            file.write("Size STORE JSON:" + str(filesize) + "MB\n")
            file.write("Products in JSON: " + str(len(self.STORE_JSON["products"]))+"\n")
            file.write("Updated " +  str(self.updated) + " products.\n")
            file.write("Added " + str(self.new) + " product to JSON.\n")
            file.write("No new data for " + str(not_touched)+ " products in JSON")
           
        print("Done")
    
    def save_error_log(self):
        self.print_message("Saving error log")
        
        with open(self.path_to_log, "a", encoding="UTF-8") as file:
            file.write("\n-----------------------------------------------------")
            file.write("\n" + self.store+ " ABORTED WITH ERROR\n")
        if self.show_prints:
            print("Done")

    def give_infos(self):
        self.t1 = time.time()
        total_seconds = self.t1-self.t0
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        formatted_time = f"{minutes}min, {seconds}s"
        not_touched_products = len(self.STORE_JSON["products"]) - self.updated - self.new

        print("\n****************")
        print("FINISHED", self.store, "in", formatted_time , "seconds")
        print("* Products in JSON:", len(self.STORE_JSON["products"]))
        print("     - Updated", self.updated, "products.")
        print("     - Added", self.new, "product to JSON.")
        print("     - no new data for", not_touched_products, "products in JSON.")
  

        file_size_in_bytes = os.path.getsize(self.path_to_store_json)
        file_size_in_mb = file_size_in_bytes / (1024 * 1024)
        print("Size of STORE_JSON:", round(file_size_in_mb,2), "MB")

        self.savelog(formatted_time, not_touched_products)
        print("\n\n")