import json
import os
from datetime import datetime

def load_user_config():
    """Load user configuration from Streamlit app"""
    config_file = "user_config.json"
    
    if not os.path.exists(config_file):
        print("❌ Something went wrong!")
        print("💡 might be a missing configuration file")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print("✅ Configuration loaded successfully!")

        user_search_text = config.get("search_text")
        user_price_min = config.get("price_range", {}).get("min")
        user_price_max = config.get("price_range", {}).get("max")
        user_region = config.get("region")
        user_include_img = config.get("include_images")
        user_ai_mode = config.get("ai_mode")
        user_components = config.get("ai_suggestions")
        
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None


if __name__ == "__main__":
    load_user_config()