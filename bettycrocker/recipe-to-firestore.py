#external libraries
from recipe_scrapers import scrape_me
import re
from inflector import English
import json
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db

#modules from main file


#loop through all links from json file
# Opening JSON file 
f = open('bettycrocker.json',)

# returns JSON object as  
# a dictionary 
data = json.load(f) 



#Regex ingredients, split to: qty, unit, ingredient, how to cut
#Loop through all ingredients

#split numbers
def qty_split(ingre):

    # Contains a fraction
    if re.search(r"\d", ingre) is not None:
        if re.search(r"(\d+)/(\d+)", ingre) is not None:
            if re.search(r"^(\d+)(?=\s)", ingre) is not None:
                #change fraction to decimal
                result_fraction = re.search(r"(\d+)/(\d+)", ingre)
                deci_value = int(result_fraction.group(1))/int(result_fraction.group(2))
                
                #add decimal to value
                results_int = re.search(r"^(\d+)(?!/)", ingre)
                final_value = float(results_int.group(1)) + float(deci_value)

                return final_value
            
            else: 
                #change fraction to decimal
                result_fraction = re.search(r"(\d)/(\d)", ingre)
                deci_value = int(result_fraction.group(1))/int(result_fraction.group(2))
                
                return float(deci_value)

        # Contains a decimal
        elif re.search(r"(\d+.\d+)(?=\s)", ingre) is not None:
            result_decimal = re.search(r"(\d+).(\d+)(?=\s)", ingre)
            return float(result_decimal.group(1) + "." + result_decimal.group(2))

        # Just an integer
        else:
            results_int = re.search(r"^(\d+)", ingre)
            return int(results_int.group(1))
    
    else:
        return None


#split units
# singularize all units

#list of units:
unit_short = ["tbsp", "tsp", "oz", "ml", "l", "g", "kg", "lb"]
unit_full = ["tablespoon", "teaspoon", "cup", "ounce", "millilitre", "litre", "gram", "kilogram", "clove", "pound", "link"]


eng_noun = English()

def unit_split(ingre):
    #long forms
    for unit in unit_full:
        if re.search(rf"\b{eng_noun.singularize(unit)}\b", ingre) or re.search(rf"\b{eng_noun.pluralize(unit)}\b", ingre) is not None:
            return unit.strip()

    #short forms
    for unit in unit_short:
        if re.search(rf"\b{unit}\b", ingre) is not None:
            return unit.strip()


#split how to cut
def cut_split(ingre):
    if re.search(r",", ingre) is not None:
        cut_way = re.search(r",(\D+)", ingre)
        return cut_way.group(1).strip()


#get ingredient name

def ingre_name_split(ingre, quantity, unit, cut):
    word_list = ["to"]
    
    word_list.append(str(quantity))
    word_list.append(unit)
    if unit is not None: 
        word_list.append(unit + "s")
    word_list.append(cut)
    ingrewords = ingre.split(",")
    ingrewords[0] = ingrewords[0].split()

    temp = []
    for word in ingrewords[0]:
        if (not ( word in word_list or "/" in word)) and word.isalpha():
            temp.append(word)
    ingre_name = ' '.join(temp)

    # name_results = [word for word in ingrewords[0] if word.lower() not in word_list]
    # ingre_name = ' '.join(name_results)

    return ingre_name


#Transform to Dictionary/JSON format

class Recipe:
    def __init__(self, title, time, servings, ingredients, instructions):
        self.title = title
        self.time = time
        self.servings = servings
        self.ingredients = ingredients
        self.instructions = instructions
    
    def reprJSON(self):
        return dict(name=self.title, servings=self.servings, ingredients=self.ingredients, instructions=self.instructions) 

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):                     # pylint: disable=E0202
        return obj.__dict__  

#Optional Json file output function
def to_Json(recipe):
    with open(f"{recipe.title}.json", "w") as outfile: 
        json.dump(recipe.reprJSON(), outfile, cls=ComplexEncoder, indent = 4)

#upload dictionary to firebase
cred = credentials.Certificate('../foodstuff-be28b-firebase-adminsdk-2pi9a-0be2b43333.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://foodstuff-be28b.firebaseio.com/'
})


# Iterating through the json 
# list 
for link in data[472:10000]: 
    scraper = scrape_me(link, wild_mode=True)

    title = scraper.title()
    time = scraper.total_time()
    servings = scraper.yields()
    ingredients = scraper.ingredients()
    instructions = scraper.instructions()
    scraper.image()


    #sorting out ingredients to their stuff
    ingre_dict = {}

    for ingre in ingredients:
        try: 
            quantity = qty_split(ingre)
            unit = unit_split(ingre)
            cut = cut_split(ingre)
            ingre_name = ingre_name_split(ingre, quantity, unit, cut)

            ingre_dict[ingre_name] = {"quantity": quantity, "unit": unit, "cut": cut}
        except Exception:
            pass
    

    recipe = Recipe(title, time, servings, ingre_dict, instructions)

    db = firestore.client()

    #Import Data
    # print(vars(recipe))
    try:
        db.collection(u'recipesites').document(u'bettycrocker').collection(u'recipes').document(recipe.title).set(vars(recipe))
    except Exception:
        pass
    else:
        print(f"Successfully uploaded {recipe.title}")

# Closing file 
f.close()