import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import hashlib
from recipe_scrapers import scrape_me
import json


#getting all links from a website
# Pass the headers you want to retrieve from the xml such as ["loc", "lastmod"]
def parse_sitemap(url, headers):
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if (200 != resp.status_code):
        return False

    # BeautifulSoup to parse the document
    soup = Soup(resp.content, "xml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')
    sitemaps = soup.findAll('sitemap')
    new_list = ["Source"] + headers
    panda_out_total = pd.DataFrame([], columns=new_list)


    if not urls and not sitemaps:
        return False

    # Recursive call to the the function if sitemap contains sitemaps
    if sitemaps:
        for u in sitemaps:
            sitemap_url = u.find('loc').string
            panda_recursive = parse_sitemap(sitemap_url, headers)
            panda_out_total = pd.concat([panda_out_total, panda_recursive], ignore_index=True)

    # storage for later...
    out = []

    # Creates a hash of the parent sitemap
    hash_sitemap = hashlib.md5(str(url).encode('utf-8')).hexdigest()

    # Extract the keys we want
    for u in urls:
        values = [hash_sitemap]
        for head in headers:
            loc = None
            loc = u.find(head)
            if not loc:
                loc = "None"
            else:
                loc = loc.string
            values.append(loc)
        out.append(values)
    
    # Creates a dataframe
    panda_out = pd.DataFrame(out, columns= new_list)

    # If recursive then merge recursive dataframe
    if not panda_out_total.empty:
        panda_out = pd.concat([panda_out, panda_out_total], ignore_index=True)

    #returns the dataframe
    return panda_out


df = parse_sitemap("https://www.bettycrocker.com/sitemap.xml", ["loc"])

df = df.drop(columns="Source")

categories = ["main-ingredient", "global-cuisine", "dishes", "special-occasions", "preparation", "health-and-diet", "courses", "product-recipes", "bestof"]

#remove links without /recipes/
for ind in df.index:
    if "https://www.bettycrocker.com/recipes/" not in df['loc'][ind]:
        df.drop([ind], inplace = True)

#remove links that contains /recipes/categories/
df = df[df["loc"].str.contains('|'.join(categories))==False]

print(df)

#remove broken links (not sure if needed)

# for ind in df.index:
#     try:
#         # print(f"Trying ind number {ind}")
#         requests.get(df['loc'][ind])
#         # response = requests.get(df['loc'][ind])
#         # print("URL is valid and exists on the internet")
#     except Exception as exception:
#         df.drop([ind], inplace = True)
#         print(ind)
#         print(exception)


#make condition to check if its a recipe or not (not sure if needed)

def is_Recipe(dataframe):
    for ind in dataframe.index:
        scraper = scrape_me(dataframe['loc'][ind], wild_mode=True)
        # title = scraper.title()
        # time = scraper.total_time()
        # servings = scraper.yields()
        ingredients = scraper.ingredients()
        # instructions = scraper.instructions()
        # scraper.image()

        if not ingredients:
            dataframe.drop([ind], inplace = True)
        else:
            continue
    
    return dataframe


#put all links in a json file
result = df["loc"].to_json(orient="values")
parsed = json.loads(result)
# json.dumps(parsed, indent=4)

with open("bettycrocker.json", "w") as outfile: 
    json.dump(parsed, outfile, indent = 4)
