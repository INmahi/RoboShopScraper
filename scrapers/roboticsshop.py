import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
products = []
seen = set()

def scraper(user):
    query = user["search_text"]
    for i in range (1,3):
        url = f"https://www.roboticsshop.com.bd/products?name={query.replace(' ','+')}&data_from=search&page={i}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("div", class_="product")
        # print(len(articles)," products found")

        if not articles:  # stop when no products returned
            break

        similar_text_list = []
        for card in articles:
            title = card.find('div',class_='product__thumbnail').find('img').get('alt').lower()
            
            if all(word.lower() in title for word in query.split()):
                similar_text_list.append(card)

        final_list = []
        for card in similar_text_list:

            price = card.find('ins', class_='product__new-price').get_text(strip=True).replace(",","").replace("৳","")
            # print( price, " price")
            price_val = int(price) if price.isdigit() else 0
            # print( price_val, " price_val")
            if user["price_min"] <= price_val <= user["price_max"]:
                # print( price_val, " in range")
                final_list.append(card)
        # print(len(final_list), " after price filtering")
        # print(len(final_list), " after filtering")
        for article in final_list:
            product={}

            title = article.find('div',class_='product__thumbnail').find('img').get('alt')
            pLink = article.find('h6',class_='product__title').find('a').get('href')
            price = article.find('ins', class_='product__new-price').get_text(strip=True).replace(",","").replace("৳","BDT ")
            product = {
                "title": title,
                "link": pLink,
                "price": price
            }

            if user["include_img"]:

                img = article.find('div',class_='product__thumbnail').find('img').get('src')

                product["image"] = img

            log_str = product["title"] + " | " + product["price"]
            
            if log_str not in seen:
                seen.add(log_str)
                products.append(product)



    # print(products)


    return products

if __name__ == "__main__":
    scraper()
