import streamlit as st
import json

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

def main():
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
            step=1000,
            format="%d"
        )
    with col2:
        price_to = st.number_input(
            "To:",
            min_value=0,
            max_value=100000,
            value=100000,
            step=1000,
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
            placeholder="Enter additional search criteria for AI processing...",
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
        # Collect all user inputs
        user_config = {
            "search_text": search_text,
            "price_range": {
                "min": price_range[0],
                "max": price_range[1]
            },
            "region": region,
            "include_images": include_images,
            "ai_mode": ai_mode,
            "ai_suggestions": ai_suggestions if ai_mode else None
        }
        
        # Display the configuration
        st.sidebar.success("Configuration captured!")
        
        # Show the reusable Python code in the main area
        st.markdown('<h2 style="color: #00FFFF;">📋 User Configuration</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🎛️ Current Settings")
            st.json(user_config)
        
        with col2:
            st.markdown("### 🐍 Reusable Python Code")
            python_code = f'''# User Configuration
user_config = {{
    "search_text": "{search_text}",
    "price_range": {{
        "min": {price_range[0]},
        "max": {price_range[1]}
    }},
    "region": "{region}",
    "include_images": {include_images},
    "ai_mode": {ai_mode},
    "ai_suggestions": {"'" + ai_suggestions + "'" if ai_mode and ai_suggestions else "None"}
}}

# Access values:
search_query = user_config["search_text"]
min_price = user_config["price_range"]["min"]
max_price = user_config["price_range"]["max"]
selected_region = user_config["region"]
images_enabled = user_config["include_images"]
ai_enabled = user_config["ai_mode"]
ai_input = user_config["ai_suggestions"]
'''
            st.code(python_code, language="python")
    
    # Main content area - Dummy results for now
    else:
        st.markdown('<h2 style="color: #00FFFF;">🛒 Search Results</h2>', unsafe_allow_html=True)
        
        # Create dummy product cards
        col1, col2, col3 = st.columns(3)
        
        dummy_products = [
            {"name": "Gaming Laptop Pro", "price": "৳85,000", "store": "TechShop BD", "rating": "4.8⭐"},
            {"name": "Wireless Headphones", "price": "৳12,500", "store": "AudioWorld", "rating": "4.6⭐"},
            {"name": "Smart Watch Ultra", "price": "৳25,000", "store": "GadgetHub", "rating": "4.7⭐"},
            {"name": "Gaming Mouse RGB", "price": "৳3,500", "store": "GameZone BD", "rating": "4.5⭐"},
            {"name": "Mechanical Keyboard", "price": "৳8,200", "store": "KeyWorld", "rating": "4.9⭐"},
            {"name": "4K Monitor 27\"", "price": "৳35,000", "store": "DisplayTech", "rating": "4.6⭐"}
        ]
        
        for i, product in enumerate(dummy_products):
            with [col1, col2, col3][i % 3]:
                st.markdown(f'''
                <div class="result-card">
                    <h4 style="color: #00FFFF; margin-bottom: 0.5rem;">{product["name"]}</h4>
                    <div class="price-tag">{product["price"]}</div>
                    <p style="margin: 0.5rem 0; color: #CCCCCC;">Store: {product["store"]}</p>
                    <p style="margin: 0; color: #FFD700;">{product["rating"]}</p>
                </div>
                ''', unsafe_allow_html=True)
        
        # Additional info section
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('''
            <div class="result-card">
                <h4 style="color: #00BFFF;">📊 Search Statistics</h4>
                <p>• Found: 156 products</p>
                <p>• Stores: 12 platforms</p>
                <p>• Avg. Price: ৳28,500</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('''
            <div class="result-card">
                <h4 style="color: #00BFFF;">⚡ Performance</h4>
                <p>• Search Time: 2.3s</p>
                <p>• Cache Hit: 78%</p>
                <p>• Success Rate: 94%</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown('''
            <div class="result-card">
                <h4 style="color: #00BFFF;">🎯 Filters Active</h4>
                <p>• Price Range: Any</p>
                <p>• Region: Bangladesh</p>
                <p>• Images: Disabled</p>
            </div>
            ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
