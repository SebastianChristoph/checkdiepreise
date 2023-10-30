import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

found_products_list = []

def getting_articles_from_shop(searchterm, page): 
    collecting = True
    while collecting:
        URL2 =  f"https://product-search.services.dmtech.com/de/search?query={searchterm}&searchType=product&currentPage={page}&type=search"
        s = requests.Session()
        s.headers = headers
        
        try:
            source = s.get(URL2, headers = headers).text
            response_dict = json.loads(source)

            print("...found", len(response_dict["products"]), "products")
            
            for product in response_dict["products"]:

                try:

                    #price

                    price = product["priceLocalized"].replace("€", "").strip()


                    # base price
                    if product.get("basePrice") != None:
                        baseprice = product["basePrice"]["formattedValue"]
                    else:
                        baseprice = product["priceLocalized"]

                    # unit
                    if product.get("basePriceUnit") != None:
                        unit = product["basePriceUnit"]
                    else:
                        unit = "Stk"
                except:
                    
                    print("******************")
                    print(product)
                    print("*************************")
                    print("error getting price")
                    continue

                try:
                    # image
                    if product.get("imageUrlTemplates") != None:
                        imageURL = product["imageUrlTemplates"][0].replace("{transformations", "")
                        imageURL = imageURL.replace("}/", "")
                except:
                    imageURL = ""
                    print("error getting img")
                
                if product.get("categoryNames") != None:
                    category = product["categoryNames"][0]
                else:
                    category = "Sonstiges"
                    
               
                new_dictionary = {
                    "name" : product["brandName"] + " - " + product["title"],
                    "price" : price,
                    "baseprice": baseprice,
                    "unit" : unit,
                    "category" : category,
                    "original_link" : "https://www.dm.de" + product["relativeProductUrl"],
                    "imageURL" : imageURL,
                    "id" : product["gtin"]
                }
                found_products_list.append(new_dictionary)
            collecting = False
         
        except Exception as e:
            collecting = False
            print("*******************************************************")
            print(source)
            print("error", e)
            print("*******************************************************")
            
    return found_products_list
