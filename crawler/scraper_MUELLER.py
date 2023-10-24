from bs4 import BeautifulSoup
import requests
import json
import re

URL = "https://www.mueller.de/search/?q="
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

def getting_max_page_from_soup(soup):
    try:
        found_articles_wrapper = soup.find("span", class_ = "mu-product-list-page__headline-count").text.strip()
        print(found_articles_wrapper)
        found_articles =re.findall(r'\d+', found_articles_wrapper)
        found_articles_string = "".join(found_articles)
        found_articles = int(found_articles_string)
        max_pages = found_articles // 60
        if found_articles % 60 != 0:
            max_pages += 1
        return max_pages

    except Exception as e:
        print("getting max page klappte nicht")
        print(e)
        return 1


def getting_articles_from_shop(poduct_to_search,  show_product_to_search = False): 
    list_products = []
    list_of_found_products = []
    s = requests.Session()
    s.headers = headers
    source = s.get("https://www.mueller.de/parfuemerie/duefte-fuer-ihn/", headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    with open("mullerbert.html", "w", encoding = "UTF-8") as file:
        file.write(soup.prettify())
    return

    max_pages = getting_max_page_from_soup(soup)
    print("FOUND", max_pages, "for search term", poduct_to_search)
    print("Start Crawling")

    for page in range(1, max_pages+1):
        print("... page", page, "of", max_pages)
        try:
            s = requests.Session()
            s.headers = headers
            source = s.get(URL+poduct_to_search+"&p="+str(page), headers = headers).text
            soup = BeautifulSoup(source, "lxml")
            list_products = soup.find_all("div", class_="mu-product-list__item")
            # with open("mullbert.html", "w", encoding = "UTF-8") as file:
            #     file.write(soup.prettify())

            if show_product_to_search:
                if(len(list_products) == 0):
                    print(">> FOUND NO PRODUCTS!")

                    with open("testing_log_MUELLER.html", "w", encoding = "UTF-8") as file:
                        print("source saved in testing_log_MUELLER.html")
                        file.write(soup.prettify())
                
                with open("testing_log_MUELLER.html", "w", encoding = "UTF-8") as file:
                    file.write(list_products[0].prettify())
                    print(">> div class='mu-product-list__item' saved in testing_log_MUELLER.html")
                
                ## saving source?
                with open("testing_log_SOURCE_MUELLER.html", "w", encoding = "UTF-8") as file:
                    file.write(soup.prettify())
                    print(">> soup saved in testing_log_SOURCE_MUELLER.html")


                print("Found products:", len(list_products))
        
            for product in list_products:
                try:
                    data = product.get("data-gtm-json")
                    pdict = json.loads(data)

                    # TILE
                    try:
                        title =  pdict["ecommerce"]["impressions"][0]["brand"] + " - " + pdict["ecommerce"]["impressions"][0]["name"]
                    except:
                        print("no tilte")
                        continue

                    #ID
                    try:
                        id = pdict["ecommerce"]["impressions"][0]["id"]
                    except:
                        print("no id")
                        continue

                    # PRICE

                    found_base_price = False
                    try:
                        baseprice = product.find("div", class_ = "mu-product-tile__additional-info").text
                        if "=" in baseprice:
                            baseprice_split  = baseprice.split("=")
                            price = baseprice_split[0]
                            unit = baseprice_split[1]
                            found_base_price = True
                        else:
                            found_base_price = False
                    except:
                        found_base_price = False
                    
                    try:
                        if found_base_price == False:
                            price = pdict["ecommerce"]["impressions"][0]["price"]
                            unit = "Stk"
                    except:
                        print("no price")
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

                except Exception as e:
                    print("MAIN ERROR:", e)
                    continue
                
                product_dict = {
                    "imageURL" : imageURL,
                    "id" : id,
                    "unit" : unit,
                    "name" : title,
                    "price" : price,
                    "original_link" : original_link
                }
                if product_dict not in list_of_found_products:
                    list_of_found_products.append(product_dict)
                else:
                    print("product already in list")
        except Exception as e:
            print("...ERROR IN CRAWLING PAGE", page, ":", e)
    
    print(len(list_of_found_products))
    return list_of_found_products


getting_articles_from_shop("makeup")