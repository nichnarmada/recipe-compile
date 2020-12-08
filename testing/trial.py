#Web Scrape recipe

import requests

sample_page = requests.get("https://www.marionskitchen.com/chicken-egg-donburi/")
sample_page.content


from bs4 import BeautifulSoup

soup = BeautifulSoup(sample_page.content, "html.parser")

#Title of dish is in:
# <div class="penci-recipe-heading">
# <div class="penci-recipe-metades">

#Ingredient list is in:
# <div class="penci-recipe-ingredients penci-recipe-ingre-visual">

#Each ingredients are in:
# <p itemprop="recipeIngredient">
# <span data-contrast="auto"></span>

#Servings are in:
# <span class="servings" itemprop="recipeYield">



#Name of dish
dishname_soup = soup.find(class_="penci-recipe-metades")
title_tag = dishname_soup.contents[0]
dishname = title_tag.contents[0]

#Number of Servings
servings_soup = soup.find(itemprop = "recipeYield")
servings = servings_soup.contents[0]

#Ingredient list
ingredients_soup = soup.find_all("p", itemprop="recipeIngredient")
ingredients = []

for ingre_tags in ingredients_soup:
    try:
        ingredients.append(ingre_tags.contents[0].contents[0])
    except AttributeError:
        ingredients.append(ingre_tags.contents[0])
    else:
        continue


#Split ingredients based on qty, unit and ingredient name
# Use regex to split them up



# convert to dictionary to format of chicken = {"quantity": 200, "unit": g}




#




# class Recipes:
#     """
#     Attributes of a Recipe below
#     """
#     def __init__(self, name, servings, ingredients):
#         self.name = name
#         self.servings = servings
#         self.ingredients = ingredients
    

# recipe = Recipes(dishname, servings, ingredients)
# print(recipe.name)
# print(recipe.servings)
# print(recipe.ingredients)

#Transfer all info to JSON file

import json

class Recipe:
    def __init__(self):
        self.name="abc name"
        self.servings="abc first"
        self.ingredients=Ingre()
    def reprJSON(self):
        return dict(name=self.name, servings=self.servings, ingredients=self.ingredients) 

class Ingre:
    def __init__(self):
        self.quantity="sesame street"
        self.unit="13000"
    def reprJSON(self):
        return dict(quantity=self.quantity, unit=self.unit)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

doc=Recipe()
print("Str representation")
print(doc.reprJSON())
print("Full JSON")
print(json.dumps(doc.reprJSON(), cls=ComplexEncoder))
print("Partial JSON")
print(json.dumps(doc.identity.addr.reprJSON(), cls=ComplexEncoder))

recipe.ingredients

#Split ingredients to qty and unit

