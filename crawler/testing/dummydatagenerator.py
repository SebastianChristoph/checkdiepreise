import random
import string
import json

STORENAME = "BigStore"
DAYS = 4
RISING = True
#max 60
AMOUNT_PRODUCTS = 10

#max 60
product_names = [
    "ZappoChips",
    "CrunchyMunchies",
    "BerryBurst Cereal",
    "CheezyDelights",
    "FrostedFlakey Pops",
    "CreamyDream Yogurt",
    "ChocoFusion Bars",
    "FreshSqueeze Juice",
    "VeggieBlast Snacks",
    "SparklingQuench Soda",
    "GourmetDelite Pasta",
    "FarmFresh Eggs",
    "MeatyMarvel Sausages",
    "RiceHarvest Medley",
    "SweetTreat Cookies",
    "Sizzlin'Grill Sauce",
    "NuttyNectar Granola",
    "TastyTwist Pretzels",
    "SavorySpice Mix",
    "FruitFiesta Sorbet",
    "WholesomeHarbor Bread",
    "YummoNoodle Soup",
    "SmoothieBliss Mix",
    "GourmetGarden Dressing",
    "CrispyCrunch Crackers",
    "ChocoCherry Delights",
    "ZestyZing Salsa",
    "FreshPicked Apples",
    "HoneyGrove Cereal",
    "CoolCrisp Pickles",
      "FruitFusion Sparkle Water",
    "GoldenGrove Honey Nut Clusters",
    "ChocoCharm Marshmallow Bites",
    "SavorySurgeon Sausage Links",
    "MochaMountain Coffee Beans",
    "CrispCoastal Seaweed Snacks",
    "SpicySunrise Hot Sauce",
    "GreenHarvest Quinoa Pilaf",
    "CreamyCanyon Almond Milk",
    "CinnamonTwist Swirl Bread",
    "TropicalTreat Fruit Cups",
    "FlavorFiesta Tortilla Chips",
    "YogurtYacht Parfait Cups",
    "HarvestHaven Veggie Mix",
    "ChocolateCascade Pancake Mix",
    "SilkSmoothie Fruit Blends",
    "ZestyZephyr Popcorn",
    "MapleMeadow Syrup",
    "NoodleNirvana Ramen Bowls",
    "CherryBurst Energy Bars",
    "SunnySideUp Omelette Mix",
    "CrispyCove Croutons",
    "HeartyHarbor Soup Mix",
    "FreshFields Green Beans",
    "TropicTwirl Sorbet",
    "ChocoCraze Chocolate Spread",
    "PepperParade Salad Dressing",
    "SodaSensation Variety Pack",
    "ProteinPower Bites",
    "CheddarCharm Cheese Balls",
    "RainbowDelight Ice Cream"
]

categories = ["Obst", "Gemüse", "Wohnen", "Tiere"]

units = ["Stk", "pro kg", "L", " ", "m²"]


store_json = {
    "name" : STORENAME,
    "via": "Dummy", 
    "products" : [],
    "historical_labels" : []
}

def generate_historical_labels():
    global DAYS, store_json
    for i in range(1, DAYS+1):
        store_json["hisorical_labels"].append(f"{i}-01-2023")
    
def generate_id():
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(10))
    return random_id

def generate_data_for_product():
    global RISING, categories, product_names
    for i in range(0, AMOUNT_PRODUCTS):

        new_product = {
            "id" : generate_id(),
            "name" : product_names[i],
            "unit" : random.choice(units),
            "imageURL" : "www.",
            "category" :random.choice(categories),
            "original_link" : "www.",
            "dates" : {}
        }

        # dates data
        
        if RISING:
            price = 1
        else: 
            price = 100

        for date in store_json["hisorical_labels"]:
            new_product["dates"][date] = str(price)

            price_random = round(random.uniform(0.1, 2.0), 2)
            if RISING:
                price = round(price + price_random ,2)
            else:
                price = round(price - price_random, 2)
        store_json["products"].append(new_product)



def generate():
    generate_historical_labels()
    generate_data_for_product()

    with open("bigStore.json" , "w" , encoding = "UTF-8") as file:
         json.dump(store_json, file)


generate()
print("Done, saved in JSON")