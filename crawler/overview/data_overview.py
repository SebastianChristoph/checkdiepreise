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

stores = ["Aldi Süd", "Baby Walz", "dm", "Hellweg", "Ikea", "Rewe"]
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

def add_thousands_separator(number):
    # Verwende die Funktion format, um das 1000er Trennzeichen hinzuzufügen
    formatted_number = '{:,}'.format(number).replace(',', '.')
    # Gib das formatierte Ergebnis als String zurück
    return formatted_number

def do_stuff():
    global stores
    today = get_current_date()
    yesterday = get_yesterday_date()

    max_up_price_single_change_percent = 0.0
    max_up_price_bulk_change_percent = 0.0
    max_up_price_change_product = {}

    max_down_price_single_change_percent = 0.0
    max_down_price_bulk_change_percent = 0.0
    max_down_price_change_product = {}

    products_total = 0

    for store in stores:
        store_dict_to_merge = {
            "store_name" : store,
            "products_store_total" : 0,
            "changes_to_yesterday" : []
        }

        print("##############################################################")
        print("Analyzing:", store)
        store_dict= {}
        path_to_store_json = get_path_for_file(store+".json", 'jsons')
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

            # Es gibt einen EIntag für heute, also einen Price-Change
            if product["price_changes"][-1]["date"] == today and len(product["price_changes"]) > 1:

                try:

                    price_single_today = float(filter_numerical_with_regex(product["price_changes"][-1]["price_single"]))
                    price_bulk_today = float(filter_numerical_with_regex(product["price_changes"][-1]["price_bulk"]))

                    price_single_before = float(filter_numerical_with_regex(product["price_changes"][-2]["price_single"]))
                    price_bulk_before = float(filter_numerical_with_regex(product["price_changes"][-2]["price_bulk"]))

                    imageURL = product["imageURL"]
                    category = product["category"]

                    price_single_change = round(price_single_today - price_single_before, 2)
                    price_bulk_change = round(price_bulk_today - price_bulk_before, 2)

                    if price_bulk_today != 0 and price_bulk_before != 0:
                        if price_bulk_change != 0:
                           
                            if SHOW_PRINT:
                                print("+ ", product["name"], end = "")
                            
                            if price_bulk_change > 0:
                                direction = "up"
                                
                            else:
                                direction = "down"

                            
                            price_change_bulk_percentage = round(price_bulk_change / price_bulk_before * 100, 2)

                            #price_percentage =   price_change / price_yesterday * 100
                            if SHOW_PRINT:
                                print("Percent:", price_change_bulk_percentage, "%", end = "")
                            
                            if SHOW_PRINT:
                                print(" >> ", direction, price_bulk_change, "€ [",price_bulk_before, " >", price_bulk_today, "]")
                            # {product_name :  , price_yesterday : , price_today : , price_change, direction, original_link}
                            
                            product_changes = {
                                "id" : product["id"],
                                "unit" : product["unit"],
                                "product_name": product["name"],
                                "price_yesterday" : format_string(price_bulk_before),
                                "price_today" : format_string(price_bulk_today),
                                "price_change" : format_string(price_bulk_change),
                                "price_change_percentage" : format_string(price_change_bulk_percentage),
                                "direction" : direction,
                                "original_link" :  product["original_link"],
                                "category" : category,
                                "imageURL" : imageURL,
                                "store" : store
                            }

                        
                            if price_change_bulk_percentage > max_up_price_bulk_change_percent:
                                max_up_price_bulk_change_percent = price_change_bulk_percentage
                                max_up_price_change_product = product_changes
                        
                        
                            if price_change_bulk_percentage < max_down_price_bulk_change_percent:
                                max_down_price_bulk_change_percent = price_change_bulk_percentage
                                max_down_price_change_product = product_changes

                            store_dict_to_merge["changes_to_yesterday"].append(product_changes)
                    else:
                        continue
                except Exception as e:
                    print(" not working", price_bulk_today, price_bulk_before, e)
                    continue

        info_dict["stores"].append(store_dict_to_merge)
        
        ### AMOUNT PRODUCTS IN JSON
        products_in_json = len(store_dict["products"])
        store_dict_to_merge["products_store_total"] = add_thousands_separator(products_in_json)


    info_dict["products_total"] = add_thousands_separator(products_total)
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

def add_historical_label():

    if "home" in cwd:
            historical_dates_json = "/home/SebastianChristoph/mysite/static/crawler/jsons/dates.json"
    else:
        historical_dates_json = os.path.join(cwd, "crawler\\jsons", "dates.json")
    
    with open(historical_dates_json, "r", encoding="utf-8") as file:
        content = file.read()
        historical_dates = json.loads(content)

    current_date = get_current_date()

    if current_date not in historical_dates["dates"]:
        historical_dates["dates"].append(current_date)


    with open(historical_dates_json, "w", encoding="utf-8") as file:
        json.dump(historical_dates, file)





do_stuff()
saving_logs_for_today()
add_historical_label()