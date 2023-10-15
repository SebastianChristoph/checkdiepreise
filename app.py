from flask import Flask, request, render_template, url_for, redirect
import requests
import json
import os
import datetime

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    # redirect from blog-entry-submit
    if request.method == "POST":
        title = request.form['title'] 
        category = request.form['category'] 
        text1 = request.form['text1'] 
        text2 = request.form['text2'] 
        today = datetime.date.today()
        date = today.strftime("%d.%m.%Y")
        icon = request.form['icon'] 

        new_post =  {
        "title": title,
        "category": category,
        "text_header": text1,
        "text_readmore": text2,
        "date": date, 
        "fontawesome_icon": icon
        }

        cwd = os.getcwd()
        if "home" in cwd:
            #flask path
            print("RUNNING IN FLASK")
            path_to_blog_json = "/home/SebastianChristoph/mysite/static/blog/blog.json"
         

            with open(path_to_blog_json, "r", encoding = "UTF-8") as json_file:
                blog = json.load(json_file)
                blog["content"].insert(0, new_post)
        
            with open(path_to_blog_json, "w") as outfile:
                json.dump(blog, outfile)

        else:
            # local path
            print("RUNNING LOCALLY")
            path_to_blog_json = os.path.join(current_directory, "static\\blog", "blog.json")
          
          
            with open(path_to_blog_json, "r", encoding = "UTF-8") as json_file:
                blog = json.load(json_file)
                blog["content"].insert(0, new_post)
    
            with open(path_to_blog_json, "w") as outfile:
                json.dump(blog, outfile)

        return redirect(url_for('home'))
    else:
        current_directory = os.getcwd()
        cwd = os.getcwd()
      
        if "home" in cwd:
            #flask path
            print("RUNNING IN FLASK")
            path_to_blog_json = "/home/SebastianChristoph/mysite/static/blog/blog.json"
            path_to_info_json = "/home/SebastianChristoph/mysite/static/crawler/info.json"
            with open(path_to_blog_json, encoding = "UTF-8") as json_file:
                context = json.load(json_file)
        else:
            # local path
            print("RUNNING LOCALLY")
            path_to_blog_json = os.path.join(current_directory, "static\\blog", "blog.json")
            path_to_info_json = os.path.join(cwd, "crawler", "info.json")
       
     
        with open(path_to_info_json, "r", encoding="UTF-8") as json_info_file:
            context_info = json.load(json_info_file)
        
        with open(path_to_blog_json, encoding = "UTF-8") as json_file:
                context = json.load(json_file)

        return render_template("start.html", context = context, context_info = context_info)

@app.route("/blogentry", methods = ["GET", "POST"])
def blogentry():
    if request.method == "POST":
        pw = request.form['pw'] 
        if pw =="ADMINPASSWORDHERE":

            cwd = os.getcwd()
            log_string = "LOCAL, no log"
            if "home" in cwd:
                with open("/home/SebastianChristoph/mysite/static/crawler/testing_log.txt", "r", encoding = "UTF-8") as file:
                    log_string = file.read()
            return render_template("blogentry.html", log_string = log_string)
 
    return redirect(url_for('home'))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/tableviewaux")
def tableviewaux():
    return render_template("tableviewaux.html")

# @app.route("/tableview/",methods = ['POST', 'GET'])
# def tableview():
#     if request.method == "POST":
#         search = request.form['searchProduct'] 
#         print(search)
#     else:
#         search = request.args.get('search')

#     labels = ""
#     categories = []
#     stores = ["Kaufland", "Hellweg", "Netto", "Mueller", "Rossmann"]
#     filter_category = request.args.get('filterby')
#     store = request.args.get('store')
#     selected_product = request.args.get('selectedProduct')    
#     context = {}
#     cwd = os.getcwd()

#     if "home" in cwd:
#         #flask path
#         print("RUNNING IN FLASK")
#         store_json = "/home/SebastianChristoph/mysite/static/crawler/"+store.upper()+".json"
#         with open(store_json, encoding = "UTF-8") as json_file:
#             context = json.load(json_file)
        
#     else:
#         # local path
#         print("RUNNING LOCALLY")
#         store_json = store.upper()+".json"
#         json_url_local = os.path.join(cwd, "crawler", store_json)

