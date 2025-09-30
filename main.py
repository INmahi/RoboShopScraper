import json
import os
from datetime import datetime

def load_user_config():
    """Load user configuration from Streamlit app"""
    config_file = "user_config.json"
    
    if not os.path.exists(config_file):
        print("❌ No configuration found!")
        print("💡 Please run the Streamlit app first and click 'Let's Go!'")
        print("   Command: streamlit run app.py")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print("✅ Configuration loaded successfully!")
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def display_config(config):
    """Display the loaded configuration"""
    print("\n" + "="*50)
    print("📋 USER CONFIGURATION")
    print("="*50)
    print(f"🔍 Search Text: {config.get('search_text', 'N/A')}")
    print(f"💰 Price Range: ৳{config['price_range']['min']:,} - ৳{config['price_range']['max']:,}")
    print(f"🌍 Region: {config.get('region', 'N/A')}")
    print(f"🌐 Selected Websites:")
    for i, site in enumerate(config.get('selected_websites', []), 1):
        print(f"   {i}. {site}")
    print(f"📸 Include Images: {config.get('include_images', False)}")
    print(f"🤖 AI Mode: {config.get('ai_mode', False)}")
    if config.get('ai_mode') and config.get('ai_suggestions'):
        print(f"💭 AI Suggestions: {config['ai_suggestions']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    display_config(load_user_config())
