import subprocess
import json
import re

from bs4 import BeautifulSoup
import requests


list_of_found_products =  []


def fetch_rewe_data():


    pageId = 1
    items = []

    while True:
        curl_command = f'curl -s "https://mobile-api.rewe.de/api/v3/product-search?searchTerm=*&page={pageId}&sorting=RELEVANCE_DESC&objectsPerPage=250&marketCode=440405&serviceTypes=PICKUP" -H "Rd-Service-Types: PICKUP" -H "Rd-Market-Id: 440405"'

        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print("Failed to fetch REWE-DE data. Either cURL is not installed or there's an issue with the request.")
            break

        firstPage = json.loads(result.stdout)
        items.extend(firstPage['products'])
        totalPages = firstPage['totalPages']

        if pageId >= totalPages:
            break

        pageId += 1

    return items

def create_product_url(name, product_id):
    # Bereinigen Sie den Namen, indem Sie Leerzeichen und Sonderzeichen entfernen
    cleaned_name = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')

    # Erstellen Sie die URL durch Hinzufügen von /p/ und der bereinigten Produkt-ID
    product_url = f"/p/{cleaned_name}/{product_id}"

    return product_url



def getting_articles_from_shop():
    global list_of_found_products
    pageId = 1
    curl_command = f'curl -s "https://mobile-api.rewe.de/api/v3/product-search?searchTerm=*&page={pageId}&sorting=RELEVANCE_DESC&objectsPerPage=250&marketCode=440405&serviceTypes=PICKUP" -H "Rd-Service-Types: PICKUP" -H "Rd-Market-Id: 440405"'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    firstPage = json.loads(result.stdout)

    pagesTotal = firstPage["totalPages"]
    print("pagesTotal:", pagesTotal)


    for pageId in range(1, pagesTotal+1):
        print("CURL PAGE", pageId, "of", pagesTotal)
        curl_command = f'curl -s "https://mobile-api.rewe.de/api/v3/product-search?searchTerm=*&page={pageId}&sorting=RELEVANCE_DESC&objectsPerPage=250&marketCode=440405&serviceTypes=PICKUP" -H "Rd-Service-Types: PICKUP" -H "Rd-Market-Id: 440405"'
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

        try:
            currentPage = json.loads(result.stdout)

            for product in currentPage["products"]:
                try:

                    #price and uit
                    if product.get("grammage") != None:
                        unit = product["grammage"].strip()

                        if "=" in unit:
                            split_unit = unit.split("=")
                            price = split_unit[1].replace(")", "")
                            unit = split_unit[0]
                            index_of_klammer = unit.index("(")
                            unit = unit[index_of_klammer+1:-1].strip()
                        else: 
                            price = product["currentPrice"].strip()
                    else:
                        price = product["currentPrice"].strip()
                        unit = "Stk"
                    

                    original_link = create_product_url(product["name"], product["id"])
                    original_link = "https://shop.rewe.de" + original_link

                    product_dict = {
                        "id" : product["id"],
                        "unit" : unit, 
                        "imageURL" : product["imageUrl"],
                        "name" : product["name"],
                        "price" : price,
                        "original_link" : original_link
                    }

                    list_of_found_products.append(product_dict)

                except Exception as e:
                    print("error", e)
                    continue
        except:
            print("Parsing for page", pageId, "not possible> continue")
            continue

    return list_of_found_products

