import streamlit as st
import json
from scrapers.sites import sites
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
    
    /* Sidebar headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #00BFFF !important;
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
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background-color: #00FFFF;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #00BFFF;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > div {
        background-color: #262626;
        border: 2px solid #00FFFF;
        color: #FAFAFA;
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
    
    /* Toggle buttons */
    .stCheckbox > label {
        color: #FAFAFA !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background-color: #262626;
        border: 2px solid #00FFFF;
        color: #FAFAFA;
        border-radius: 8px;
    }
    
    /* Cards for results */
    .result-card {
        background: linear-gradient(135deg, #1E1E1E, #2D2D2D);
        border: 2px solid #00FFFF;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px #00FFFF20;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        border-color: #00BFFF;
        box-shadow: 0 0 30px #00BFFF30;
        transform: translateY(-5px);
    }
    
    /* Price tags */
    .price-tag {
       
        color: #FA9320;
        padding: 0.5rem 1rem;
      
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    

    
    /* Success message styling */
    .stSuccess {
        background-color: #1E3A1E;
        border: 2px solid #00FF00;
        color: #00FF00;
    }
</style>
""", unsafe_allow_html=True)

def display_products(products, config):
    """Display the processed products in a clean layout"""
    if not products:
        st.info("🔍 No products found matching your criteria.")
        return

    st.markdown(f'<h2 style="color: #FA9320;">🛒 Found {len(products)} Products</h2>', unsafe_allow_html=True)

    cols_per_row = 3
    include_images = config.get('include_images', False)

    for i in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(products):
                with cols[j]:
                    create_product_card(products[idx], include_images)
    # end for


def create_product_card(product, include_images: bool):
    """Render a single product card."""
    title = product.get("title", "No Title Available")
    link = product.get("link", "#")
    price = product.get("price") or "Price N/A"
    image_url = product.get("image") if include_images else None

    clean_title = (title[:70] + "...") if len(title) > 70 else title

    from urllib.parse import urlparse
    try:
        domain = urlparse(link).netloc or "Unknown"
    except Exception:
        domain = "Unknown"

    parts = []
    parts.append('<div class="result-card" style="display:flex;flex-direction:column;min-height:360px;position:relative;border-color:#FA9320;box-shadow:0 0 14px #fa93201a;">')
    parts.append(f'<div style="position:absolute;top:8px;right:8px;background:rgba(250,147,32,0.15);backdrop-filter:blur(4px);padding:4px 8px;border:1px solid #FA9320;border-radius:14px;font-size:11px;color:#FA9320;font-weight:600;">🛍️ {domain.replace("www.", "")}</div>')

    if include_images:
        if image_url:
            parts.append(
                '<div style="flex:0 0 150px;display:flex;align-items:center;justify-content:center;margin-bottom:10px;overflow:hidden;">'
                f'<img alt="{clean_title}" src="{image_url}" style="max-width:100%;max-height:150px;object-fit:contain;border-radius:6px;border:1px solid #073642;" '
                "onerror=\"this.onerror=null;this.style.display='none';\" />"
                '</div>'
            )
        else:
            parts.append('<div style="flex:0 0 150px;display:flex;align-items:center;justify-content:center;margin-bottom:10px;border:1px dashed #004455;border-radius:6px;color:#555;font-size:13px;">No Image</div>')

    parts.append(
        f'<div style="flex-grow:1;">'
        f'<h4 style="margin:0 0 8px 0;color:#FA9320;font-size:0.97rem;line-height:1.35;">📦 {clean_title}</h4>'
        '</div>'
    )

    parts.append(
        f'<div style="margin:0 0 14px 0;">'
        f'<span class="price-tag" style="color:#FA9320;display:inline-flex;align-items:center;gap:6px;font-size:18px">💰 <span>{price}</span></span>'
        '</div>'
    )

    if link and link != "#":
        parts.append(
            f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;margin-top:auto;">'
            '<div style="background:linear-gradient(135deg,#FA9320,#ffb469);color:#000;font-weight:650;text-align:center;padding:10px 12px;border-radius:8px;font-size:0.85rem;letter-spacing:0.3px;display:flex;align-items:center;justify-content:center;gap:6px;">🔗 Visit</div>'
            '</a>'
        )
    else:
        parts.append('<div style="margin-top:auto;background:#333;color:#777;text-align:center;padding:10px 12px;border-radius:8px;font-size:0.85rem;">Link Not Available</div>')

    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def run_streamlit_app():
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
    
    # AI Compatibility Check
    st.sidebar.markdown("---")
    st.sidebar.markdown("🤖 **AI Compatibility Check**")
    
    ai_mode = st.sidebar.checkbox(
        "Enable AI Suggestions",
        value=False,
        help="Enable AI-powered search suggestions and compatibility checks"
    )
    
    # AI suggestion text field (only enabled when AI mode is on)
    ai_suggestions = ""
    if ai_mode:
        ai_suggestions = st.sidebar.text_area(
            "AI Search Components:",
            placeholder="Enter additional Components to get the best compatible products...",
            height=100,
            help="Add specific components for AI to consider in the search"
        )
    else:
        st.sidebar.text_area(
            "AI Search Components:",
            placeholder="Enable AI mode to use this feature...",
            height=100,
            disabled=True,
            help="Enable AI mode above to use this feature"
        )
    
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
            "include_images": include_images,
            "ai_mode": ai_mode,
            "ai_suggestions": ai_suggestions if ai_mode else None
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
                import main
                products = main.main()
                
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
        # Welcome message when no search is performed
        st.markdown('<h2 style="color: #00FFFF;">🔍 Ready to Search</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="result-card" style="text-align: center; padding: 3rem;">
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
