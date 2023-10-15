from bs4 import BeautifulSoup
import requests

URL = "https://www.rossmann.de/de/search/?text="
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

SHOW_PRINTS = True

def getting_articles_from_shop(poduct_to_search, show_product_to_search = False): 
    list_of_found_products = []
    list_products = []
    s = requests.Session()
    s.headers = headers
    source = s.get(URL+poduct_to_search, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    list_products = soup.find_all("div", class_="rm-grid__content")

    if show_product_to_search:
        if(len(list_products) == 0):
            print(">> FOUND NO PRODUCTS!")
            with open("testing_log_ROSSMANN.html", "w", encoding = "UTF-8") as file:
                file.write(soup.prettify())
                print(">> soup saved in testing_log_ROSSMANN.html")
        else:
            with open("testing_log_ROSSMANN.html", "w", encoding = "UTF-8") as file:
                file.write(soup.prettify())
                print(">> div class='rm-grid__conent' saved in testing_log_ROSSMANN.html")

        print("Found products:", len(list_products))

    for product in list_products:
        try:

            # TITLE
            try:
                title = product.find("div", class_ = "rm-product__title").text.strip()
            except:
                continue

            # PRICE
            try:
                price = product.find("div", class_ = "rm-price__base").text.strip()
            except:
                continue

            # IMAGE URL
            try:
                image_source = product.find("source") 
                imageURL = image_source.get("data-srcset")
                imageURL = imageURL.split("?")[0].strip()
            except:
                imageURL = ""
            
            # SHOP LINK
            try:
                original_link = product.find("a", class_="rm-tile-product__headline").get("href")
                original_link = "https://www.rossmann.de" + original_link.strip()
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

