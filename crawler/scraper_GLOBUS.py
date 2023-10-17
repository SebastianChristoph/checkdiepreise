from bs4 import BeautifulSoup
import requests

URL = "https://www.globus-baumarkt.de/search/result?query="
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

def getting_articles_from_shop(poduct_to_search, show_product_to_search = False): 
    list_products = []
    list_of_found_products = []
   
    source = requests.get(URL + poduct_to_search, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    list_products = soup.find_all("div", class_="card product-box box-standard")

    if show_product_to_search:
        if(len(list_products) == 0):
            print(">> FOUND NO PRODUCTS!")
        
        else:

            print("div class='card product-box box-standard' saved in testing_log_GLOBUS.html")
            with open("testing_log_GLOBUS.html", "w", encoding = "UTF-8") as file:
                file.write(list_products[0].prettify())
            
            #save soup
            print("soup saved in testing_log_SOURCE_HELLWEG.html")
            with open("testing_log_SOURCE_GLOBUS.html", "w", encoding = "UTF-8") as file:
                file.write(soup.prettify())
        
        print("Found products:", len(list_products))

    for product in list_products:
        try:
           
            # IMAGE URL
            try:
                image_wrapper = product.find("div", class_= "product-image-wrapper")
                imgediv = image_wrapper.find("img")
                imageURL = imgediv.get("srcset")               
            except:
                imageURL = ""

            # # STORE LINK
            try: 
                image_wrapper = product.find("div", class_= "product-image-wrapper")
                linkwrapper = image_wrapper.find("a")
                original_link = "https://www.globus-baumarkt.de" + linkwrapper.get("href").strip()
            except:
                original_link = ""

            # TITLE
            try:
                title_link = product.find("a", class_="product-image-link")
                title = title_link.get("title").strip()

                if "{" in title:
                    continue
            except:
                continue
        
            # PRICE
            try:
                priceWrapper = product.find("div", class_ = "product-price")
                price = priceWrapper.text.strip()
                if "%" in price:
                    spans = priceWrapper.find_all("span")
                    price = spans[-1].text
                       
                if "{" in price:
                    continue
            except Exception as e:
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
