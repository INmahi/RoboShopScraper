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
        background: linear-gradient(45deg, #00FFFF, #00BFFF);
        color: #000000;
        padding: 0.5rem 1rem;
        border-radius: 20px;
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
    if not products or len(products) == 0:
        st.info("🔍 No products found matching your criteria.")
        return
    
    # Add a nice header with the count
    st.markdown(f'<h2 style="color: #00FFFF;">🛒 Found {len(products)} Products</h2>', unsafe_allow_html=True)
    
    # Add filtering options
    
    # Display products in a responsive grid with better spacing
    cols_per_row = 3
    
    # Calculate rows needed
    total_rows = (len(products) + cols_per_row - 1) // cols_per_row
    
    for i in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(products):
                product = products[i + j]
                with cols[j]:
                    create_product_card(product, config.get('include_images', False))
    
    # Display summary stats
    # display_summary_stats(products, config)

def create_product_card(product, include_images):
    """Create a single product card with a clean design"""
    # Extract product information
    title = product.get('title', 'No Title Available')
    link = product.get('link', '#')
    image_url = product.get('image', '') if include_images else ''
    
    # Clean and truncate title for display
    if len(title) > 70:
        clean_title = title[:70].replace('"', '').replace("'", '') + "..."
    else:
        clean_title = title.replace('"', '').replace("'", '')
    
    # Extract domain for display
    try:
        from urllib.parse import urlparse
        domain = urlparse(link).netloc if link and link != '#' else "Unknown Source"
    except:
        domain = "Unknown Source"
    
    # Create the card container with a fixed height
    card_html = f'''
    <div class="result-card" style="height: 350px; display: flex; flex-direction: column; overflow: hidden; position: relative;">
    '''
    
    # Add source badge at the top right
    card_html += f'''
    <div style="position: absolute; top: 10px; right: 10px; background: rgba(0, 0, 0, 0.7); 
                padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; z-index: 10;">
        <span style="color: #00BFFF;">{domain.replace('www.', '')}</span>
    </div>
    '''
    
    # Add image if available and enabled
    if image_url and include_images:
        card_html += f'''
        <div style="text-align: center; margin-bottom: 1rem; height: 160px; display: flex; align-items: center; justify-content: center; overflow: hidden;">
            <img src="{image_url}" 
                 style="max-width: 100%; max-height: 160px; object-fit: contain; border-radius: 8px; transition: transform 0.3s ease;" 
                 onerror="this.onerror=null; this.src='https://via.placeholder.com/150x150?text=No+Image'; this.style.opacity='0.5';"
                 onmouseover="this.style.transform='scale(1.05)'"
                 onmouseout="this.style.transform='scale(1)'" />
        </div>
        '''
    elif include_images:
        card_html += f'''
        <div style="text-align: center; margin-bottom: 1rem; height: 160px; background: linear-gradient(135deg, #1A1A1A, #0E0E0E); 
                    border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px solid #004455;">
            <span style="color: #666; font-size: 0.9rem;">📷 No Image Available</span>
        </div>
        '''
    
    # Add title with hover effect
    card_html += f'''
        <div style="flex-grow: 1; overflow: hidden;">
            <h4 style="color: #00FFFF; margin-bottom: 0.5rem; font-size: 0.95rem; line-height: 1.4; 
                       transition: color 0.3s ease;" 
                onmouseover="this.style.color='#FFFFFF'"
                onmouseout="this.style.color='#00FFFF'">
                {clean_title}
            </h4>
        </div>
    '''
    
    # Add visit button with enhanced hover effect
    if link != '#':
        card_html += f'''
        <div style="margin-top: auto; padding-top: 0.5rem;">
            <a href="{link}" target="_blank" style="text-decoration: none;" title="Visit {clean_title}">
                <div style="background: linear-gradient(45deg, #00FFFF, #00BFFF); color: #000000; 
                           padding: 0.7rem 1rem; border-radius: 8px; text-align: center; 
                           font-weight: bold; transition: all 0.3s ease;"
                     onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 5px 15px rgba(0, 191, 255, 0.4)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    🔗 Visit Product
                </div>
            </a>
        </div>
        '''
    else:
        card_html += f'''
        <div style="margin-top: auto; padding-top: 0.5rem;">
            <div style="background: #444; color: #888; padding: 0.7rem 1rem; border-radius: 8px; text-align: center;">
                🔗 Link Not Available
            </div>
        </div>
        '''
    
    card_html += '</div>'
    
    st.markdown(card_html, unsafe_allow_html=True)

# def display_summary_stats(products, config):
#     """Display summary statistics with improved error handling"""
#     st.markdown("---")
#     col1, col2, col3 = st.columns(3)
    
#     # Count products by source/domain
#     sources = {}
#     with_images = 0
    
#     for product in products:
#         # Count products with images
#         if product.get('image'):
#             with_images += 1
            
#         # Count sources
#         link = product.get('link', '')
#         if link:
#             try:
#                 from urllib.parse import urlparse
#                 domain = urlparse(link).netloc
#                 if domain:
#                     sources[domain] = sources.get(domain, 0) + 1
#                 else:
#                     sources['Unknown'] = sources.get('Unknown', 0) + 1
#             except:
#                 sources['Unknown'] = sources.get('Unknown', 0) + 1
    
#     # Search Statistics Card
#     with col1:
#         search_term = config.get("search_text", "")
#         if len(search_term) > 30:
#             search_term = search_term[:30] + "..."
            
#         st.markdown(f'''
#         <div class="result-card">
#             <h4 style="color: #00BFFF;">📊 Search Results</h4>
#             <p>• Total Found: <span style="color: #00FFFF; font-weight: bold;">{len(products)}</span> products</p>
#             <p>• With Images: <span style="color: #00FFFF;">{with_images}</span> products</p>
#             <p>• Search Term: "<span style="color: #00FFFF;">{search_term}</span>"</p>
#         </div>
#         ''', unsafe_allow_html=True)
    
#     # Sources Card
#     with col2:
#         st.markdown(f'''
#         <div class="result-card">
#             <h4 style="color: #00BFFF;">🌐 Sources</h4>
#         ''', unsafe_allow_html=True)
        
#         if sources:
#             # Sort sources by count
#             sorted_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
#             for source, count in sorted_sources[:3]:
#                 # Clean up domain name for display
#                 display_source = source.replace('www.', '')
#                 if len(display_source) > 30:
#                     display_source = display_source[:27] + "..."
#                 st.markdown(f'<p>• <span style="color: #00FFFF;">{display_source}</span>: {count} items</p>', unsafe_allow_html=True)
            
#             # If there are more sources
#             if len(sources) > 3:
#                 remaining = sum([count for _, count in sorted_sources[3:]])
#                 st.markdown(f'<p>• <span style="color: #888;">+{len(sources) - 3} more sources</span>: {remaining} items</p>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<p style="color: #888;">No source information available</p>', unsafe_allow_html=True)
            
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Active Filters Card
#     with col3:
#         # Handle potential missing config values with safe defaults
#         min_price = config.get("price_range", {}).get("min", 0)
#         max_price = config.get("price_range", {}).get("max", 100000)
        
#         try:
#             min_price = int(min_price)
#             max_price = int(max_price)
#         except (ValueError, TypeError):
#             min_price = 0
#             max_price = 100000
            
#         region = config.get("region", "N/A")
#         include_images = config.get("include_images", False)
        
#         # Selected websites
#         selected_websites = config.get("selected_websites", [])
#         website_count = len(selected_websites) if selected_websites else 0
            
#         st.markdown(f'''
#         <div class="result-card">
#             <h4 style="color: #00BFFF;">🎯 Active Filters</h4>
#             <p>• Price Range: <span style="color: #00FFFF;">৳{min_price:,} - ৳{max_price:,}</span></p>
#             <p>• Region: <span style="color: #00FFFF;">{region}</span></p>
#             <p>• Websites: <span style="color: #00FFFF;">{website_count}</span> selected</p>
#         </div>
#         ''', unsafe_allow_html=True)

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
