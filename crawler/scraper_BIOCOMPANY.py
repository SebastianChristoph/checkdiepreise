from bs4 import BeautifulSoup
import requests

URL = "https://www.biocompany.de/neuigkeiten/angebote.html"
URL_Dresden = "https://www.biocompany.de/neuigkeiten/angebote.html"
headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

SHOW_PRINTS = True

def getting_articles_from_shop(show_product_to_search = False): 
    list_of_found_products = []
    list_products = []
    s = requests.Session()
    s.headers = headers
    source = s.get(URL, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    list_products = soup.find_all("div", class_="dealscard")

    print(list_products[0])

    s2 = requests.Session()
    s2.headers = headers
    source = s2.get(URL_Dresden, headers = headers).text
    soup = BeautifulSoup(source, "lxml")
    list_products2 = soup.find_all("div", class_="dealscard")

    set1 = set(list_products)
    set2 = set(list_products2)

    in_second_but_not_in_first = set2 - set1

    result = list_products + list(in_second_but_not_in_first)

    if show_product_to_search:
        if(len(result) == 0):
            print(">> FOUND NO PRODUCTS!")
            with open("testing_log_BIOCOMPANY.html", "w", encoding = "UTF-8") as file:
                file.write(soup.prettify())
                print(">> soup saved in testing_log_BIOCOMPANY.html")
        else:
            with open("testing_log_BIOCOMPANY.html", "w", encoding = "UTF-8") as file:
                file.write(result[0].prettify())
                print(">> div class='rdealscard' saved in testing_log_BIOCOMPANY.html")
            
            # save soup
            with open("testing_log_SOUP_BIOCOMPANY.html", "w", encoding = "UTF-8") as file:
                file.write(soup.prettify())
                print("soup saved in testing_log_SOURCE-BIOCOMPANY.html")


        print("Found products:", len(result))

    for product in result:
        try:
            # TITLE
            try:
                title = product.find("h3").text.strip()
            except:
                continue

            # PRICE
            try:
                pricelist = product.find_all("p")
                for price_in_list in pricelist:
                    if "=" in price_in_list.text:
                        price = price_in_list.text.split("=")[-1]
                        break
                
                if price == "":
                    continue
            except Exception as e:
                print("error", e)
                continue

            # IMAGE URL
            try:
                image_source = product.find("img") 
                imageURL = "https://www.biocompany.de" + image_source.get("src").strip()
            except:
                imageURL = ""
            
            # SHOP LINK
            original_link = URL
            
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

getting_articles_from_shop(True)