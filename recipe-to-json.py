from recipe_scrapers import scrape_me
scraper = scrape_me('https://www.bettycrocker.com/recipes/ultimate-chocolate-chip-cookies/77c14e03-d8b0-4844-846d-f19304f61c57', wild_mode=True)
# if no error is raised - there's schema available:
title = scraper.title()
time = scraper.total_time()
servings = scraper.yields()
ingredients = scraper.ingredients()
instructions = scraper.instructions()
scraper.image()



#Regex ingredients, split to: qty, unit, ingredient, how to cut
#Loop through all ingredients
# print(ingredients)

# class Ingredients:
#     def __init__(self, quantity, unit, cut):
#         self.quantity = quantity
#         self.unit = unit
#         self.cut = cut
    
#     def reprJSON(self):
#         return dict(quantity=self.quantity, unit=self.unit)



#want to save it in class under ingredient name, thus need to make a loop per every ingredient


#split numbers
# return tuple of (qty, remaining string)
import re

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

from inflector import English
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
ingre: '5 tbsp unsalted butter, divided'

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


#sorting out ingredients to their stuff
ingre_dict = {}

for ingre in ingredients:
    quantity = qty_split(ingre)
    unit = unit_split(ingre)
    cut = cut_split(ingre)
    ingre_name = ingre_name_split(ingre, quantity, unit, cut)

    ingre_dict[ingre_name] = [quantity, unit, cut]

# print(ingredients)
# print(ingre_dict)

#Transform to JSON format

import json



# out_file = open("myfile.json", "w")
# json_object = json.dumps(ingre_dict, out_file, indent = 4)
# print(json_object)

# title
# time
# servings

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
        # if hasattr(obj,'reprJSON'):
        #     return obj.reprJSON()
        # else:
        #     return json.JSONEncoder.default(self, obj)

recipe = Recipe(title, time, servings, ingre_dict, instructions)

print(json.dumps(recipe.reprJSON(), cls=ComplexEncoder))

with open("sample.json", "w") as outfile: 
    json.dump(recipe.reprJSON(), outfile, cls=ComplexEncoder, indent = 4)