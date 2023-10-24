
import os
import sys
import json
import found_products_collection
from datetime import datetime, timedelta
import re

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from crawler_handler import CrawlerHandler

store_dict = {}
fails = 0
tests = 0
CrawlerHandlerTest = None

def get_current_date():
        today = datetime.now()
        return today.strftime("%d-%m-%Y")

def get_path_for_file(filename, directory):
    # Pfad zur aktuellen Datei (test.py)
    current_dir = os.path.dirname(__file__)

    # Pfad zur JSON-Datei relativ zur aktuellen Datei
    file_relative_path = os.path.join('..', directory, filename)

    # Den absoluten Pfad zur JSON-Datei erstellen
    file_path = os.path.abspath(os.path.join(current_dir, file_relative_path))

    return file_path

def is_numeric(value):
    numeric_pattern = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
    return bool(numeric_pattern.match(str(value)))

def assert_all(assertions):
    global fails, tests
    success = True
    error_messages = []

    for assertion, message in assertions:
        tests += 1
        try:
            assert assertion, message
        except AssertionError:
            fails += 1
            success = False
            error_messages.append("⇨ " +message)

    if success:
        return "\n      🥦 All assertions passed"
    else:
        return "\n      🍎 Assertions failed:\n        " + "\n          ".join(error_messages)

def setup():
    global store_dict, CrawlerHandlerTest
  
    path_to_dummy_json = get_path_for_file("DUMMYSTORE.json", "jsons")
    print("SETUP")
    print("... path to dummy_store_json:", path_to_dummy_json)
    with open(path_to_dummy_json, "r", encoding = "UTF-8") as file:
        store_dict = json.load(file)
    print("... Loaded dummy store data")

def test_generals():
    CrawlerHandlerTest = CrawlerHandler("DummyStore", "dummy_store_type", with_id=True, show_prints=False)

    found_products = found_products_collection.products["general"]
    CrawlerHandlerTest.handle_with_id(found_products)
    CrawlerHandlerTest.clean_data()
    prices_for_dates = CrawlerHandlerTest.STORE_JSON["products"][0]["dates"]

    assertions = [
        (len(prices_for_dates) > 1, "Price wurde dem Produkt hinzugefügt"),
        (get_current_date()  in prices_for_dates, "Heutiges Datum wurde dem Produkt hinzugefügr"),
        (get_current_date()  in CrawlerHandlerTest.STORE_JSON["historical_labels"], "Heutiges Datum wurde den historical labels hinzugefügt")
    ]

    result = assert_all(assertions)
    return result
    
def test_wrong_price():
    CrawlerHandlerTest = CrawlerHandler("DummyStore", "dummy_store_type", with_id=True, show_prints=False)

    found_products = found_products_collection.products["wrong_price"]
    CrawlerHandlerTest.handle_with_id(found_products)
    CrawlerHandlerTest.clean_data()

    assertions = [
        (is_numeric(CrawlerHandlerTest.STORE_JSON["products"][0]["dates"][get_current_date()]), "Preis hat korrektes Format"),
          (is_numeric(CrawlerHandlerTest.STORE_JSON["products"][1]["dates"][get_current_date()]), "Preis hat korrektes Format"),
        (is_numeric(CrawlerHandlerTest.STORE_JSON["products"][2]["dates"][get_current_date()]), "Preis hat korrektes Format"),
        (is_numeric(CrawlerHandlerTest.STORE_JSON["products"][3]["dates"][get_current_date()]), "Preis hat korrektes Format")
    ]

    result = assert_all(assertions)
    return result

def test_same_id():
    CrawlerHandlerTest = CrawlerHandler("DummyStore", "dummy_store_type", with_id=True, show_prints=False)

    found_products = found_products_collection.products["same_ID"]
    CrawlerHandlerTest.handle_with_id(found_products)
    CrawlerHandlerTest.clean_data()
    # print("       ")
    # for product in CrawlerHandlerTest.STORE_JSON["products"]:
    #     print(product)
    #     print("****")
    # print(CrawlerHandlerTest.STORE_JSON["products"][0]["dates"][get_current_date()])
    assertions = [
        (len(CrawlerHandlerTest.STORE_JSON["products"]) == 2, "ID Anzahl korrekt"),
        (CrawlerHandlerTest.STORE_JSON["products"][0]["dates"][get_current_date()] == "10.00", "Price korrekt hinzugefügt"),
        (CrawlerHandlerTest.STORE_JSON["products"][1]["dates"][get_current_date()] == "1.00", "Price korrekt hinzugefügt")
    ]

    result = assert_all(assertions)
    return result

def do_tests():
    global fails, tests
    print("_________________________Start Testing___________________\n")
    try:
        print("   + Test generals", test_generals())
        print("   + Test wrong price", test_wrong_price())
        print("   + Test same ID", test_same_id())

    
    except Exception as e:
        print("Fail:")
        print(e)

    print("\n_________________________End Testing___________________")
    print("\n\n", fails, "of", tests, "failed")
    print("", tests-fails, "of", tests, "passed\n\n ")


setup()
do_tests()

