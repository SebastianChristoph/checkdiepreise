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

def get_category():

    pass
    #  # Set the user-agent header
    # user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'

    # # Set the URL
    # URL = "https://shop.rewe.de/p/salatgurke-1-stueck/483303"

    # # Construct the cURL command
    # curl_command = f'curl -s -A "{user_agent}" -o /home/SebastianChristoph/mysite/static/crawler/rewe.html "{URL}"'

    # try:
    #     # Execute the cURL command
    #     subprocess.run(curl_command, shell=True)
    #     print("HTML page saved in rewe.html")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error: {e}")


    # headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}
    # URL = "https://shop.rewe.de/p/salatgurke-1-stueck/483303"

    # s = requests.Session()
    # s.headers = headers
    # source = s.get(URL, headers = headers).text
    # soup = BeautifulSoup(source, "lxml")





def getting_articles_from_shop():
    global list_of_found_products
    pageId = 1
    curl_command = f'curl -s "https://mobile-api.rewe.de/api/v3/product-search?searchTerm=*&page={pageId}&sorting=RELEVANCE_DESC&objectsPerPage=250&marketCode=440405&serviceTypes=PICKUP" -H "Rd-Service-Types: PICKUP" -H "Rd-Market-Id: 440405"'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    firstPage = json.loads(result.stdout)

    pagesTotal = firstPage["totalPages"]
    print("pagesTotal:", pagesTotal)

    #print(firstPage["products"][0])

    # {'id': '483303', 'listingId': '13-8436000259209-rewe-online-services|4640405-440405', 'name': 'Salatgurke 1 Stück', 'grammage': '1 Stück', 'imageUrl': 'https://img.rewe-static.de/0483303/24569873_digital-imag
    # e.png', 'tags': ['discounted'], 'currentPrice': '0,49 €', 'discount': {'regularPrice': '0,55 €', 'discountRate': '10%', 'expiration': '21.10.'}, 'hasBioCide': False, 'orderLimit': 15}

    # for product in firstPage["products"]:
    #     try:

    #         if product.get("grammage") != None:
    #             price = product["grammage"]

    #             if "=" in price:
    #                 price = price.split("=")[-1]
    #             else:
    #                 price = product["currentPrice"]
    #         else:
    #             price = product["currentPrice"]


    #         original_link = create_product_url(product["name"], product["id"])
    #         original_link = "https://shop.rewe.de" + original_link


    #         product_dict = {
    #             "id" : product["id"],
    #             "imageURL" : product["imageUrl"],
    #             "name" : product["name"],
    #             "price" : price,
    #             "original_link" : original_link
    #         }

    #         list_of_found_products.append(product_dict)

    #     except Exception as e:
    #         print("error", e)


    for pageId in range(1, pagesTotal+1):
        print("CURL PAGE", pageId, "of", pagesTotal)
        curl_command = f'curl -s "https://mobile-api.rewe.de/api/v3/product-search?searchTerm=*&page={pageId}&sorting=RELEVANCE_DESC&objectsPerPage=250&marketCode=440405&serviceTypes=PICKUP" -H "Rd-Service-Types: PICKUP" -H "Rd-Market-Id: 440405"'
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

        try:
            currentPage = json.loads(result.stdout)
            for product in currentPage["products"]:
                try:

                    if product.get("grammage") != None:
                        price = product["grammage"]

                        if "=" in price:
                            price = price.split("=")[-1]
                        else:
                            price = product["currentPrice"]

                    else:
                        price = product["currentPrice"]


                    original_link = create_product_url(product["name"], product["id"])
                    original_link = "https://shop.rewe.de" + original_link

                    product_dict = {
                        "id" : product["id"],
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

    print(len(list_of_found_products))
    print("example:")
    print(list_of_found_products[0])


