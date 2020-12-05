import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import hashlib
from recipe_scrapers import scrape_me
import sys
from urllib.parse import urlparse
from urllib.parse import urljoin





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

for ind in df.index:
    if "/recipes" not in df['loc'][ind]:
        df.drop([ind])

#remove broken links

# for ind in df.index:
#     try:
#         requests.get(df['loc'][ind])
#         # response = requests.get(df['loc'][ind])
#         # print("URL is valid and exists on the internet")
#     except requests.ConnectionError as exception:
#         df.drop([ind])

# print(df['loc'][0])



searched_links = []
broken_links = []

def getLinksFromHTML(html):
    def getLink(el):
        return el["href"]
    return list(map(getLink, Soup(html, features="html.parser").select("a[href]")))

def find_broken_links(domainToSearch, URL, parentURL):
    if (not (URL in searched_links)) and (not URL.startswith("mailto:")) and (not ("javascript:" in URL)) and (not URL.endswith(".png")) and (not URL.endswith(".jpg")) and (not URL.endswith(".jpeg")):
        try:
            requestObj = requests.get(URL)
            searched_links.append(URL)
            if(requestObj.status_code == 404):
                broken_links.append("BROKEN: link " + URL + " from " + parentURL)
                print(broken_links[-1])
            else:
                print("NOT BROKEN: link " + URL + " from " + parentURL)
                if urlparse(URL).netloc == domainToSearch:
                    for link in getLinksFromHTML(requestObj.text):
                        find_broken_links(domainToSearch, urljoin(URL, link), URL)
        except Exception as e:
            print("ERROR: " + str(e))
            searched_links.append(domainToSearch)

find_broken_links(urlparse(sys.argv[1]).netloc, sys.argv[1], "")

print("\n--- DONE! ---\n")
print("The following links were broken:")

for link in broken_links:
    print ("\t" + link)







#make condition to check if its a recipe or not

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
            dataframe.drop([ind])
        else:
            continue
    
    return dataframe

# df = is_Recipe(df)
# print(df)