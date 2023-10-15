from bs4 import BeautifulSoup
import requests
import crawler_handler

URL1 = "https://www.obi.de/search/"
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

def getting_articles_from_shop(poduct_to_search): 
    list_of_found_products = []

    s = requests.Session()
    s.header = headers
    s.max_redirects = 60
    source = s.get(URL1+poduct_to_search, headers = headers, allow_redirects=True).text
    soup = BeautifulSoup(source, "lxml")

    list_products = soup.find_all("div", class_="artikelkachel")
    print(len(list_products))

    for product in list_products:
        try:
            image_source = product.find("img")
            imageURL = image_source.get("src")
            title = image_source.get("title")

            prices = product.find("div", class_ = "find-h-preise")
            price =prices.find("span").text.replace("€", "").replace("*", "").replace(",",".").strip()

            product_dict = {
                "imageURL" : imageURL,
                "name" : title,
                "price" : price
            }
            
            list_of_found_products.append(product_dict)
        except Exception as e:
            continue

    return list_of_found_products


Crawler_Handler = crawler_handler.CrawlerHandler("Obi")

for prodcut_to_find in Crawler_Handler.PRODUCTS_TO_CHECK:
     print("Searching products for:", prodcut_to_find, ", found: ", end = "")
     found_products = getting_articles_from_shop(prodcut_to_find)
     Crawler_Handler.handle(found_products, prodcut_to_find)


print("Finish Looping")

Crawler_Handler.clean_data_if_null()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()