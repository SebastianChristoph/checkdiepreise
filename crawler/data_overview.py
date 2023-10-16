import os
import re
import json
from datetime import datetime, timedelta
cwd = os.getcwd()

SHOW_PRINT = True

info_dict = {
    "stores" : [],
    "products_total"  : 0,
    "max_down_product": {},
    "max_up_product" : {}
    }

stores = ["Mueller", "Rossmann", "Hellweg", "Netto", "Kaufland"]
#stores = ["Testing"]

print(cwd)
def get_current_date():
    today = datetime.now()
    return today.strftime("%d-%m-%Y")

def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%d-%m-%Y")

def filter_numerical_with_regex(input_string):
    # Verwende einen regulären Ausdruck, um alle Zeichen außer Zahlen und Punkt zu entfernen
    filtered_string = re.sub(r'[^0-9.]', '', input_string)
    
    return filtered_string

today = get_current_date()
yesterday = get_yesterday_date()

max_up_price_change_percent = 0.0
max_up_price_change_product = {}

max_down_price_change_percent = 0.0
max_down_price_change_product = {}


products_total = 0

for store in stores:
    store_dict_to_merge = {
        "store_name" : store,
        "products_store_total" : 0,
        "changes_to_yesterday" : []
        # {product_name :  , price_yesterday : , price_today : , price_change, "direction"}
    }


    print("##############################################################")
    print("Analyzing:", store.upper())
    path_to_store_json = ""
    store_dict= {}
    if "home" in cwd:
        #flask path
        print("RUNNING IN FLASK")
        path_to_info_json = "/home/SebastianChristoph/mysite/static/crawler/info.json"
        path_to_store_json = "/home/SebastianChristoph/mysite/static/crawler/" + store.upper() + ".json"
    else:
        # local path
        print("RUNNING LOCALLY")

        if(store == "Testing"):
            path_to_store_json = "testingoutput.json"
            path_to_info_json = "crawler/info.json"
        else:
            path_to_store_json = "crawler/" + store.upper() + ".json"
            path_to_info_json = "crawler/info.json"
    
    print("Load JSON into Dict", end = "")
    with open(path_to_store_json, encoding="utf-8") as json_file:
        store_dict = json.load(json_file)
    print("...Done")

    ### CHANGES TO YESTERDAY
    print("*** PRICE CHANGES ******")

    for product in store_dict["products"]:
        products_total += 1
        if product["dates"].get(yesterday) != None and product["dates"].get(today) != None:
            try:

                price_today = filter_numerical_with_regex(product["dates"][today])
                price_yesterday = filter_numerical_with_regex(product["dates"][yesterday])

                price_today = float(price_today)
                price_yesterday = float(price_yesterday)
                imageURL = product["image"]
                category = product["category"]

                price_change = round(price_today - price_yesterday, 2)

                if price_today != 0 and price_yesterday != 0:
                    if price_change != 0:
                        direction = "u"

                        if SHOW_PRINT:
                            print("+ ", product["name"], end = "")
                        
                        if price_change > 0:
                            direction = "up"
                            
                        else:
                            direction = "down"

                        
                        price_percentage = round(price_change / price_yesterday * 100, 2)

                        #price_percentage =   price_change / price_yesterday * 100
                        print("Percent:", price_percentage, "%", end = "")
                        
                        if SHOW_PRINT:
                            print(" >> ", direction, price_change, "€ [",price_yesterday, " >", price_today, "]")
                        # {product_name :  , price_yesterday : , price_today : , price_change, direction, original_link}
                        
                        product_changes = {
                            "product_name": product["name"],
                            "price_yesterday" : price_yesterday,
                            "price_today" : price_today,
                            "price_change" : price_change,
                            "price_change_percentage" : price_percentage,
                            "direction" : direction,
                            "original_link" :  product["original_link"],
                            "category" : category,
                            "imageURL" : imageURL,
                            "store" : store
                        }

                        if price_percentage < 90:
                            if price_percentage > max_up_price_change_percent:
                                max_up_price_change_percent = price_percentage
                                max_up_price_change_product = product_changes
                        
                        if price_percentage > -90:
                            if price_percentage < max_down_price_change_percent:
                                max_down_price_change_percent = price_percentage
                                max_down_price_change_product = product_changes

                        store_dict_to_merge["changes_to_yesterday"].append(product_changes)
                else:
                    continue
            except Exception as e:
                print(" not working", price_today, price_yesterday, e)
                continue



    info_dict["stores"].append(store_dict_to_merge)
    


    ### AMOUNT PRODUCTS IN JSON
    products_in_json = len(store_dict["products"])
    store_dict_to_merge["products_store_total"] = products_in_json
info_dict["products_total"] = products_total
info_dict["updated"] = get_current_date()
info_dict["max_down_product"] = max_down_price_change_product
info_dict["max_up_product"] = max_up_price_change_product

with open(path_to_info_json, "w") as outfile: 
    json.dump(info_dict, outfile)

print("Saved in info.json")
