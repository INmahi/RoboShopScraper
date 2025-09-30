from scrapers.scrapeSites import roboShopScraper#, primeABGBScraper, mdComputersScraper
#handle bangladeshi/american....
def aggregate_products(query: str):
    products = []
    products.extend(roboShopScraper(query))
    # products.extend(primeABGBScraper(query))
    # products.extend(mdComputersScraper(query))
    return products
