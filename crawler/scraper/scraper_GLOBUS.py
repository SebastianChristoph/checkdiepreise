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

    # with open("example_response_globus.html", "w", encoding="UTF-8") as file:
    #     file.write(list_products[0].prettify())

    # with open("globus.html", "w", encoding="UTF-8") as file:
    #     file.write(soup.prettify())
    # return

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


            # ORIGINAL LINK and ID
            try: 
                image_wrapper = product.find("div", class_= "product-image-wrapper")
                linkwrapper = image_wrapper.find("a")
                original_link = "https://www.globus-baumarkt.de" + linkwrapper.get("href").strip()

                id= original_link.split("-")[-1].replace("/", "")
            except:
                original_link = ""
                continue
            
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
                found_price_unit = False

                try:
                    price_unit = product.find("span", class_ ="unit")
                    price = price_unit.text.strip()
                    price_spit = price.split("/")
                    price = price_spit[0].strip()
                    unit = price_spit[1].strip()
                    found_price_unit = True
                    # print("1", price, unit)
                    if (price == ""):
                        # print("skipped")
                        found_price_unit = False
                except:
                    found_price_unit = False

                if found_price_unit == False:
                    try:
                        unit_price = product.find("span", class_ = "product-unit-price")
                        price = unit_price.text.strip()
                        price_spit = price.split("/")
                        price = price_spit[0].strip()
                        unit = price_spit[1].strip()
                        found_price_unit = True
                        #print("2", price, unit)
                        if (price == ""):
                            # print("skipped")
                            found_price_unit = False
                        
                    except:
                        found_price_unit = False
                
                if found_price_unit == False:
                    try:
                        price_wrapper = product.find("div", class_ = "product-price")
                        price = price_wrapper.text.strip()
                        unit = "Stk/L/kg"
                        if "%" in price:
                            spans = price_wrapper.find_all("span")
                            price = spans[-1].text
                        
                        #print("3", price, unit)
                      
                    except:
                        print("no price possible")
                        continue

        
                if "{" in price:
                    continue
            
                # print("**************************")
                # print(price, unit)
                
               
            except Exception as e:
                print("ERROR", e)
                continue

            product_dict = {
                "id" : id, 
                "unit": unit,
                "imageURL" : imageURL,
                "name" : title,
                "price" : price,
                "original_link" : original_link
            }

            list_of_found_products.append(product_dict)

        except:
            continue

    return list_of_found_products



getting_articles_from_shop("mehl")