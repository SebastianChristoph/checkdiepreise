from bs4 import BeautifulSoup
import requests

URL = "https://www.kaufland.de/item/search/?search_value="
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

def getting_articles_from_shop(poduct_to_search, show_product_to_search = False): 
    list_products = []
    list_of_found_products = []
    source = requests.get(URL+poduct_to_search, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    list_products = soup.find_all("article", class_="product")

   
    if show_product_to_search:
        if(len(list_products) == 0):
            print(">> FOUND NO PRODUCTS!")

        with open("testing_log_KAUFLAND.html", "w", encoding = "UTF-8") as file:
            file.write(list_products[0].prettify())
            print(">> article class='product' saved in testin_log_KAUFLAND.html")
            print("Found products:", len(list_products))
        
        # save soup
        with open("testing_log_SORCE_KAUFLAND.html", "w", encoding = "UTF-8") as file:
            file.write(soup.prettify())
            print("soup saved in testing_log_SOURCE_KAUFLAND.html")
        
        print("Found products:", len(list_products))


    for product in list_products:

        # IMAGE URL
        try:
            image_source = product.find("source")
            imageURL = image_source.get("srcset").strip()
        except:
            imageURL = ""
        
        # TITLE
        try:
            title = product.find("div", class_="product__title").text.strip()
        except:
            continue

        # SHOP LINK
        try:
            original_link_wrapper = product.find("a", class_ = "product__wrapper")
            original_link = "http://www.kaufland.de" + original_link_wrapper.get("href").strip()
        except:
            original_link = ""

        # PRICE
        found_base_price = False
        try:
           
            # try:
            #     product_base_price = product.find("div", class_="product__base-price").text.strip()
            #     found_base_price = True
            #     price = product_base_price
            # except:
            #     found_base_price = False

            # if(found_base_price == False):
                price = product.find("div", class_="price").text.strip()
              
        except:
            if show_product_to_search:
                print("error")
                print(product.prettify())
                print("#################")
            continue

        product_dict = {
            "imageURL" : imageURL,
            "name" : title,
            "price" : price,
            "original_link" : original_link
        }

        list_of_found_products.append(product_dict)

    return list_of_found_products
