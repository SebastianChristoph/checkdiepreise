import requests
import json

headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

SHOW_PRINT = False
def get_category(id):

    try:
        URL = f"https://api.cloud.kaufland.de/pdp-frontend/v1.1/{id}/mrv/"
        s = requests.Session()
        s.headers = headers
        source = s.get(URL, headers = headers).text
        responsedict = json.loads(source)

        return responsedict["product"]["breadcrumb"][1]["title"]
    
    except:
        return "Divers"

def get_correct_unit_price(eingabe):
    
    price = str(eingabe)
    if SHOW_PRINT:
        print(price + " >>", end = "")
    teile = price.split(".")

    # kein Punkt
    if len(teile) == 1:
        teil_vor_punkt = teile[0][0:-2]
        teil_nach_punkt = teile[0][-3:-1]
        price_cleaned = teil_vor_punkt+"."+teil_nach_punkt
        if SHOW_PRINT:
            print(price_cleaned)
        return price_cleaned
    elif len(teile) == 2:
        teil_vor_punkt = teile[0][0:-2]
        teil_nach_punkt = teile[0][-3:-1]
        price_cleaned = teil_vor_punkt+"."+teil_nach_punkt
        if SHOW_PRINT:
            print(price_cleaned)
        return price_cleaned
    else:
        return price  
    

def fetch(searchterm, max_page_iteration):
    list_of_found_products = []
    page = 1
    searching = True
    while searching:
        try:    
            print(page)
            URL = f"https://api.cloud.kaufland.de/search/v5/results/?requestType=load&page={page}&pageType=search&searchValue={searchterm}&useNewEngine=false&deviceType=desktop&loadType=pagination"
            s = requests.Session()
            s.headers = headers
            source = s.get(URL, headers = headers).text
            responsedict = json.loads(source)

        
            for product in responsedict["products"]:
                try:

                    try:
                        link =  "https://www.kaufland.de"  + product["link"]["url"]
                    except:
                        print("ERROR, weil: no link")
                        link = ""

                    #PRICE
                    try:
                        if product.get("price") != None:
                            if product["price"]["units"] != None:
                                price = product["price"]["units"][0]["price"]
                                price = get_correct_unit_price(price)
                                unit = product["price"]["units"][0]["unit"]

                                if float(price) > 2500:
                                    price = product["unit"]["price"]
                                    unit = "Stk"

                            else:
                                price = product["unit"]["price"]
                                unit = "Stk"
                        else:
                            price = product["unit"]["price"]
                            unit = "Stk"
                    except Exception as e:
                        print("ERROR, weil: no price  / unit; ERROR:")
                        print(e)
                        print("product_dict:")
                        print(product)
                        print("*********************")
                        continue

                    try:
                        id =   product["id"]
                    except:
                        print("ERROR, weil: no id")
                        continue
                    
                    try:
                        imageURL =  product["images"][0]["variants"][0]["url"]
                    except:
                        print("ERROR, weil: no imageurl")
                        imageURL = ""
                    
                    try:
                        if product["manufacturer"] != None:
                            name =  product["manufacturer"]["title"] + " - " +product["title"]
                        else:
                            name = product["title"]
                    except:

                        print("ERROR, weil: no name")
                        print("product dict:")
                        print(product)
                        return


                    product_dict = {
                        "id": id,
                        "imageURL" : imageURL,
                        "name" :    name,
                        "unit" : unit,
                        "price" : price,
                        "category" : get_category(product["id"]),
                        "original_link" : link
                    }

                    list_of_found_products.append(product_dict)
        
                except Exception as e:
                    print("ERROR:", e)
                    break

            if page < max_page_iteration:
                 page += 1
            else:
                searching = False

        except:
            print("Not working for page", page)
            searching= False
       
    return list_of_found_products
