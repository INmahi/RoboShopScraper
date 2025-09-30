#scrapers for each site returns a list of product dicts with title, price, desc, link, img link
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
query = "arduino uno"
page = 1
all_articles = []
all_titles = []

for i in range (1,3):
    url = f"https://store.roboticsbd.com/search?controller=search&s={query.replace(' ','+')}&page={i}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article")
    if not articles:  # stop when no products returned
        break
    titles = [article.find("h3",class_="product-title").get_text() for article in articles]
    all_titles.extend(titles)
    all_articles.extend(articles)
    print(f"Page {i}: {len(articles)} products found")

print(f"Total products scraped: {len(all_articles)}")



def search_filter(card_list,txt):
    final_list = []
    for card in card_list:
        title = card.find('h3',class_='product-title').get_text(strip = True).lower()

        if all(word.lower() in title for word in txt.split()):
            final_list.append(card)
    
    return len(final_list)


print(search_filter(all_articles,"arduino Uno"))

#get a page..loop through first 2/3 pages....get the product articles...filter out titles not containing the search terms...