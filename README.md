<div align="center">

<h1>🤖 RoboShop Scraper</h1>
<p><strong>A modern Streamlit application to search, filter, and compare robotics & electronics products across multiple online shops.</strong></p>

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-ff4b4b?logo=streamlit)
![Status](https://img.shields.io/badge/Project-Active-success)

</div>

---

## 1. Overview

RoboShop Scraper provides a unified interface for searching product listings from multiple region‑specific e‑commerce sources. The UI is built with **Streamlit**, producing interactive product cards that include:

- Title
- Price (color‑coded per source)
- Direct link
- Optional image preview

You enter a product (e.g. `arduino uno`), choose websites, define a price band, and receive sorted, styled results. The system is intentionally modular so you can add new scrapers quickly.

> Educational / research intent only. Respect each website's Terms of Service & robots.txt and avoid abusive request patterns.

---

## 2. Core Features

- 🔍 Multi‑site product search (select which sites per run)
- 🌍 Region grouping (Bangladeshi / American / Global aggregate)
- 💰 Price range filtering (min/max BDT entry)
- 🖼️ Optional image inclusion
- 🎨 Dynamic per‑domain color themes on result cards
- ↕️ Sort by price (low→high / high→low) without re‑scraping
- 🧹 Stateless scrapers (no stale global data for fresh runs)
- ⚙️ Simple JSON config handoff (`user_config.json`)
- 🧩 Easily extend with new scrapers

Planned / placeholder:
- AI suggestion mode (UI hook present, logic to be implemented)
- Additional international stores

---

## 3. Project Structure

```
RoboShopScraper/
├── app.py                # Streamlit UI (inputs, session state, rendering)
├── main.py               # Loads config JSON, adapts to scraper format
├── aggregator.py         # Dispatches to the correct site scraper(s)
├── scrapers/
│   ├── roboticsbd.py     # RoboticsBD scraper
│   ├── roboticsshop.py   # RoboticsShop scraper
│   └── sites.py          # Region → site name → base URL mapping (selection source)
├── requirements.txt      # Dependencies (to be installed in a venv)
├── README.md             # Documentation (this file)
├── user_config.json      # Auto-generated per search (do not edit manually)
└── (future) tests/       # Suggested place for automated tests
```

---

## 4. Working Logic (Data Flow)

```
[User Inputs in app.py]
  search_text, price_range, region, selected_websites, include_images
	│
	▼
Write user_config.json
	▼
main.load_user_config() → normalized user dict
	▼
aggregator.aggregate_products(user)
	│  loops over user['selected_websites']
	▼
scrapers/<site>.py.scraper(user) → list[product dict]
	▼
Concatenate all product lists → return to Streamlit
	▼
Session cache (for re-sorting) → styled card rendering
```

Each product dict follows:

```python
{
  "title": str,
  "link": str,          # absolute or relative product URL
  "price": str,         # e.g. "BDT 2450" or similar
  "image": str | optional
}
```

Sorting is performed client‑side by extracting digits from the `price` string.

---

## 5. User Manual

1. Launch the app (see install steps below).
2. Enter a product name: e.g. `servo motor`.
3. Choose a price range (defaults represent "Any Price").
4. Pick a region (Bangladeshi, American, or Global). Global merges lists.
5. Toggle which websites to include (all on by default).
6. (Optional) enable "Include Images" (slower, more bandwidth).
7. (Optional) toggle AI mode (currently placeholder text area).
8. Click "🚀 Let's Go!".
9. Wait for the progress bar to finish.
10. Use the sort dropdown above the results to reorder by price.

If no products match, adjust keywords or widen price bounds.

---

## 6. Download / Installation (All Platforms)

### Option A: Git Clone (Recommended)

```bash
git clone https://github.com/<your-username>/RoboShopScraper.git
cd RoboShopScraper
```

### Option B: Download ZIP
1. Click the green "Code" button on GitHub.
2. Choose "Download ZIP".
3. Extract the archive to your chosen folder.

### Create & Activate Virtual Environment

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

Visit: http://localhost:8501 (auto-opens in most cases).

To stop: Ctrl + C in the terminal.

---

## 7. Updating / Adding Scrapers

### A. Add the Base URL (Optional for UI Listing)
Edit `scrapers/sites.py` and place your site under the appropriate region or create a new region key:

```python
sites = {
    'Bangladesh': {
	'Roboticsbd': 'https://www.store.roboticsbd.com/',
	'Roboticsshop': 'https://roboticsshop.com.bd/',
	'MyNewStore': 'https://example.com/',
    },
    # ...
}
```

### B. Create the Scraper Module
Add `scrapers/mynewstore.py` implementing:

```python
def scraper(user: dict) -> list[dict]:
    # return list of product dicts
```

Ensure you:
- Construct search URL(s) using `user['search_text']`.
- Filter by words: each search term should appear in the lowercased title.
- Enforce price range using `user['price_min']` / `user['price_max']` if the site exposes price.
- Return fresh lists (avoid module‑level global accumulation).

### C. Register in `aggregator.py`

```python
from scrapers import mynewstore

for website in user['selected_websites']:
    # ...previous code
    elif 'example.com' in website:
        products.extend(mynewstore.scraper(user))
```

### D. Test
Run the app, select the site, confirm products appear and price sorting works.

---

## 8. Editing `sites.py`

Purpose: Control which base URLs appear in the Streamlit selection UI grouped by region. The key (e.g. `Roboticsbd`) is just a label; the value is the base URL used for matching inside `aggregator.py`.

> Matching currently relies on substring checks (e.g., `'store.roboticsbd.com' in website`). If you modify domains, update the conditional logic in `aggregator.py` accordingly.

---

## 9. Requirements & Environment

Core dependencies (see pinned versions in `requirements.txt`):

| Library | Purpose |
|---------|---------|
| streamlit | Web UI framework |
| requests | HTTP fetching |
| beautifulsoup4 | HTML parsing |
| rich | (Future) improved logging / CLI visuals |

You can update to newer patch versions with:

```bash
pip install --upgrade streamlit requests beautifulsoup4 rich
```

(Re‑pin versions afterwards if required for reproducibility.)

---

## 10. Maintenance Tips

- Periodically verify CSS classes / DOM structures for each source – e‑commerce sites change layouts.
- Add network timeouts to new scrapers to avoid long hangs (`requests.get(..., timeout=15)`).
- Keep scrapers idempotent; no writes or persistent caches unless explicitly added.
- Consider adding automated tests that mock HTML snippets.

---

## 12. Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/add-new-store`
3. Make changes (add scraper, docs, etc.)
4. Run locally: `streamlit run app.py`
5. Commit: `git commit -m "Add new store scraper"`
6. Push and open a Pull Request with description + screenshots (if UI changes)

Please keep commits scoped and write clear messages.

---

## 13. License

Add a `LICENSE` file (e.g. MIT) for clarity if you plan to distribute. Example header:

```
MIT License (c) 2025 <Your Name>
```

---

## 14. Disclaimer

This tool is for educational / research use. You are responsible for ensuring that your use complies with applicable laws and with each website's policies. Do not overwhelm target servers.

---

## 15. Contact

**Author:** Ishat Noor Mahi  
**Contact:** [inmlink.netlify.app](https://inmlink.netlify.app)  
**Issues:** Please [open a GitHub issue](https://github.com/INmahi/RoboShopScraper/issues) with details & reproduction steps.

---

Happy scraping & building! 🚀