#         with open(json_url_local) as json_file:
#                 context = json.load(json_file)

   
#     # Create x-datumLabels
#     for key, value in context["products"][0]["dates"].items():
#         labels += str(key) + ","
    
#     # Create categories
#     for product in context["products"]:
#         if product["category"] not in categories:
#             categories.append(product["category"])

#     # sort list
#     sorted_products = sorted(context["products"], key=lambda x: x["name"])

#     # refresh sorted dict
#     context["products"] = sorted_products
    
#     labelsTable = labels.split(",")[:-1]
#     context["labelsTable"] = labelsTable
#     context["labels"] = labels
#     context["categories"] = categories
#     context["filter"] = filter_category
#     context["stores"] = stores
#     context["selectedProduct"] = selected_product

#     print(search)
#     context["search"] = search
#     print( context["search"])
   
#     selected_product_data = ""
#     selectedProductImageURL = ""

#     # get selected product data
#     for product in context["products"]:
#         if product["name"] == selected_product:
#             print(product["name"])
#             selectedProductImageURL = product.get("image")
#             for key, value in product["dates"].items():
#                 selected_product_data += str(value) + ","
                

#     context["selectedProductData"] = selected_product_data
#     context["selectedProductImageURL"] = selectedProductImageURL

#     return render_template("tableview.html", context=context)


@app.route("/tableview_new/",methods = ['POST', 'GET'])
def tableview_new():
   
    labels = ""
    categories = []
    stores = ["Kaufland", "Hellweg", "Netto", "Mueller", "Rossmann"]
    filter_category = request.args.get('filterby')
    store = request.args.get('store')
    selected_product = request.args.get('selectedProduct')    
    context = {}
    cwd = os.getcwd()

    if "home" in cwd:
        #flask path
        print("RUNNING IN FLASK")
        store_json = "/home/SebastianChristoph/mysite/static/crawler/"+store.upper()+".json"
        with open(store_json, encoding = "UTF-8") as json_file:
            context = json.load(json_file)
        
    else:
        # local path
        print("RUNNING LOCALLY")
        store_json = store.upper()+".json"
        json_url_local = os.path.join(cwd, "crawler", store_json)

        with open(json_url_local) as json_file:
                context = json.load(json_file)

   
    # Create x-datumLabels
    for key, value in context["products"][0]["dates"].items():
        labels += str(key) + ","
    
    # Create categories
    for product in context["products"]:
        if product["category"] not in categories:
            categories.append(product["category"])

    # sort list
    sorted_products = sorted(context["products"], key=lambda x: x["name"])

    # refresh sorted dict
    context["products"] = sorted_products
    
    labelsTable = labels.split(",")[:-1]
    context["labelsTable"] = labelsTable
    context["labels"] = labels
    context["categories"] = categories
    context["filter"] = filter_category
    context["stores"] = stores
    context["selectedProduct"] = selected_product
 
    selected_product_data = ""
    selectedProductImageURL = ""

    # get selected product data
    for product in context["products"]:
        if product["name"] == selected_product:
            print(product["name"])
            selectedProductImageURL = product.get("image")
            for key, value in product["dates"].items():
                selected_product_data += str(value) + ","
                

    context["selectedProductData"] = selected_product_data
    context["selectedProductImageURL"] = selectedProductImageURL

    print(context["stores"])
    return render_template("tableview_new.html", context=context)



@app.route("/hilfe")
def hilfe():
    return render_template("hilfe.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/preisunterschiede")
def preisunterschiede():
    cwd = os.getcwd()
    if "home" in cwd:
        #flask path
        print("RUNNING IN FLASK")
        json_url_local = "/home/SebastianChristoph/mysite/static/crawler/info.json"
    
    else:
        # local path
        print("RUNNING LOCALLY")
        json_url_local = os.path.join(cwd, "crawler", "info.json")
       
    with open(json_url_local) as json_file:
        context = json.load(json_file)
    
    return render_template("data_overview.html", context = context)

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")


cwd = os.getcwd()
if "home" not in cwd:
    if __name__ == '__main__':
        app.run(debug=True)
