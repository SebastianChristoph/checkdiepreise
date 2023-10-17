from PIL import Image, ImageDraw, ImageFont
import os
import requests
import json
from io import BytesIO

def cut_text(input_string):
    words_per_chunk = 9
    words = input_string.split()
    parts = []

    for i in range(0, len(words), words_per_chunk):
        part = ' '.join(words[i:i + words_per_chunk])
        parts.append(part)

    return parts

def get_info_json():
    cwd = os.getcwd()
      
    if "home" in cwd:
        path_to_info_json = "/home/SebastianChristoph/mysite/static/crawler/info.json"
    else:
        path_to_info_json = os.path.join(cwd, "crawler", "info.json")

    return path_to_info_json

def merge_product_image(background, product_image_url,  x):
    max_width = 180
    max_height = 180
    # Lade das Overlay-Bild aus dem Internet herunter
    overlay_response = requests.get(product_image_url)
    overlay_image = Image.open(BytesIO(overlay_response.content))
    overlay_image = overlay_image.convert("RGBA")
    overlay_image.thumbnail((max_width, max_height), Image.BICUBIC)
    background.paste(overlay_image, (x, 290))
    
def draw_text(image, text, position, text_color=(0,0,0), font=None, font_size = 15):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'crawler\Arial.ttf', font_size)  
    draw.text(position, text, fill=text_color, font=font)

def insert_logo(background, store, x):
    cwd = os.getcwd()
    if "home" in cwd:
        path_to_logos = "/home/SebastianChristoph/mysite/static/crawler/storelogos/"
    else:
        path_to_logos = "crawler\\storelogos\\"

    logomapper = {
        "Kaufland" : path_to_logos + "kaufland.png",
        "Hellweg" : path_to_logos + "hellweg.png",
        "Biocompany" :  path_to_logos + "biocompany.png",
        "Mueller" :  path_to_logos + "mueller.png",
        "Netto" :  path_to_logos + "netto.png",
        "Rossmann" :  path_to_logos + "rossmann.png",
        "Globus" :  path_to_logos + "globus.png"
        
    }

    logo_image = Image.open(logomapper[store])
    logo_image = logo_image.convert("RGB")

    max_width = 100
    max_height = 100
    logo_image.thumbnail((max_width, max_height), Image.BICUBIC)
    background.paste(logo_image, (x, 200))

def draw_gewinner(price_today, price_yesterday, change_rel, change_abs, product_name, imageURL, store):
    # LOGO STORE
    insert_logo(background_image, store, 100)

    # PRODUCT IMAGE
    merge_product_image(background_image, imageURL, 200)

    product_list = cut_text(product_name)
    for i in range(0, len(product_list)):
        y = 230 + (i*20)
        draw_text(background_image, product_list[i], (100,y), font_size = 15)
    

    draw_text(background_image, str(price_yesterday) + "€", (110, 560), font_size=30)
    draw_text(background_image, str(price_today) + "€", (390, 560), font_size=30)
    draw_text(background_image, str(change_abs) + "€", (270, 550), font_size=20, text_color=(65,161,34))
    draw_text(background_image, str(change_rel) + "%", (270, 580), font_size=20, text_color=(65,161,34))

def draw_verlierer(price_today, price_yesterday, change_rel, change_abs, product_name, imageURL, store):
    logo_image = Image.open("crawler\\storelogos\\kaufland.png")
    logo_image = logo_image.convert("RGB")
    insert_logo(background_image, store, 720)

    # PRODUCT IMAGE
    merge_product_image(background_image,imageURL, 850)

    product_list = cut_text(product_name)
    for i in range(0, len(product_list)):
        y = 230 + (i*20)
        draw_text(background_image, product_list[i], (720,y), font_size = 15)
    

    draw_text(background_image, str(price_yesterday) + "€", (730, 560), font_size=30)
    draw_text(background_image, str(price_today) + "€", (990, 560), font_size=30)
    draw_text(background_image, "+" + str(change_abs) + "€", (880, 550), font_size=20, text_color=(224,90,47))
    draw_text(background_image, "+" + str(change_rel) + "%",  (880, 580), font_size=20, text_color=(224,90,47))

def save_image():
    cwd = os.getcwd()
    if "home" in cwd:
        path_to_save = "/home/SebastianChristoph/mysite/static/crawler/today.png"
    else:
        path_to_save = "crawler/today.png"

    background_image.save(path_to_save)


background_image = Image.open("crawler\\template.png")
background_image = background_image.convert("RGB")

#GET INFO.JSON
path_to_json = get_info_json()
with open(path_to_json, "r", encoding="UTF-8") as file:
    infodict= json.load(file)

draw_gewinner(infodict["max_down_product"]["price_today"], infodict["max_down_product"]["price_yesterday"], infodict["max_down_product"]["price_change_percentage"], infodict["max_down_product"]["price_change"], infodict["max_down_product"]["product_name"], infodict["max_down_product"]["imageURL"], infodict["max_down_product"]["store"])

draw_verlierer(infodict["max_up_product"]["price_today"], infodict["max_up_product"]["price_yesterday"], infodict["max_up_product"]["price_change_percentage"], infodict["max_up_product"]["price_change"], infodict["max_up_product"]["product_name"], infodict["max_up_product"]["imageURL"], infodict["max_up_product"]["store"])

save_image()


