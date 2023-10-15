from bs4 import BeautifulSoup
import requests

URL = "https://www.hellweg.de/search?order=score&p=1&search="
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

def getting_articles_from_shop(poduct_to_search, show_product_to_search = False): 
    list_products = []
    list_of_found_products = []
   
    source = requests.get(URL + poduct_to_search, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    list_products = soup.find_all("div", class_="product-box")

    if show_product_to_search:
        if(len(list_products) == 0):
            print(">> FOUND NO PRODUCTS!")

        print("div class='product-box' saved in testing_log_HELLWEG.html")
        print("Found products:", len(list_products))
        with open("testing_log_HELLWEG.html", "w", encoding = "UTF-8") as file:
            file.write(list_products[0].prettify())

    for product in list_products:
        try:

            # IMAGE URL
            try:
                image_source = product.find("img")
                imageURL = image_source.get("data-src").strip()
            except:
                imageURL = ""

            # STORE LINK
            try: 
                original_link_wrapper = product.find("a", class_ = "product-image-link")
                original_link = original_link_wrapper.get("href").strip()
            except:
                original_link = ""

            # TITLE
            try:
                title_link = product.find("a", class_="product-image-link")
                title = title_link.get("title").strip()
            except:
                continue
        
            # PRICE
            try:
                price = product.find("div", class_ = "price-wrapper").text.strip()
            except:
                continue

            product_dict = {
                "imageURL" : imageURL,
                "name" : title,
                "price" : price,
                "original_link" : original_link
            }

            list_of_found_products.append(product_dict)
        except:
            continue

    return list_of_found_products