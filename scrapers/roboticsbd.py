
import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0"}

def scraper(user):
    # fresh containers each invocation
    products = []
    seen = set()
    query = user["search_text"]
    price_min = user.get("price_min", 0)
    price_max = user.get("price_max", 10**4)
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
            
            if all(word.lower() in title for word in query.split()):
                similar_text_list.append(card)
        print(len(similar_text_list), " after text filtering")

        final_list = []
        for card in similar_text_list:
            price_raw = card.find('span',class_='price')
            if not price_raw:
                continue
            price_txt = price_raw.get_text(strip = True)
            cleaned = price_txt.replace('\xa0',' ').replace('BDT','').replace(',','').strip()
            digits = ''.join(ch for ch in cleaned if ch.isdigit())
            if not digits:
                continue
            price_val = int(digits)
            if price_min <= price_val <= price_max:
                final_list.append(card)
        print(len(final_list), " after price filtering")
        # print(len(final_list), " after filtering")
        for article in final_list:
            product={}

            title = article.find("h3",class_="product-title").get_text()
            pLink = article.find("a").get("href")
            price = article.find("span",class_="price").get_text(strip = True).replace('\xa0',' ').replace(",","")
            product = {
                "title": title,
                "link": pLink,
                "price": price
            }

            if user["include_img"]:

                img = article.find("img").get("src")
                product["image"] = img

            log_str = product["title"] + " | " + product["price"]
            
            if log_str not in seen:
                seen.add(log_str)
                products.append(product)



    # print(products)


    return products

if __name__ == "__main__":
    scraper({"search_text":"arduino uno","include_img":True})