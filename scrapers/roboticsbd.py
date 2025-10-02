
import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0"}
query = "arduino uno"
page = 1
products = []


def scraper(user):

    for i in range (1,3):
        url = f"https://store.roboticsbd.com/search?controller=search&s={query.replace(' ','+')}&page={i}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("article")
        # print(len(articles)," products found")

        if not articles:  # stop when no products returned
            break

        similar_text_list = []
        for card in articles:
            title = card.find('h3',class_='product-title').get_text(strip = True).lower()
            
            if all(word.lower() in title for word in user["search_text"].split()):
                similar_text_list.append(card)
        print(len(similar_text_list), " after text filtering")

        final_list = []
        for card in similar_text_list:

            price = card.find('span',class_='price').get_text(strip = True).replace(",","").replace("BDT ","")
            price_val = int(price) if price.isdigit() else 0
            if user["price_min"] <=price_val <= user["price_max"]:
                print( price_val, " in range")
                final_list.append(card)
        print(len(final_list), " after price filtering")
        # print(len(final_list), " after filtering")
        for article in final_list:
            product={}

            title = article.find("h3",class_="product-title").get_text()
            pLink = article.find("a").get("href")
            price = article.find("span",class_="price").get_text(strip = True).replace("BDT&nbsp;","BDT ").replace(",","")
            product = {
                "title": title,
                "link": pLink,
                "price": price
            }
            if user["include_img"]:

                img = article.find("img").get("src")
                product["image"] = img
            
            products.append(product)

        

    # print(products)


    return products

if __name__ == "__main__":
    scraper({"search_text":"arduino uno","include_img":True})