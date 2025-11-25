import pytest
import json
import os
import tempfile
from project import build_user, load_user_config, filter_products_by_price
import aggregator

def test_build_user():
    """Test build_user function with valid config file"""
    # Create a temporary config file
    config_data = {
        "search_text": "arduino",
        "price_range": {"min": 100, "max": 1000},
        "region": "Bangladeshi",
        "include_images": True,
        "ai_mode": False,
        "ai_suggestions": [],
        "selected_websites": ["roboticsshop.com.bd"]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_file = f.name
    
    try:
        result = build_user(temp_file)
        
        assert result is not None
        assert result["search_text"] == "arduino"
        assert result["price_min"] == 100
        assert result["price_max"] == 1000
        assert result["region"] == "Bangladeshi"
        assert result["include_img"] == True
        assert result["selected_websites"] == ["roboticsshop.com.bd"]
    finally:
        os.unlink(temp_file)

def test_load_user_config():
    """Test load_user_config function"""
    # Create a temporary user_config.json file
    config_data = {
        "search_text": "raspberry pi",
        "price_range": {"min": 50, "max": 500},
        "region": "American",
        "include_images": False,
        "ai_mode": True,
        "ai_suggestions": ["sensor", "module"],
        "selected_websites": ["store.roboticsbd.com"]
    }
    
    # Save original config if it exists
    original_config = None
    if os.path.exists("user_config.json"):
        with open("user_config.json", 'r') as f:
            original_config = json.load(f)
    
    try:
        # Create test config file
        with open("user_config.json", 'w') as f:
            json.dump(config_data, f)
        
        # Test the function
        result = load_user_config()
        
        assert result is not None
        assert result["search_text"] == "raspberry pi"
        assert result["price_min"] == 50
        assert result["price_max"] == 500
        assert result["region"] == "American"
        assert result["include_img"] == False
        assert result["ai_mode"] == True
        assert result["components"] == ["sensor", "module"]
        assert result["selected_websites"] == ["store.roboticsbd.com"]
        
    finally:
        # Restore original config or remove test file
        if original_config:
            with open("user_config.json", 'w') as f:
                json.dump(original_config, f)
        elif os.path.exists("user_config.json"):
            os.remove("user_config.json")

def test_filter_products_by_price():
    products = [
        {"title": "Product A", "price": 150},
        {"title": "Product B", "price": 300},
        {"title": "Product C", "price": 450},
        {"title": "Product D", "price": 600},
    ]
    
    # Test filtering with valid range
    filtered = filter_products_by_price(products, min_price=200, max_price=500)
    assert len(filtered) == 2
    assert all(200 <= p["price"] <= 500 for p in filtered)
    
    # Test filtering with no products in range
    filtered = filter_products_by_price(products, min_price=700, max_price=800)
    assert len(filtered) == 0
    
    # Test filtering with negative min price
    filtered = filter_products_by_price(products, min_price=-100, max_price=400)
    assert len(filtered) == 3
    assert all(p["price"] <= 400 for p in filtered)
    
    # Test filtering with max price less than min price
    filtered = filter_products_by_price(products, min_price=500, max_price=400)
    assert len(filtered) == 0
