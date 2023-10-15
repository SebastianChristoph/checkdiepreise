from bs4 import BeautifulSoup
import requests
import json

URL = "https://www.mueller.de/search/?q="
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

def getting_articles_from_shop(poduct_to_search,  show_product_to_search = False): 
    list_products = []
    list_of_found_products = []
    s = requests.Session()
    s.headers = headers
    source = s.get(URL+poduct_to_search, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    list_products = soup.find_all("div", class_="mu-product-list__item")

    if show_product_to_search:
        if(len(list_products) == 0):
            print(">> FOUND NO PRODUCTS!")

            with open("testing_log_MUELLER.html", "w", encoding = "UTF-8") as file:
                print("source saved in testing_log_MUELLER.html")
                file.write(soup.prettify())
        
        with open("testing_log_MUELLER.html", "w", encoding = "UTF-8") as file:
            file.write(list_products[0].prettify())
            print(">> div class='mu-product-list__item' saved in testing_log_MUELLER.html")


        print("Found products:", len(list_products))
  
    for product in list_products:
        try:
            data = product.get("data-gtm-json")
            pdict = json.loads(data)

            # TILE
            try:
                title = pdict["ecommerce"]["impressions"][0]["name"]
            except:
                continue

            # PRICE
            try:
                price = pdict["ecommerce"]["impressions"][0]["price"]
            except:
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

        except:
            continue
        
        product_dict = {
            "imageURL" : imageURL,
            "name" : title,
            "price" : price,
            "original_link" : original_link
        }

        list_of_found_products.append(product_dict)
    
    return list_of_found_products
