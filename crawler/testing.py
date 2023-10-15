import scraper_HELLWEG, scraper_KAUFLAND, scraper_MUELLER, scraper_NETTO, scraper_ROSSMANN
import re
import os
import datetime


def is_numeric(value):
    numeric_pattern = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
    return bool(numeric_pattern.match(str(value)))

now = datetime.datetime.now()
formatted_datetime = now.strftime("%H:%M Uhr, %d-%m-%Y")

log_string = "Last Update: " + formatted_datetime + " (UTC, Germany +2h)\n"

def assert_HELLWEG():
    global log_string
    print("*********************************")
    print("Start assert HELLWEG...")
    log_string += "Hellweg: "
    try:
        result_product = scraper_HELLWEG.getting_articles_from_shop("holz", show_product_to_search=True)[0]
        assert result_product["imageURL"] != "", "No data for imageURL"
        assert result_product["name"] != "", "No data for name"
        assert result_product["price"] != "", "No data for price"
        assert is_numeric(result_product["price"]) == True, f"Price {result_product['price']}is not numeric"
        assert result_product["original_link"] != "", "No data for original link"
        assert result_product["original_link"] != "#", "No data for original link"
    except Exception as e:
        print("ERROR")
        log_string += str(e) + "\n"
        print(e)
    log_string += "Done. \n"
    print("done")

def assert_KAUFLAND():
    global log_string
    print("*********************************")
    print("Start assert KAUFLAND...")
    log_string += "KAUFLAND: "
    try:
        result_product = scraper_KAUFLAND.getting_articles_from_shop("kartoffel", show_product_to_search=True)[0]
        assert result_product["imageURL"] != "", "No data for imageURL"
        assert result_product["name"] != "", "No data for name"
        assert result_product["price"] != "", "No data for price"
        assert is_numeric(result_product["price"]) == True, f"Price {result_product['price']}is not numeric"
        assert result_product["original_link"] != "", "No data for original link"
    except Exception as e:
        print("ERROR")
        log_string += str(e) + "\n"
        print(e)
    log_string += "Done. \n"
    print("done")

def assert_MUELLER():
    global log_string
    print("*********************************")
    print("Start assert MUELLER...")
    log_string += "MUELLER: "
    try:
        result_product = scraper_MUELLER.getting_articles_from_shop("duft", show_product_to_search=True)[0]
        assert result_product["imageURL"] != "", "No data for imageURL"
        assert result_product["name"] != "", "No data for name"
        assert result_product["price"] != "", "No data for price"
        assert is_numeric(result_product["price"]) == True, f"Price {result_product['price']}is not numeric"
        assert result_product["original_link"] != "", "No data for original link"
    except Exception as e:
        print("ERROR")
        log_string += str(e) + "\n"
        print(e)
    log_string += "Done. \n"
    print("done")


def assert_NETTO():
    global log_string
    print("*********************************")
    print("Start assert NETTO...")
    log_string += "NETTO: "
    try:
        result_product = scraper_NETTO.getting_articles_from_shop("kartoffel", show_product_to_search=True)[0]
        assert result_product["imageURL"] != "", "No data for imageURL"
        assert result_product["name"] != "", "No data for name"
        assert result_product["price"] != "", "No data for price"
        assert is_numeric(result_product["price"]) == True, f"Price {result_product['price']}is not numeric"
        assert result_product["original_link"] != "", "No data for original link"
    except Exception as e:
        print("ERROR")
        log_string += str(e) + "\n"
        print(e)
    log_string += "Done. \n"
    print("done")

def assert_ROSSMANN():
    global log_string
    print("*********************************")
    print("Start assert ROSSMANN...")
    log_string += "ROSSMANN: "
    try:
        result_product = scraper_ROSSMANN.getting_articles_from_shop("kartoffel", show_product_to_search=True)[0]
        assert result_product["imageURL"] != "", "No data for imageURL"
        assert result_product["name"] != "", "No data for name"
        assert result_product["price"] != "", "No data for price"
        assert is_numeric(result_product["price"]) == True, f"Price {result_product['price']}is not numeric"
        assert result_product["original_link"] != "", "No data for original link"
    except Exception as e:
        print("ERROR")
        log_string += str(e) + "\n"
        print(e)
    log_string += "Done. \n"
    print("done")



assert_HELLWEG()
assert_KAUFLAND()
assert_MUELLER()
assert_NETTO()
assert_ROSSMANN()


cwd = os.getcwd()
if "home" in cwd:
    print("Saved in Flask Log")
    with open("/home/SebastianChristoph/mysite/static/crawler/testing_log.txt", "w", encoding = "UTF-8") as file:
        file.write(log_string)
else:
    print("LOG:")
    print(log_string)
print("___________________________________")
print("End of Assertion.")
