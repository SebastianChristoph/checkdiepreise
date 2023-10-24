
from bs4 import BeautifulSoup
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}


URLS_COLLECTION = []
found_products = []

def get_ikeas_categories():
    url = "https://www.ikea.com/de/de/cat/produkte-products/"
    cat_list = []
    s = requests.Session()
    s.headers = headers
    source = s.get(url, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    listen = soup.find_all("a", class_ = "vn-link vn-nav__link")
    for cat in listen:
        cat_list.append(cat.get("href"))

    return cat_list

def get_ikea_sub_categories(url):
    global URLS_COLLECTION

    sub_cat_list = []
    s = requests.Session()
    s.headers = headers
    source = s.get(url, headers = headers).text
    soup = BeautifulSoup(source, "lxml")

    sub_cat_wrappers = soup.find_all("a", class_="vn-8-grid-gap")

    for sub_cat_wrapper in sub_cat_wrappers:
        sub_link = sub_cat_wrapper.get("href")
        if sub_link not in sub_cat_list:
            sub_cat_list.append(sub_link)

    return sub_cat_list

def add_products_from_category_page(url, page_iteration_limit = 10):
    global URLS_COLLECTION
    page = 8
    url_to_check = url + f"?page={page}"
    
    #print("     normal page")
    try:
        s = requests.Session()
        s.headers = headers
        source = s.get(url_to_check, headers = headers).text
        soup = BeautifulSoup(source, "lxml")
        product_wrappers = soup.find_all("div", class_ = "plp-fragment-wrapper")

        for product_wrapper in product_wrappers:
            product_info = product_wrapper.find("div", class_= "pip-product-compact")
            link = product_info.find("a").get("href")
            if link not in URLS_COLLECTION:
                URLS_COLLECTION.append(link)          
    except:
        print("Error in PT1")
    
    url_to_check = url + "?sort=PRICE_LOW_TO_HIGH"
    #print("     PRICE_LOW_TO_HIGH")
    try:
        s = requests.Session()
        s.headers = headers
        source = s.get(url_to_check, headers = headers).text
        soup = BeautifulSoup(source, "lxml")
        product_wrappers = soup.find_all("div", class_ = "plp-fragment-wrapper")

        for product_wrapper in product_wrappers:
            product_info = product_wrapper.find("div", class_= "pip-product-compact")
            link = product_info.find("a").get("href")
            if link not in URLS_COLLECTION:
                URLS_COLLECTION.append(link)          
    except:
        print("error")

    #print("     MOST_POPULAR")
    url_to_check = url + "?sort=MOST_POPULAR"
    try:
        s = requests.Session()
        s.headers = headers
        source = s.get(url_to_check, headers = headers).text
        soup = BeautifulSoup(source, "lxml")
        product_wrappers = soup.find_all("div", class_ = "plp-fragment-wrapper")

        for product_wrapper in product_wrappers:
            product_info = product_wrapper.find("div", class_= "pip-product-compact")
            link = product_info.find("a").get("href")
            if link not in URLS_COLLECTION:
                URLS_COLLECTION.append(link)          
    except:
        print("error")

      
def get_product_info(url):
    global temp_list
    try:
        s = requests.Session()
        s.headers = headers
        source = s.get(url, headers = headers).text
        soup = BeautifulSoup(source, "lxml")


        utag_data_script = soup.find('script', {'data-type': 'utag-data'})
        javascript_code = utag_data_script.string
        start = javascript_code.find('var utag_data = ') + len('var utag_data = ')
        end = javascript_code.find(';', start)
        utag_data_json = javascript_code[start:end]
        utag_data = json.loads(utag_data_json+"}")

        meta_wrappers = soup.find_all("meta")

        # TITLE
        title = meta_wrappers[-7].get("content")

        # IMAGE
        imageURL = meta_wrappers[-5].get("content")

        # ORIGINAL_LINK
        original_link = meta_wrappers[-4].get("content")

        # id 
        id = utag_data["product_ids"][0]

        # price
        price = utag_data["price"][0]

        unit = "Artikel"

        # CATEGORY
        category_wrapper = soup.find("div", class_ = "bc-breadcrumb")
        category_list = category_wrapper.find_all("li", class_="bc-breadcrumb__list-item")
        category = category_list[1].text.strip()

        new_dict = {
            "id" : id,
            "unit" : unit,
            "price" : price, 
            "category" : category,
            "imageURL" : imageURL,
            "original_link" : original_link,
            "name" : title

        }

        found_products.append(new_dict)
        
    except:
        print("no product infos possible")


def get_products_from_shop():

    # GET MAIN CATGEORIES URLS
    print("Getting main categories")
    ikea_main_cat_urls = get_ikeas_categories()

    # GET SUB CATGEORIES URLS
    ikea_sub_cat_urls = []
    
    for i in range(0, len(ikea_main_cat_urls)):
        print("Getting sub categories", i, " of ", len(ikea_main_cat_urls))
        sub_category_urls = get_ikea_sub_categories(ikea_main_cat_urls[i])
        for sub_category_url in sub_category_urls:
            if sub_category_url not in ikea_sub_cat_urls:
                ikea_sub_cat_urls.append(sub_category_url)
        
    print("Done")

  
    # ITERATE OVER MAIN CATGEORIES
    print("Iterate over main categories")
    for i in range(0,len(ikea_main_cat_urls)):
        print(i, "/", len(ikea_main_cat_urls) )
        add_products_from_category_page(ikea_main_cat_urls[i])
    
    # ITERATE OVER SUB CATGEORIES
    print("Iterate over sub categories")
    for i in range(0,len(ikea_sub_cat_urls)):
        print(i, "/", len(ikea_sub_cat_urls))
        add_products_from_category_page(ikea_sub_cat_urls[i])

    print("********************************")
    print(len(URLS_COLLECTION))

    for i in range(0, len(URLS_COLLECTION)):
        print("Getting information for product", i, "of", len(URLS_COLLECTION))
        get_product_info(URLS_COLLECTION[i])
    
    return found_products







