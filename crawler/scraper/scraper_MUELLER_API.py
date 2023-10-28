
import requests
import json
import os
import time
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

categories = {}
found_products = []
cool_down = 20
errors = 0

def getting_max_page_from_soup(category_url):
    global errors
    page = 1
    url = f"{category_url}?p={page}"
    base_url =  f"{url}?ajax=true&p={page}"
    backoff = 2

    while True:
        response = requests.get(base_url)
        if response.status_code == 404:
            print(f"Couldn't fetch {base_url}, retrying in {backoff} seconds.")
            time.sleep(backoff)
            backoff *= 2
        elif 200 <= response.status_code < 300:
            soup = BeautifulSoup(response.text, "lxml")
        else:
            # Handle other status codes as needed
            print("getting max page klappte nicht")
            print(e)
            errors += 1
            return 1
        
        try:
            found_articles_wrapper = soup.find("span", class_ = "mu-product-list-page__headline-count").text.strip()
            print(found_articles_wrapper)
            found_articles =re.findall(r'\d+', found_articles_wrapper)
            found_articles_string = "".join(found_articles)
            found_articles = int(found_articles_string)
            max_pages = found_articles // 60
            if found_articles % 60 != 0:
                max_pages += 1
            return max_pages

        except Exception as e:
            print("getting max page klappte nicht")
            print(e)
            errors += 1
            return 1

def get_path_for_file(filename, directory):
    # Pfad zur aktuellen Datei (test.py)
    current_dir = os.path.dirname(__file__)

    # Pfad zur JSON-Datei relativ zur aktuellen Datei
    file_relative_path = os.path.join('..', directory, filename)

    # Den absoluten Pfad zur JSON-Datei erstellen
    file_path = os.path.abspath(os.path.join(current_dir, file_relative_path))

    return file_path

def get_categories():
    global categories
    url =   "https://www.mueller.de/ajax/burgermenu/"
    path_to_backup_file = get_path_for_file("mueller_categories.json", "jsons")
    print("Get Categories")
    try:
        s = requests.Session()
        s.headers = headers
        source = s.get(url, headers = headers).text
        print("...Try convert response in dict")
       
        response_dict = json.loads(source)
   
        print("...error convertig response as dict, error:")
        print("...", e)
        print("********************")
    
    
        for category in response_dict:
            data_dict = { "url" : category["url"], 
                         "main_category" : category["name"]
                         }

            categories[category["name"]] = data_dict

            for subcategory in category["subcategories"]:
                data_dict = { 
                    "url" : subcategory["url"],       "main_category" : category["name"]
                    } 
                categories[subcategory["name"]] = data_dict
        
        print("categories saved in backup json")
        
        with open(path_to_backup_file, "w", encoding="UTF-8") as outfile: 
            json.dump(categories, outfile)

    except Exception as e:
        print("ERROR", e)
        print("Get dict from text because of error above")
        with open(path_to_backup_file, "r", encoding="UTF-8") as file:
            json_content = file.read()
            response_dict = json.loads(json_content)
        print("...Done")
        print("...Categories:", len(response_dict))

        print("Try reading dict from backupFile")
        for category in response_dict:        
            categories[category] = { "url" : response_dict[category]["url"], "main_category" : response_dict[category]["main_category"]}
        print("Done")

def get_products_for_category(category_name, category_url):
    global found_products, errors
    retries = 0
    print("Process data for", category_name, "[errors:", errors, "]")
    category_url = category_url +"?ajax=true&p=1"
    try:
        s = requests.Session()
        s.headers = headers
        source = s.get(category_url, headers = headers).text
        response_dict = json.loads(source)
        page_max = int(response_dict["productlistresult"]["pager"]["pages"][-1])
        # temporär
        # page_max=3
    except Exception as e:
        print("...error in getting resonse:", e)
        print("Set maxPage to 3 as default")
        page_max=3
    for page in range(1, page_max+1):
        try:
            print("...Crawl page", page, "of", page_max)
            category_url = category_url + f"?ajax=true&p={page}"
            s = requests.Session()
            s.headers = headers
            source = s.get(category_url, headers = headers).text
            response_dict = json.loads(source)

            for product in response_dict["productlistresult"]["products"]:

                if product["priceInfo"].get("basePrice") != None:
                    price = product["priceInfo"]["basePrice"]["price"]
                    unit =  product["priceInfo"]["basePrice"]["quantity"]
                else:
                    price = product["priceInfo"]["price"]
                    unit = "Stk."

                new_dict = {
                    "name" : product["dataLayer"]["ecommerce"]["brandName"]+ " - " + product["name"],
                    "unit" : unit,
                    "price" : price, 
                    "id":  product["productId"],
                    "imageURL" : product["imageUrl"],
                    "original_link" : product["productUrl"],
                    "category" : response_dict["categoryHeadline"]
                }
                found_products.append(new_dict)
        except Exception as e:
            print("...... Error:", e)
            if(retries > 1):
                print("MORE THEN 3 ERRORS >> ABORT CATEGORY <<")
                errors += 1
                print("COOL DOWN FOR", cool_down, "seoconds")
                time.sleep(cool_down)
                break
            else:
                retries += 1
            continue

