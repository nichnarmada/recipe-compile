from requests_html import HTMLSession
session = HTMLSession()
baseURL = session.get("https://www.bettycrocker.com/recipes")

#make a program to get all the categories in each category using webscrapers somehow
categories = {
    "main": ["main-ingredient", "global-cuisine", "dishes", "special-occasions", "preparation", "health-and-diet", "courses", "product-recipes"],
    "main-ingredient": ["chicken-recipes", "beef-recipes", "apple-recipes", "pork-recipes", "turkey-recipes", "bean-and-legume-recipes", "vegetable-recipes", "fruit-recipes"], 
    "global-cuisine": [], 
    "dishes": [], 
    "special-occasions": [], 
    "preparation": [], 
    "health-and-diet": [], 
    "courses": [], 
    "product-recipes": []
}







# from requests_html import HTMLSession
# session = HTMLSession()
# #he got baseURL based on the hackernews website when he clicks on a category
# baseURL = 'https://thehackernews.com/search/label/'
# #thus the name of the category is based on link
# categories = ['data%20breach', 'Cyber%20Attack', 'Vulnerability', 'Malware']


# class CategoryScrape():
#     #catURL is baseURL + category name, which is the address to access the category page
#     catURL = ''
#     r = ''

#     def __init__(self, catURL, category):
#         print(f'Scraping starting on Category : {category} \n')
#         print(' ')

#         self.catURL = catURL
#         self.r = session.get(self.catURL)

#     def scrapeArticle(self):

#         #both links and title are within class called body-post, thus .body-post was used
#         blog_posts = self.r.html.find('.body-post')

#         for blog in blog_posts:
#             #links have class story-link
#             storyLink = blog.find('.story-link', first=True).attrs['href']
#             #titles have class home-title
#             storyTitle = blog.find('.home-title', first=True).text

#             print(storyTitle)
#             print(storyLink)
#             print("\n")


# for category in categories:
#     #first, gets session of the catURL
#     #combines the catURL into one string here
#     category = CategoryScrape(f'{baseURL}{category}', category)
#     #next, scrapes the article
#     category.scrapeArticle()

