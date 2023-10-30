import requests
import json

categories = {}
current = 0
list_found_products = []
def fix_encoding_error(input_string):
    # Ersetze das nicht brechbare Leerzeichen (U+00A0) durch ein normales Leerzeichen
    corrected_string = input_string.replace('\xa0', ' ')
    return corrected_string

def collect():
    global list_found_products, current

    for search_term in categories:
        print("Getting products for", search_term, "[", current, "of", len(categories), "]")
        category = search_term.split(" ")[0]
        collecting = True
        page = 0
        while collecting:
            url = f"https://api.os.fressnapf.com//rest/v2/fressnapfDE/products/search?fields=DEFAULT&query={search_term}&sort=relevance&currentPage={page}&pageSize=100&lang=de"
            try:
                response = requests.get(url)
                response_dict = json.loads(response.text)

                if len(response_dict["products"]) == 0:
                    collecting = False
                    break

                # with open("example_response_fressnapf.json", "w", encoding="UTF-8") as file:
                #     json.dump(response_dict, file)
                # return
            
                for product in response_dict["products"]:

                    # name
                    name = product["fullName"]

                    #id
                    id = product["code"]

                    #price
                    price = product["pricing"]["current"]["value"]

                    #baseprice
                    if product["pricing"].get("perUnit") != None:
                        baseprice = product["pricing"]["perUnit"]["value"]
                        unit = product["pricing"]["perUnit"]["formattedValue"].replace('\xa0', ' ')
                        if "/" in unit:
                            unit = unit.split("/")[-1]
                    else:
                        baseprice = price
                        unit = "Stk"
            
                    # imageURL
                    imageURL = product["images"][0]["url"]

                    # original_link
                    original_link = "https://www.fressnapf.de" + product["url"]

                    new_product = {
                        "name" : name,
                        "imageURL" : imageURL,
                        "category" : category,
                        "original_link" : original_link,
                        "id" : id, 
                        "unit" : unit,
                        "price" : price,
                        "baseprice" : baseprice
                    }

                    if new_product not in list_found_products:
                        list_found_products.append(new_product)
                #print(len(list_found_products))
                page +=1
                
            except Exception as e:
                print("nope", e)
                collecting = False

        current += 1
    print(len(list_found_products))
  
def get_categories():
    global categories
    fressnap_categories = {
        "Hund" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/hund/&lang=de",

        "Katze" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/katze/&lang=de",

        "Kleintier" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/kleintier/&lang=de",

        "Vogel" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/vogel/&lang=de",

        "Aqua" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/aqua/&lang=de",

        "Terra" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/terra/&lang=de",

        "Garten-Teich" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/garten-teich/&lang=de",

        "Tiergesundheit" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/vet-diaeten/&lang=de"
    }

    #"Tiergesundheit" : "https://api.os.fressnapf.com//rest/v2/fressnapfDE/cms/wordpress/pages?fields=DEFAULT&url=%2Fc/vet-diaeten/&lang=de"

    print("Getting sub categories for")

    for category in fressnap_categories:
        print("...", category)
        response = requests.get(fressnap_categories[category])
        response_dict = json.loads(response.text)
        content = json.loads(response_dict["content"])

        if category == "Tiergesundheit":
            for cat in content["content_slots"]["a"]["sections"]:
                try:
                    for test in cat["grid"]["items"][0]["components"][0]["data"]["items"]:
                       
                        if "hund" in test["link"]["url"]:
                            main_cat = "Hund"
                        else:
                            main_cat = "Katze"
                    
                        subcategory = category + " " + main_cat + " " + test["title"]
                        subcategory_url = test["link"]["url"]
                        categories[subcategory] = {"url" : subcategory_url, "main_category" : category}

                    for test in cat["grid"]["items"][1]["components"][0]["data"]["items"]:
                        if "hund" in test["link"]["url"]:
                            main_cat = "Hund"
                        else:
                            main_cat = "Katze"
    
                        subcategory = category + " " + main_cat + " " + test["title"]
                        subcategory_url = test["link"]["url"]
                        categories[subcategory] = {"url" : subcategory_url, "main_category" : category}
        
                except:
                    continue       
        else:

            for cat in content["content_slots"]["a"]["sections"][0]["grid"]["items"][0]["components"][0]["data"]["slides"]:
                subcategory = category + " " + cat["link"]["title"]
                subcategory_url = cat["link"]["url"]
                categories[subcategory] = {"url" : subcategory_url, "main_category" : category}
 
def get_products_from_shop():
    get_categories()
    collect()

    return list_found_products

# with open("fressnapf.json", "w", encoding="UTF-8") as file:
#     json.dump(content, file)
# print("Done")
