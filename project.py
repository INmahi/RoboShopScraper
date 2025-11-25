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


def main():
    cfg = load_user_config()
    if not cfg:
        return []
       
    products = aggregator.aggregate_products(cfg)
 
    return products


if __name__ == "__main__":
    main()