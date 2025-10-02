from scrapers import roboticsbd, roboticsshop
import main


def aggregate_products(user):
    products = []
    for website in user['selected_websites']:
        if 'store.roboticsbd.com' in website:
            products.extend(roboticsbd.scraper(user))
        elif 'roboticsshop.com.bd' in website:
            products.extend(roboticsshop.scraper(user))
        # elif 'mdcomputers' in website:
        #     products.extend(mdComputersScraper(user))
        else:
            print(f"❌ No scraper available for {website}")

    return products




if __name__ == "__main__":
    print(aggregate_products(main.load_user_config()))
    
