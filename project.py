import json
import os
from datetime import datetime
import aggregator

def build_user(file):
    """create the user choice json"""
    try:
        with open(file, 'r') as f:
            config = json.load(f)

        user = {
            "search_text" : config.get("search_text"),
            "price_min" : config.get("price_range", {}).get("min"),
            "price_max" : config.get("price_range", {}).get("max"),
            "region" : config.get("region"),
            "include_img" : config.get("include_images"),
            "ai_mode" : config.get("ai_mode"),
            "components" : config.get("ai_suggestions"),
            "selected_websites": config.get("selected_websites"),
        }
        return user
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def load_user_config():
    """Load user configuration from Streamlit app"""
    config_file = "user_config.json"
    
    if not os.path.exists(config_file):
        print("❌ Something went wrong!")
        print("💡 might be a missing configuration file")
        return None

    return build_user(config_file)


#cs50 
def filter_products_by_price(products, min_price=0, max_price=float('inf')):
    """
    Filter products based on price range.
    
    Args:
        products (list): List of product dictionaries
        min_price (int): Minimum price threshold (default: 0)
        max_price (int/float): Maximum price threshold (default: infinity)
    
    Returns:
        list: Filtered products within the price range
    """
    if not products:
        return []
    
    if min_price < 0:
        min_price = 0
    
    if max_price < min_price:
        return []
    
    filtered_products = []
    
    for product in products:
        # Extract numeric price from product
        price_str = product.get('price', '')
        if not price_str or price_str == "Price N/A":
            continue
        
        # Extract digits from price string (e.g., "BDT 995" -> 995)
        import re
        digits = re.findall(r'\d+', str(price_str))
        if not digits:
            continue
        
        try:
            numeric_price = int(''.join(digits))
            
            # Check if price falls within range
            if min_price <= numeric_price <= max_price:
                # Add numeric_price to product for future use
                product['numeric_price'] = numeric_price
                filtered_products.append(product)
        except (ValueError, TypeError):
            # Skip products with invalid price formats
            continue
    
    return filtered_products

def main():

    cfg = load_user_config()
    if not cfg:
        return []      
    products = aggregator.aggregate_products(cfg)
    
    # Apply price filtering if specified
    if cfg.get('price_min') is not None or cfg.get('price_max') is not None:
        min_price = cfg.get('price_min', 0)
        max_price = cfg.get('price_max', float('inf'))
        products = filter_products_by_price(products, min_price, max_price)
    
    return products

if __name__ == "__main__":
    main()