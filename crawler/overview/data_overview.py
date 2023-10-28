import os
import re
import json

from datetime import datetime, timedelta
cwd = os.getcwd()

SHOW_PRINT = False

info_dict = {
    "stores" : [],
    "products_total"  : 0,
    "max_down_product": {},
    "max_up_product" : {}
    }

stores = ["REWE", "Kaufland", "AldiSued","dm", "Hellweg", "Globus", "IKEA", "Netto", "Fressnapf", "BabyWalz"]
#stores = ["Testing"]

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

def format_string(input):
    # 2.9 > 2.90, 2. > 2.00
    input_string = str(input)
    if '.' in input_string:
        parts = input_string.split('.')

        if len(parts[1]) == 0:
            formatted_string = f"{parts[0]}.00"
    
        elif len(parts[1]) == 1:
            formatted_string = f"{parts[0]}.{parts[1]}0"
     
        elif len(parts[1]) == 2:
            formatted_string = input_string
    
        else:
            formatted_string = f"{parts[0]}.{parts[1][:2]}"
    else:
    
        formatted_string = f"{input_string}.00"
    
    return formatted_string

def get_path_for_file(filename, directory):
    # Pfad zur aktuellen Datei (test.py)
    current_dir = os.path.dirname(__file__)

    # Pfad zur JSON-Datei relativ zur aktuellen Datei
    file_relative_path = os.path.join('..', directory, filename)

    # Den absoluten Pfad zur JSON-Datei erstellen
    file_path = os.path.abspath(os.path.join(current_dir, file_relative_path))

    return file_path

def get_path_info():
    json_relative_path = 'info.json'
    # Den absoluten Pfad zur JSON-Datei erstellen
    json_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), json_relative_path))
    return json_file_path


def do_stuff():
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
        }

        print("##############################################################")
        print("Analyzing:", store.upper())
        path_to_store_json = ""
        store_dict= {}
        path_to_store_json = get_path_for_file(store.upper()+".json", 'jsons')
        path_to_info_json = get_path_info()
   
        print("Load JSON into Dict", end = "")
        with open(path_to_store_json, encoding="utf-8") as json_file:
            store_dict = json.load(json_file)
        print("...Done")

        ### CHANGES TO YESTERDAY
        if SHOW_PRINT:
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
                            if SHOW_PRINT:
                                print("Percent:", price_percentage, "%", end = "")
                            
                            if SHOW_PRINT:
                                print(" >> ", direction, price_change, "€ [",price_yesterday, " >", price_today, "]")
                            # {product_name :  , price_yesterday : , price_today : , price_change, direction, original_link}
                            
                            product_changes = {
                                "id" : product["id"],
                                "unit" : product["unit"],
                                "product_name": product["name"],
                                "price_yesterday" : format_string(price_yesterday),
                                "price_today" : format_string(price_today),
                                "price_change" : format_string(price_change),
                                "price_change_percentage" : format_string(price_percentage),
                                "direction" : direction,
                                "original_link" :  product["original_link"],
                                "category" : category,
                                "imageURL" : imageURL,
                                "store" : store
                            }

                        
                            if price_percentage > max_up_price_change_percent:
                                max_up_price_change_percent = price_percentage
                                max_up_price_change_product = product_changes
                        
                        
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

    print("________________________________________")
    print("Saved everything in info.json")

def saving_logs_for_today():

    path_to_log = get_path_for_file('dailylog.txt', 'logging')
    path_to_weblog= get_path_for_file('log.txt', 'logging')

    # 1. Öffnen der Quelldatei im Lesemodus
    with open(path_to_log, "r") as quelle:
        # 2. Lese den Inhalt der Quelldatei
        inhalt = quelle.read()

    # Leeren
    with open(path_to_log, "w") as quelle:
        pass


    # 3. Öffnen der Zieldatei im Schreibmodus
    with open(path_to_weblog, "w") as ziel:
        # 4. Schreibe den gelesenen Inhalt in die Zieldatei
        ziel.write(inhalt)


    print("Dailylog cleaned, saved everything in weblog")

do_stuff()
saving_logs_for_today()