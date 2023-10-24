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

    # with open("example_response_hellweg.html", "w", encoding="UTF-8") as file:
    #     file.write(list_products[3].prettify())
    

    if show_product_to_search:
        if(len(list_products) == 0):
            print(">> FOUND NO PRODUCTS!")
        
        else:

            print("div class='product-box' saved in testing_log_HELLWEG.html")
            with open("testing_log_HELLWEG.html", "w", encoding = "UTF-8") as file:
                file.write(list_products[0].prettify())
            
            #save soup
            print("soup saved in testing_log_SOURCE_HELLWEG.html")
            with open("testing_log_SOURCE_HELLWEG.html", "w", encoding = "UTF-8") as file:
                file.write(soup.prettify())
        
        print("Found products:", len(list_products))

    for product in list_products:
        try:

            #id
            try:
                product_wrapper = product.find("div", class_ = "product-image-wrapper")
                product_link = product_wrapper.find("a", class_ = "product-image-link")
                id = product_link.get("data-product-id")
            except:
                print("no id found")
                continue

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
                brand = product.find("div", class_ ="manufacturer-name").text.strip()
                title = brand + " - " + title_link.get("title").strip()

            except:
                continue
        
            # PRICE
            try:
                unit = "Stk."
                found_base_price = False
                try:
                    base_price_wrapper = product.find("span", class_= "price-unit-reference")
                    price = base_price_wrapper.text.strip()
                    price_split = price.split("/")
                    price = price_split[0]
                    unit = price_split[1]

                except:
                    found_base_price = False
                
                if found_base_price == False:
                    try:
                        price = product.find("div", class_ = "price-wrapper").text.strip()
                        unit = "Stk."
                    except:
                        print("no price found")
                        continue
            except:
                print("error")
                continue

            product_dict = {
                "id" : id,
                "unit" : unit,
                "imageURL" : imageURL,
                "name" : title,
                "price" : price,
                "original_link" : original_link
            }

            list_of_found_products.append(product_dict)
        except:
            continue

    return list_of_found_products

