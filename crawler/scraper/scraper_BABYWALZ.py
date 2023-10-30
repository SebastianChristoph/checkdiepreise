
from bs4 import BeautifulSoup
import requests
import json

categories = {}
list_found_products = []
used_ids = []
current = 1

SHOW_PRINT = True

def get_categories():
    global categories
    print("Get categories")
    url = "https://www.baby-walz.de"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    category_wrappers = soup.find_all("a", class_ = "bw-menu__sub-item--header-single__link")

    for category_wrapper in category_wrappers:
        categories[category_wrapper.text.strip()] = "https://www.baby-walz.de" + category_wrapper.get("href")


def collect(url, categoryname):
    global current, categories, list_found_products, used_ids
    print("Get products for category:", categoryname, "[", current, "of", len(categories), "]")
    print(url)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        list_products = soup.find_all("div", class_ ="bw-category-column")
        # products_max = soup.find("span", class_ = "bw-items-amount").text.replace("(", "").replace(")", "").replace("Artikel", "").strip()

        pages_pagination = soup.find_all("a", class_="bw-pagination__element")
        last_page = int(pages_pagination[-1].text.strip())
    except:
        return

    for page in range(1, last_page):
        if SHOW_PRINT:
            print("... page", page, "of", last_page)

        try:
            url_page = f"{url}?pageNumber={page}"
            print("...", url_page)
            response = requests.get(url_page)
            soup = BeautifulSoup(response.text, "lxml")
            list_products = soup.find_all("div", class_ ="bw-category-column")

            # with open("example_response_babywalz.html", "w", encoding="UTF-8") as file:
            #     file.write(soup.prettify())
            #     print("Done")
            #     return

            for product_wrapper in list_products:
                try:
                    # name
                    brand = product_wrapper.find("div", class_ = "bw-product__brand").text.strip()
                    subbrand =  product_wrapper.find("div", class_ = "bw-product__subbrand").text.strip()
                    title =  product_wrapper.find("div", class_ = "bw-product__name").text.strip()

                    name = brand + " " + subbrand + " " + title

                    # print(name)

                    # id
                    id =  product_wrapper.find("div", class_ = "bw-product__fav-icon-wrapper").get("data-attr-artikelerp")

                    # print(id)


                    # imageURL

                    imageURL = ""
                    try:
                        imageURL_wrapper = product_wrapper.find("img")
                        imageURL = "https:" + imageURL_wrapper.get("data-original")
                    except:    
                        imageURL_wrapper = product_wrapper.find("img")
                        imageURL = "https:" + imageURL_wrapper.get("src")

                    # print(imageURL)

                    # category

                    #original_link

                    original_link = product_wrapper.find("a").get("href")
                    # print(original_link)

                    #price
                    try:
                        price = product_wrapper.find("div", class_ = "bw-product__price--promotion").text.strip()

                    except:
                        price =  product_wrapper.find("div", class_ = "bw-product__price").text.strip()
                    

                    #baseprice

                    unit = "Stk."
                    try:
                        baseprice = product_wrapper.find("div", class_ = "bw-product__price-base").text.strip()

                        if "=" in baseprice:
                            #1 Meter = 6,50 €
                            #1 Kilogramm = 22,71 €
                            #1 Liter = 5,99 €
                            baseprice_split = baseprice.split("=")
                            baseprice = baseprice_split[-1].replace("€", "").strip()
                            unit = baseprice_split[0].strip()
                        else:
                            baseprice = price
                    except:
                        baseprice = price


                    # print(price)
                    # print("******************")

                    new_product = {
                                "name" : name,
                                "imageURL" : imageURL,
                                "category" : categoryname,
                                "original_link" : original_link,
                                "id" : id,
                                "unit" : unit,
                                "price" : price,
                                "baseprice" : baseprice
                            }

                    if id not in used_ids:
                        list_found_products.append(new_product)
                        used_ids.append(id)

                except Exception as e:
                    if SHOW_PRINT:
                        print("... Fehler beim Anlegen dict:", e)
                    
                    continue
        except:
            continue

def get_products_from_shop():
    global current
    get_categories()

    for category in categories:
        collect(categories[category], category)
        current += 1
    return list_found_products