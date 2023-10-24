import re
import os
import sys
import datetime

cwd = ""
formatted_datetime = ""
log_string = ""

def clean_price_text( price_text):
        try:
            cleaned_price = str(price_text)
            cleaned_price = cleaned_price.replace(",",".")

            if "=" in cleaned_price:
                cleaned_price = cleaned_price.split("=")[-1]

            match = re.search(r'\d+(\.\d*)?', cleaned_price)

            if match: 
                cleaned_price = match.group()
                if(cleaned_price[-1] == "."):
                    cleaned_price = cleaned_price[:-1]
                
                return cleaned_price
            else:
                print("No cleaning possible for:", price_text)
            
                return "0"
            
        except Exception as e:
            print("ERROR IN CLEANING")
            print(e)
            print("PRICE IN:", price_text, " / PRICE IN TYPE:", type(price_text))
            print("----------------")
        
def is_numeric(value):

    price_cleaned = clean_price_text(value)
    numeric_pattern = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
    return bool(numeric_pattern.match(str(price_cleaned)))

def assert_HELLWEG():
    import scraper.scraper_HELLWEG 

    global log_string
    print("*********************************")
    print("- HELLWEG")
    log_string += "Hellweg: "

    try:
        result_product = scraper.scraper_HELLWEG.getting_articles_from_shop("tanne", show_product_to_search=True)[0]
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
    print("Done")

def assert_NETTO():
    import scraper.scraper_NETTO 
    global log_string
    print("*********************************")
    print("- NETTO...")
    log_string += "NETTO: "
    try:
        result_product = scraper.scraper_NETTO .getting_articles_from_shop("kartoffel", show_product_to_search=True)[0]
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
    print("Done")

def assert_GLOBUS():
    import scraper.scraper_GLOBUS
    global log_string
    print("*********************************")
    print("- GLOBUS...")
    log_string += "GLOBUS: "
    try:
        result_product = scraper.scraper_GLOBUS.getting_articles_from_shop("kartoffel", show_product_to_search=True)[0]
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
    print("Done")

def setup():
    global cwd,  formatted_datetime, log_string

    
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%H:%M Uhr, %d-%m-%Y")
    log_string = "Last Update: " + formatted_datetime + " (UTC, Germany +2h)\n"

    cwd = os.getcwd()
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    sys.path.append(parent_dir)

def save_testlog():
    global cwd
    if "home" in cwd:
        print("Saved in Flask Log")
        with open("/home/SebastianChristoph/mysite/static/crawler/testing/testing_log.txt", "w", encoding = "UTF-8") as file:
            file.write(log_string)
    else:
        print("LOG:\n")
        print(log_string)

def assert_all():
    print("_____________________________________________________")
    print("Start ASSERTIONS")
    assert_HELLWEG()
    assert_NETTO()
    assert_GLOBUS()
    print("_____________________________")
    print("End of Assertion.")

assert_all()