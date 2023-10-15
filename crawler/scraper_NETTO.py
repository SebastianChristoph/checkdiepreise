from bs4 import BeautifulSoup
import requests
URL = "https://www.netto-online.de/INTERSHOP/web/WFS/Plus-NettoDE-Site/de_DE/-/EUR/ViewMMPParametricSearch-Browse?SearchScope=product&SearchTerm="
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

def getting_articles_from_shop(poduct_to_search, show_product_to_search = False): 
     list_products = []
     list_of_found_products = []
     s = requests.Session()
     s.headers = headers
     source = s.get(URL+poduct_to_search, headers = headers).text
     soup = BeautifulSoup(source, "lxml")
     list_products = soup.find_all("li", class_="product-list__item")

     if show_product_to_search:
          if(len(list_products) == 0):
               print(">> FOUND NO PRODUCTS!")
               with open("testing_log_NETTO.html", "w", encoding = "UTF-8") as file:
                    file.write(soup.prettify())
                    print(">> soup saved in testin_log_NETTO.html")
          else:
               with open("testing_log_NETTO.html", "w", encoding = "UTF-8") as file:
                    file.write(list_products[0].prettify())
                    print("li class='product-list__item' saved in testing_log_NETTO.html")
          
          print("Found products:", len(list_products))
     

     for product in list_products:
          try:
               # TITLE
               try:
                    title = product.find("div", class_="product__title").text.strip()
               except:
                    continue

               # PRICE
               found_base_price = False
               try:
                    price= product.find("span", class_="product-property__base-price").text.strip()
                    found_base_price = True
               except:
                    found_base_price  = False

               if found_base_price == False:
                    price= product.find("span", class_="product__current-price--digits-before-comma").text.strip()
               
               # SHOP LINK
               try:
                    original_link = product.find("a", class_ = "product").get("href")
               except:
                    original_link = ""
               
               # IMAGE URL
               try:
                    image = product.find("img", class_ = "product__image")
                    imageURL = image.get("data-src")
               except:
                    imageURL = ""

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
