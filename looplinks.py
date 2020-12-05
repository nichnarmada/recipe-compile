#Scrape all recipe links in website

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re



def getLinks(url):
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page, features="lxml")

    invalid_href = ("#", "")
    links_html = soup.findAll("a", href=True)
    unref_links = [link.attrs for link in links_html if link["href"] not in invalid_href]
    new_links = []
    
    for dicts in unref_links:
        #remove dictionary key if value doesn't contain /recipes/
        dicts.items()
        for val in list(dicts.values()):
            if "/recipes/" in val:
                new_links.append(val)


        # for key in dicts:
            # for value in dicts[key]:
                # if re.search(r"/recipes", value) is not None:
                    # return value
    

        #check if output has .instructions from recipe-scrapers
        #if output has instructions, keep
        #if output doesn't, save to a diff list and we gonna webcrawl in there again

    new_links = list(dict.fromkeys(new_links))

    return new_links


print(getLinks("https://www.bettycrocker.com/recipes"))










# <li class="gridItem">
#             <a data-bind="click: $root.navigateToContent, attr: { 'href': Link.Url, 'target': Link.Target }" href="/recipes/2020-home-for-the-holidays-sugar-cookie-cutouts/69c2c7a7-b683-4b57-8460-6c8aff7cd983" target="_self">
#                 <div class="singleTapTarget">
#                     <div class="gridImage">
#                         <picture>
#                             <source data-bind="attr: {'srcset': $root.hasTwoColSmClass() ? StandardImages.SmallImageUrl : StandardImages.ThumbnailImageUrl, 'media': $root.MediaQuerySmall}" srcset="//images-gmi-pmc.edge-generalmills.com/eb704268-66cb-43d1-806c-bc457f2e3a93.jpg" media="(min-width : 300px) and (max-width : 500px)">
#                             <source data-bind="attr: {'srcset': StandardImages.LargeImageUrl, 'media': $root.MediaQueryMedium}" srcset="//images-gmi-pmc.edge-generalmills.com/c140e7d4-e932-4aa5-a542-0fb9f4a52924.jpg" media="(min-width : 501px) and (max-width : 1000px)">
#                             <source data-bind="attr: {'srcset': StandardImages.MediumImageUrl, 'media': $root.MediaQueryLarge}" srcset="//images-gmi-pmc.edge-generalmills.com/fc3e7ab8-fe6d-46ad-89ce-0e67f1a8e090.jpg" media="(min-width : 1001px)">
#                             <img data-bind="attr: {'src': StandardImages.ThumbnailImageUrl, 'alt': Title }" src="//images-gmi-pmc.edge-generalmills.com/2ac2e863-c7a4-4bc6-80b8-e7145c2fe01c.jpg" alt="2020 Home for the Holidays Sugar Cookie Cutouts">
#                         </picture>
#                         <!-- ko if: $root.favorites.hasRegistration() -->
#                         <!-- ko if: $root.settings().FavoriteTemplateName --><!-- /ko -->
#                         <!-- /ko -->
#                     </div>
#                     <div class="gridInfo">
#                         <!-- ko if: $root.settings().ShowContentTypeLabel -->
#                         <div data-bind="attr: { 'class': 'RecordTypePropertyView undecorated ' }, text: ContentType" class="RecordTypePropertyView undecorated ">Recipe</div>
#                         <!-- /ko -->
#                         <h4>
#                             <span class="titleLink" data-bind="'text': Title">2020 Home for the Holidays Sugar Cookie Cutouts</span>
#                         </h4>
#                         <div class="ratings undecorated" data-bind="foreach: { data: InfoProperties }">
#                             <!-- ko if: $data.Template === 'RatingPropertyView' --><!-- /ko -->
                        
#                             <!-- ko if: $data.Template === 'RatingPropertyView' --><!-- /ko -->
                        
#                             <!-- ko if: $data.Template === 'RatingPropertyView' -->
#                             <p data-bind="template: { 'name': 'RatingPropertyView', 'templateUrl': $root.templateUrl + '/PandoSites', 'templateSuffix': $root.templateSuffix, 'data': $data }"><div data-bind="attr: { 'class': Template }, delegatedHandler: 'click'" class="RatingPropertyView">
#     <span data-bind="attr: { 'title': AdditionalInfo.RatingDescription, 'class': AdditionalInfo.RatingCssClassName }" title="0 stars" class="stars star-0"></span>    


# import requests

# sample_page = requests.get("https://www.marionskitchen.com/chicken-egg-donburi/")
# sample_page.content


# from bs4 import BeautifulSoup

# soup = BeautifulSoup(sample_page.content, "html.parser")

# #Title of dish is in:
# # <div class="penci-recipe-heading">
# # <div class="penci-recipe-metades">

# #Ingredient list is in:
# # <div class="penci-recipe-ingredients penci-recipe-ingre-visual">

# #Each ingredients are in:
# # <p itemprop="recipeIngredient">
# # <span data-contrast="auto"></span>

# #Servings are in:
# # <span class="servings" itemprop="recipeYield">



# #Name of dish
# dishname_soup = soup.find(class_="penci-recipe-metades")
# title_tag = dishname_soup.contents[0]
# dishname = title_tag.contents[0]

# #Number of Servings
# servings_soup = soup.find(itemprop = "recipeYield")
# servings = servings_soup.contents[0]

# #Ingredient list
# ingredients_soup = soup.find_all("p", itemprop="recipeIngredient")
# ingredients = []

