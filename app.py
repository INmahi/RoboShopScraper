import streamlit as st
import json
import os
from scrapers.sites import sites

# Cart management functions
def load_cart():
    """Load cart data from JSON file"""
    try:
        if os.path.exists('cart.json'):
            with open('cart.json', 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

def save_cart(cart_data):
    """Save cart data to JSON file"""
    try:
        with open('cart.json', 'w') as f:
            json.dump(cart_data, f, indent=2)
        return True
    except Exception:
        return False

def add_to_cart(product_id, title, price, image_url, link):
    """Add or update product in cart"""
    cart = load_cart()
    
    # Extract numeric price
    import re
    numeric_price = 0
    if price and price != "Price N/A":
        digits = re.findall(r'\d+', str(price))
        numeric_price = int(''.join(digits)) if digits else 0
    
    if product_id in cart:
        # Update existing item
        cart[product_id]['quantity'] += 1
        cart[product_id]['total_price'] = cart[product_id]['quantity'] * numeric_price
    else:
        # Add new item
        cart[product_id] = {
            'title': title,
            'price': price,
            'numeric_price': numeric_price,
            'image_url': image_url,
            'link': link,
            'quantity': 1,
            'total_price': numeric_price
        }
    
    return save_cart(cart)

def get_cart_summary():
    """Get cart summary with total items and price"""
    cart = load_cart()
    total_items = sum(item['quantity'] for item in cart.values())
    total_price = sum(item['total_price'] for item in cart.values())
    return total_items, total_price, cart

def remove_from_cart(product_id):
    """Remove product from cart"""
    cart = load_cart()
    if product_id in cart:
        del cart[product_id]
        return save_cart(cart)
    return False

def update_quantity(product_id, new_quantity):
    """Update product quantity in cart"""
    cart = load_cart()
    if product_id in cart and new_quantity > 0:
        cart[product_id]['quantity'] = new_quantity
        cart[product_id]['total_price'] = cart[product_id]['quantity'] * cart[product_id]['numeric_price']
        return save_cart(cart)
    elif product_id in cart and new_quantity <= 0:
        return remove_from_cart(product_id)
    return False

# Page configuration
st.set_page_config(
    page_title="RoboShop Scraper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with neon cyan/blue colors
st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #1E1E1E;
        border-right: 2px solid #00FFFF;
    }

    /* Main content area */
    .main .block-container {
        background-color: #0E1117;
        padding-top: 2rem;
    }

    /* Headers */
    h1, h2, h3 {
        color: #00FFFF !important;
        font-family: 'Arial', sans-serif;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #262626;
        border: 2px solid #00FFFF;
        color: #FAFAFA;
        border-radius: 8px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #00BFFF;
        box-shadow: 0 0 15px #00BFFF50;
    }

    /* Select boxes */
    .stSelectbox > div > div > div {
        background-color: #262626;
        border: 2px solid #00FFFF;
        color: #FAFAFA;
    }

    /* Checkboxes */
    .stCheckbox > label {
        color: #FAFAFA !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00FFFF, #00BFFF);
        color: #000000;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        box-shadow: 0 0 20px #00FFFF50;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 0 30px #00FFFF80;
        transform: translateY(-2px);
    }

    /* Product Cards - Fixed overflow issues */
    .product-card {
        background: linear-gradient(135deg, #1E1E1E, #2D2D2D);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0 0.25rem 0;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        display: flex;
        flex-direction: column;
        height: 360px;
        overflow: hidden;
        box-sizing: border-box;
        transition: all 0.3s ease;
        position: relative;
    }

    .product-card:hover {
        box-shadow: 0 0 30px rgba(0, 191, 255, 0.4);
        transform: translateY(-3px);
    }

    .product-image {
        flex: 0 0 140px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }

    .product-image img {
        max-width: 100%;
        max-height: 140px;
        object-fit: contain;
        border-radius: 6px;
    }

    .product-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0;
    }

    .product-title {
        font-size: 0.9rem;
        line-height: 1.3;
        margin: 0 0 0.5rem 0;
        word-wrap: break-word;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }

    .product-price {
        font-size: 1rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .product-buttons {
        margin-top: auto;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .visit-button {
        text-decoration: none;
        display: block;
    }

    .visit-button-inner {
        text-align: center;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        transition: all 0.2s ease;
    }

    .domain-badge {
        position: absolute;
        top: 6px;
        right: 6px;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 10px;
        font-weight: 600;
        z-index: 1;
    }

    /* Add to Cart button styling */
    .stButton {
        margin-top: 0.5rem !important;
    }

    /* Cart styles */
    .cart-item {
        background: linear-gradient(135deg, #1E1E1E, #2D2D2D);
        border: 1px solid #00FFFF40;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .cart-item img {
        width: 60px;
        height: 60px;
        object-fit: contain;
        border-radius: 4px;
        border: 1px solid #00FFFF40;
    }

    .cart-summary {
        background: linear-gradient(135deg, #2D2D2D, #1E1E1E);
        border: 2px solid #00FFFF;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }

    .view-cart-btn {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: linear-gradient(45deg, #00FFFF, #00BFFF);
        color: #000;
        padding: 10px 15px;
        border-radius: 25px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        font-weight: bold;
        text-decoration: none;
        font-size: 14px;
        transition: all 0.3s ease;
    }

    .view-cart-btn:hover {
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.8);
        transform: translateY(-2px);
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .product-card {
            height: 320px;
        }
    }
</style>
""", unsafe_allow_html=True)

def display_products(products, config):
    """Display the processed products in a clean layout"""
    if not products:
        st.info("🔍 No products found matching your criteria.")
        return

    st.markdown(f'<h2 style="color: #FA9320;">🛒 Found {len(products)} Products</h2>', unsafe_allow_html=True)

    # Augment products with numeric price for sorting if not present
    for p in products:
        if 'numeric_price' not in p:
            p_price = p.get('price', '')
            # crude extraction of digits
            import re
            digits = re.findall(r'\d+', str(p_price))
            p['numeric_price'] = int(''.join(digits)) if digits else 0

    sort_choice = st.selectbox(
        "Sort / Filter",
        ["Original", "Price: Low to High", "Price: High to Low"],
        index=0,
        help="Choose ordering of the results"
    )

    if sort_choice == "Price: Low to High":
        products = sorted(products, key=lambda x: x.get('numeric_price', 0))
    elif sort_choice == "Price: High to Low":
        products = sorted(products, key=lambda x: x.get('numeric_price', 0), reverse=True)
    # Removed "Only Compatible" filter as AI compatibility feature is disabled

    cols_per_row = 3
    include_images = config.get('include_images', False)

    for i in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(products):
                with cols[j]:
                    create_product_card(products[idx], include_images, idx)
    # end for


def create_product_card(product, include_images: bool, index: int):
    """Create a clean, well-structured product card with proper overflow handling"""
    title = product.get("title", "No Title Available")
    link = product.get("link", "#")
    price = product.get("price") or "Price N/A"
    image_url = product.get("image") if include_images else None
    clean_title = (title[:80] + "...") if len(title) > 80 else title

    from urllib.parse import urlparse
    try:
        domain = urlparse(link).netloc or "unknown"
    except Exception:
        domain = "unknown"
    short_domain = domain.replace('www.', '')

    # Color palette for different domains
    palette = [
        ("#FA9320", "#ffb469"),  # orange
        ("#21A95A", "#45A885"),  # green
        ("#3498DB", "#7FC6FF"),  # blue
        ("#9B59B6", "#D7A8FF"),  # purple
        ("#E74C3C", "#FF9A8F"),  # red
        ("#F1C40F", "#FFE680"),  # yellow
        ("#1ABC9C", "#6EF5DF"),  # teal
    ]
    idx = sum(ord(c) for c in short_domain) % len(palette)
    base_color, light_color = palette[idx]

    # Build image HTML
    image_html = ""
    if include_images:
        if image_url:
            image_html = f'<div class="product-image"><img src="{image_url}" alt="{clean_title}" style="border: 1px solid {base_color}55;" onerror="this.style.display=\'none\'"/></div>'
        else:
            image_html = f'<div class="product-image"><div style="border: 1px dashed {base_color}; color: {base_color}; opacity: 0.7; padding: 2rem; text-align: center; font-size: 12px;">No Image</div></div>'
    
    # Create the complete product card HTML structure
    card_html = f'''
    <div class="product-card" style="border: 2px solid {base_color};">
        <div class="domain-badge" style="background: {base_color}22; border: 1px solid {base_color}; color: {base_color};">🛍️ {short_domain}</div>
        {image_html}
        <div class="product-content">
            <div class="product-title" style="color: {base_color};">📦 {clean_title}</div>
            <div class="product-price" style="color: {base_color};">💰 {price}</div>
            <div class="product-buttons">
                <a href="{link}" target="_blank" rel="noopener" class="visit-button">
                    <div class="visit-button-inner" style="background: linear-gradient(135deg, {base_color}, {light_color}); color: #111;">🔗 Visit</div>
                </a>
            </div>
        </div>
    </div>
    '''
    
    with st.container():
        # Render the complete card structure
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Add to Cart button using Streamlit button (outside the card HTML)
        if st.button("🛒 Add To Cart", key=f"add_to_cart_{index}", help="Add this product to your cart"):
            # Create unique product ID
            product_id = f"{short_domain}_{title.replace(' ', '_')[:30]}_{index}"
            
            # Add to cart
            if add_to_cart(product_id, title, price, image_url or "", link):
                st.success(f"✅ Added '{clean_title}' to cart!")
                st.rerun()  # Refresh to update cart count
            else:
                st.error("❌ Failed to add item to cart")



def display_cart():
    """Display cart contents with management options"""
    st.markdown('<h2 style="color: #00FFFF;">🛒 Shopping Cart</h2>', unsafe_allow_html=True)
    
    total_items, total_price, cart = get_cart_summary()
    
    if not cart:
        st.info("🛒 Your cart is empty")
        return
    
    # Cart summary
    st.markdown(f'''
    <div class="cart-summary">
        <h3 style="color: #00FFFF; margin: 0 0 0.5rem 0;">Cart Summary</h3>
        <p style="color: #FA9320; font-size: 1.2rem; margin: 0;">Total Items: <strong>{total_items}</strong></p>
        <p style="color: #21A95A; font-size: 1.4rem; margin: 0.5rem 0 0 0;">Total Price: <strong>BDT {total_price:,}</strong></p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Cart items
    st.markdown("### Items in Cart")
    
    for product_id, item in cart.items():
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        
        with col1:
            if item['image_url']:
                st.markdown(f'<img src="{item["image_url"]}" style="width: 60px; height: 60px; object-fit: contain; border-radius: 4px; border: 1px solid #00FFFF40;">', unsafe_allow_html=True)
            else:
                st.markdown('<div style="width: 60px; height: 60px; background: #333; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #666;">No Image</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div><strong style="color: #00FFFF;">{item["title"][:50]}...</strong></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #FA9320;">Price: {item["price"]} each</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #21A95A;">Total: BDT {item["total_price"]:,}</div>', unsafe_allow_html=True)
        
        with col3:
            new_quantity = st.number_input(
                "Qty",
                min_value=0,
                value=item['quantity'],
                key=f"qty_{product_id}",
                help="Set to 0 to remove"
            )
            if new_quantity != item['quantity']:
                if update_quantity(product_id, new_quantity):
                    st.rerun()
        
        with col4:
            if st.button("🗑️", key=f"remove_{product_id}", help="Remove from cart"):
                if remove_from_cart(product_id):
                    st.success("Item removed!")
                    st.rerun()
            
            if item['link'] != "#":
                st.markdown(f'<a href="{item["link"]}" target="_blank" style="color: #00BFFF;">🔗 Visit</a>', unsafe_allow_html=True)

def run_streamlit_app():
    # Get cart summary for floating button
    total_items, total_price, _ = get_cart_summary()
    
    # Floating cart button
    if total_items > 0:
        st.markdown(f'''
        <div class="view-cart-btn" onclick="document.querySelector('[data-testid=\"stSidebar\"] button[kind=\"secondary\"]').click();">
            🛒 Cart ({total_items}) - BDT {total_price:,}
        </div>
        ''', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        page = st.radio("Navigation", ["🏠 Home", "🛒 Cart"], key="navigation")
    
    if page == "🛒 Cart":
        display_cart()
        return
    
    # Title
    st.markdown('<h1 style="color: #00FFFF;">🤖 RoboShop Scraper</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00BFFF; margin-bottom: 2rem;">Find the best deals across multiple platforms</h3>', unsafe_allow_html=True)

    # Sidebar for user inputs
    st.sidebar.markdown('<h2 style="color: #00FFFF;">🎯 Search Configuration</h2>', unsafe_allow_html=True)
    
    # Search text input
    search_text = st.sidebar.text_input(
        "🔍 Search Product",
        placeholder="Enter product name...",
        help="Type the product you want to search for"
    )
    
    # Price range manual input
    st.sidebar.markdown("💰 **Price Range (BDT)**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        price_from = st.number_input(
            "From:",
            min_value=0,
            max_value=100000,
            value=0,
            step=100,
            format="%d"
        )
    with col2:
        price_to = st.number_input(
            "To:",
            min_value=0,
            max_value=100000,
            value=100000,
            step=100,
            format="%d"
        )
    
    # Handle "Any Price" option
    price_range = (price_from, price_to)
    if price_from == 0 and price_to == 100000:
        st.sidebar.markdown("*Currently set to: **Any Price***")
    
    # Region selection
    region = st.sidebar.selectbox(
        "🌍 Select Region",
        options=["Bangladeshi", "American", "Global"],
        index=0,
        help="Choose the market region to search in"
    )
    
    # Include images toggle
    include_images = st.sidebar.checkbox(
        "📸 Include Images",
        value=False,
        help="Toggle to include product images in results"
    )
    
    # Website sources based on region
    st.sidebar.markdown("---")
    st.sidebar.markdown("🌐 **Target Websites**")
    
    if region == "Bangladeshi":
        available_websites = sites['Bangladesh'].values()
    elif region == "American":
        available_websites = sites['America'].values()
    else:  # Global
        available_websites = list(sites['Bangladesh'].values()) + list(sites['America'].values())

    selected_websites = []
    for i, site in enumerate(available_websites, 1):
        is_selected = st.sidebar.checkbox(
            f"{i}. {site}",
            value=True,  # Default: all selected
            key=f"website_{site}"
        )
        if is_selected:
            selected_websites.append(site)
    
    if not selected_websites:
        st.sidebar.warning("⚠️ Please select at least one website!")
    
    # AI Compatibility Check removed
    
    # Let's Go button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚀 Let's Go!", type="primary", use_container_width=True):
        # Input validation
        if not search_text:
            st.sidebar.error("⚠️ Please enter a search term!")
            return
            
        if not selected_websites:
            st.sidebar.error("⚠️ Please select at least one website to search!")
            return
        
        # Collect all user inputs
        user_config = {
            "search_text": search_text.strip(),
            "price_range": {
                "min": price_range[0],
                "max": price_range[1]
            },
            "region": region,
            "selected_websites": selected_websites,
            "include_images": include_images
        }
        
        # Save config to JSON file for main.py
        import json
        import os
        
        try:
            config_file = "user_config.json"
            with open(config_file, 'w') as f:
                json.dump(user_config, f, indent=4)
        except Exception as e:
            st.error(f"❌ Error saving configuration: {str(e)}")
            return
        
       
        # Process and display results
        st.markdown("---")
        
        # Create a container for our results section
        results_container = st.container()
        
        # Import and run the aggregator
        try:
            import aggregator
            
            # Create progress indicators
            with results_container:
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                
                with progress_placeholder:
                    progress_bar = st.progress(0)
                
                with status_placeholder:
                    status_text = st.empty().text("📋 Loading configuration...")
                
                # Step 1: Load configuration
                progress_bar.progress(20)
                status_text.text("🔧 Initializing scrapers...")
                
                # Step 2: Initialize scraping
                progress_bar.progress(40)
                status_text.text("🚀 Scraping selected websites...")
                
                # Step 3: Scrape websites
                progress_bar.progress(60)
                
                # Get the processed results through main.py
                import project
                products = project.main()

                # Persist results & config in session state
                st.session_state["results_products"] = products
                st.session_state["results_config"] = user_config
                
                # Step 4: Processing results
                progress_bar.progress(80)
                status_text.text("📊 Processing results...")
                
                # Step 5: Complete
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                
                # Clear progress indicators after a short delay
                import time
                time.sleep(0.5)
                progress_placeholder.empty()
                status_placeholder.empty()
                
                # Display results in the results container
                if products and len(products) > 0:
                    display_products(products, user_config)
                else:
                    st.info("🔍 No products found matching your criteria. Try different search terms or adjust your filters.")
                
        except Exception as e:
            st.error(f"❌ Error processing results: {str(e)}")
            st.info("💡 Please check your scraper implementation and ensure all dependencies are installed.")
    
    # Main content area - Default state
    else:
        # If we already have products in session, show them (enables sorting without re-running search)
        session_products = st.session_state.get("results_products")
        session_config = st.session_state.get("results_config")
        if session_products and session_config:
            display_products(session_products, session_config)
        else:
            # Welcome message when no search is performed yet
            st.markdown('<h2 style="color: #00FFFF;">🔍 Ready to Search</h2>', unsafe_allow_html=True)
            st.markdown("""
            <div class="product-card" style="text-align: center; padding: 3rem; border: 2px solid #00FFFF;">
                <h3 style="color: #00BFFF; margin-bottom: 1.5rem;">Configure your search and click "Let's Go!" to start</h3>
                <p style="color: #CCCCCC; font-size: 1.1rem; line-height: 1.6;">
                    📝 Enter your search terms<br>
                    💰 Set your price range<br>
                    🌐 Choose websites to scrape<br>
                    🚀 Click "Let's Go!" to begin
                </p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    run_streamlit_app()
