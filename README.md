# RoboShop Scraper

#### Video Demo:  <URL HERE>

#### Description:
RoboShop Scraper is a modern Streamlit-based application designed to search, filter, and compare robotics and electronics products across multiple online stores. It provides a user-friendly interface for product discovery, price comparison, and decision-making, making it an ideal tool for hobbyists, students, and professionals in the robotics and electronics domain.

---

## Features

- **Multi-site Product Search**: Search for products across multiple e-commerce websites.
- **Region-based Filtering**: Choose between Bangladeshi, American, or Global regions.
- **Price Range Filtering**: Set minimum and maximum price limits to narrow down results.
- **Dynamic Sorting**: Sort products by price (low to high or high to low) without re-scraping.
- **Image Inclusion**: Optionally include product images for better visualization.
- **Cart Management**: Add products to a cart, update quantities, or clear the cart with one click.
- **Customizable Scrapers**: Easily add new scrapers for additional websites.

---

## Project Structure

```
RoboShopScraper/
├── app.py                # Streamlit UI (inputs, session state, rendering)
├── aggregator.py         # Dispatches to the correct site scraper(s)
├── scrapers/
│   ├── roboticsbd.py     # RoboticsBD scraper
│   ├── roboticsshop.py   # RoboticsShop scraper
│   └── sites.py          # Region-to-site mapping
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── user_config.json      # Auto-generated per search
└── tests/                # Suggested place for automated tests
```

---

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/INmahi/RoboShopScraper.git
   cd RoboShopScraper
   ```

2. **Set Up a Virtual Environment**:
   - Windows:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. **Search for Products**:
   - Enter a product name (e.g., "Arduino Uno").
   - Select a price range and region.
   - Choose the websites to include in the search.

2. **View Results**:
   - Browse through the product cards.
   - Sort results by price.

3. **Manage Cart**:
   - Add products to the cart.
   - Update quantities or remove items.
   - Clear the cart with one click.

---

## Future Upgrades

- **AI Compatibility**: Implement AI-based product recommendations and compatibility checks.
- **Non-Streamlit Migration**: Transition to a standalone web application for broader deployment.
- **Additional Scrapers**: Add support for more international e-commerce websites.

Contributions are welcome! See the [Contributing](#contributing) section below.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your fork and submit a pull request.

---

## Contact

**Author**: Ishat Noor Mahi  
**Website**: [inmlink.netlify.app](https://inmlink.netlify.app)  
**GitHub Issues**: [Open an issue](https://github.com/INmahi/RoboShopScraper/issues)

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