def get_products_for_category_html(category_name, category_url):
    global found_products
    list_products = []
    max_pages = getting_max_page_from_soup(category_url)
    print("FOUND", max_pages, " pages for category", category_name)
    print("Start Crawling")

    for page in range(1, max_pages+1):
        print("... page", page, "of", max_pages)
        url = f"{category_url}?p={page}"
        base_url =  f"{url}?ajax=true&p={page}"
        backoff = 2

        while True:
            response = requests.get(base_url)
            if response.status_code == 404:
                print(f"Couldn't fetch {base_url}, retrying in {backoff} seconds.")
                time.sleep(backoff)
                backoff *= 2
            elif 200 <= response.status_code < 300:
                soup = BeautifulSoup(response.text, "lxml")
                list_products = soup.find_all("div", class_="mu-product-list__item")
            else:
                # Handle other status codes as needed
                return None

            try:
                # url = category_url+ "?p=" + str(page)
                # s = requests.Session()
                # s.headers = headers
                # source = s.get(url, headers = headers).text
                # soup = BeautifulSoup(source, "lxml")
                # list_products = soup.find_all("div", class_="mu-product-list__item")
                # # with open("mullbert.html", "w", encoding = "UTF-8") as file:
                # #     file.write(soup.prettify())

                print("Found products:", len(list_products))
            
                for product in list_products:
                    try:
                        data = product.get("data-gtm-json")
                        pdict = json.loads(data)

                        # TILE
                        try:
                            title =  pdict["ecommerce"]["impressions"][0]["brand"] + " - " + pdict["ecommerce"]["impressions"][0]["name"]
                        except:
                            print("no tilte")
                            continue

                        #ID
                        try:
                            id = pdict["ecommerce"]["impressions"][0]["id"]
                        except:
                            print("no id")
                            continue

                        # PRICE

                        found_base_price = False
                        try:
                            baseprice = product.find("div", class_ = "mu-product-tile__additional-info").text
                            if "=" in baseprice:
                                baseprice_split  = baseprice.split("=")
                                price = baseprice_split[0]
                                unit = baseprice_split[1]
                                found_base_price = True
                            else:
                                found_base_price = False
                        except:
                            found_base_price = False
                        
                        try:
                            if found_base_price == False:
                                price = pdict["ecommerce"]["impressions"][0]["price"]
                                unit = "Stk"
                        except:
                            print("no price")
                            continue

                        # IMAGE URL
                        try:
                            image_source = product.find("img") 
                            imageURL = image_source.get("src")
                        except:
                            imageURL = ""

                        # SHOP LINK
                        try:
                            original_link = product.find("a", class_="mu-product-tile__link").get("href")
                            original_link = "https://www.mueller.de" + original_link
                        except:
                            original_link = ""

                    except Exception as e:
                        print("MAIN ERROR:", e)
                        continue
                    
                    product_dict = {
                        "imageURL" : imageURL,
                        "id" : id,
                        "unit" : unit,
                        "name" : title,
                        "price" : price,
                        "original_link" : original_link
                    }
                    if product_dict not in found_products:
                        found_products.append(product_dict)
                    else:
                        print(".....product already in list")
            except Exception as e:
                print("...ERROR IN CRAWLING PAGE", page, ":", e)
        

def get_products_from_shop():
    global categories, errors
    get_categories()
    current = 0
 
    for category in categories:
        if errors > 3:
            print("\n\nAPI NOT RESPONDING PROPERLY, ABORT\n\n")
            return 
        print("_________________________________________________")
        print(current, "of", len(categories))
        get_products_for_category_html(categories[category]["main_category"], categories[category]["url"])
        current += 1

    print(len(found_products))
    print("errors:", errors)
    return found_products

