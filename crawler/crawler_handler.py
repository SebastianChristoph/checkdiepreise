
import mapper
import json
from datetime import datetime, timedelta
import os
import re
import time

class CrawlerHandler:
    def __init__(self, store, mapping_cat = mapper.mapping):
        self.showPrints = False
        self.STORE_JSON = {}
        self.STORE_JSON_CURRENT_PRODUCTS = []
        self.store = store
        self.updated = 0
        self.new = 0
        self.max_length = 0
        self.mapping_cat = mapping_cat
        self.path_to_store_json = ""
        self.mapper_categories = {
            "drogerie" : mapper.mapping_drogerie,
            "baumarkt" : mapper.mapping_baumarkt
        }
        self.not_cleaned_prices = 0

        print("\n\n")
        print("##############################################")
        print("######## START ###############################")
        print("##############################################")
    
        try:
            self.mapping = self.mapper_categories[self.mapping_cat]
        except:
            print("Found no special mapping, use default mapping")
            self.mapping = mapper.mapping

        self.PRODUCTS_TO_CHECK = list(self.mapping.keys())

        # quick and dirty solution for different paths in Flask / local
        cwd = os.getcwd()
        if self.showPrints:
            print(cwd)
        if "home" in cwd:
            #flask path
            print("RUNNING IN FLASK")
            self.path_to_store_json = "/home/SebastianChristoph/mysite/static/crawler/" + self.store.upper() + ".json"
        else:
            # local path
            print("RUNNING LOCALLY")
            self.path_to_store_json = "crawler/" + self.store.upper() + ".json"

        #method calls
        self.current_date = self.get_current_date()
        self.getting_store_json()
        self.add_current_date_to_json()
        self.clear_webshop_links_for_all_products()
        self.get_all_products_form_JSON()
    
    def print_message(self, message):
        done_position = 70
        message_length = len(message)
        padding = done_position - message_length
        dots = '.' * padding
        print(message + dots, end = "")

    def getting_store_json(self):
        self.print_message("Getting Store JSON for " + self.store.upper())
        with open(self.path_to_store_json, encoding="utf-8") as json_file:
            self.STORE_JSON = json.load(json_file)
        print("Done")

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
        print("Done")
        self.print_message("Adding current date to STORE_JSON historical labels")
        self.STORE_JSON["historical_labels"].append(self.current_date)
        print("Done")
    
    def clear_webshop_links_for_all_products(self):
        self.print_message("Clear WebShop-Link for all " + str(len(self.STORE_JSON["products"]))+ " products ...")

        for product in self.STORE_JSON["products"]:
            product["original_link"] = "#"
        print("Done")

    def get_all_products_form_JSON(self):
        self.print_message("Getting products from STORE_JSON...")
        for product in self.STORE_JSON["products"]:
            self.STORE_JSON_CURRENT_PRODUCTS.append(product["name"])
        print("Done")

    def is_product_already_in_json(self, product):
        return product in self.STORE_JSON_CURRENT_PRODUCTS
    
    def save_data(self):
        self.print_message("Save data to " + self.store.upper() + ".json ...")
        if self.store == "Testing":
            with open("testingoutput.json", 'w', encoding="utf-8") as textfile:
                json.dump(self.STORE_JSON, textfile)
        else:
            with open(self.path_to_store_json, 'w', encoding="utf-8") as textfile:
                json.dump(self.STORE_JSON, textfile)
        
        print("Done")
  
    def clean_price_text(self, price_text):
        try:
            if(self.showPrints):
                print("IN", price_text, end = "")
            cleaned_price = str(price_text)
            cleaned_price = cleaned_price.replace(",",".")

            if "=" in cleaned_price:
                cleaned_price = cleaned_price.split("=")[-1]

            match = re.search(r'\d+(\.\d*)?', cleaned_price)

            if match: 
                cleaned_price = match.group()
                if(cleaned_price[-1] == "."):
                    cleaned_price = cleaned_price[:-1]
                if(self.showPrints):
                    print(" > OUT:", cleaned_price, end = "; ")
                return cleaned_price
            else:
                print("No cleaning possible for:", price_text)
                self.not_cleaned_prices += 1
                return "0"
            
        except Exception as e:
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
          
    def clean_data(self):
        self.print_message("Cleaning up")

        for product in self.STORE_JSON["products"]:
            self.handle_historical_labels(product)
            for date in product["dates"]:
                product["dates"][date]= self.clean_price_text(product["dates"][date])
            
        if(self.showPrints):
            print("\n*************************************************")
            print("SELF.STORE_JSON:")
            for product in self.STORE_JSON["products"]:
                print(product["name"])

                for date in product["dates"]:
                    print("    +", date, ":", product["dates"][date])
                print("*************************")

                if(self.showPrints):
                    print(self.STORE_JSON["historical_labels"])
        
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
        print("     - Not touched products:", not_touched_products)
        print("     - Added", self.new, "product to JSON.")
        print("     - Not cleaned prices (price set to 0):", self.not_cleaned_prices)
        print("\n\n")
    
    
    