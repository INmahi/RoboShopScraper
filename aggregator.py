from scrapers.scrapeSites import roboShopScraper#, primeABGBScraper, mdComputersScraper
#handle bangladeshi/american....
def aggregate_products(query: str,region:str):
    if region == "BD":
        # Handle Bangladeshi region specific scraping
        products = []
        products.extend(roboShopScraper(query))
        # products.extend(primeABGBScraper(query))
        # products.extend(mdComputersScraper(query))
        return products
    elif region == "US":
        # Handle American region specific scraping
        products = []
        products.extend(roboShopScraper(query))
        # products.extend(primeABGBScraper(query))
        # products.extend(mdComputersScraper(query))
        return products
    elif region == "ALL":
        # Handle global scraping
        products = []
        products.extend(roboShopScraper(query))
        # products.extend(primeABGBScraper(query))
        # products.extend(mdComputersScraper(query))
        return products
    else:
        raise ValueError("Unsupported region. Please use 'BD', 'US', or 'ALL'.")

