**SEO Analysis Tool**. Here's a brief overview of each section and its purpose:

---

### **1. `src/`**
This is the core of the project, housing all the main functionalities. It is broken into logical submodules:

#### - **`api/`**
Handles integrations with external APIs:
- `gsc_api.py`: Interface for Google Search Console.
- `moz_api.py`: Interface for Moz API.
- `rate_limiter.py`: Ensures API requests comply with rate limits.

#### - **`scraper/`**
Handles web scraping and validation:
- `web_scraper.py`: Contains logic for scraping web data.
- `validators.py`: Includes URL validation and `robots.txt` parsing.

#### - **`data/`**
Manages collected data:
- `collector.py`: Manages the process of gathering data.
- `aggregator.py`: Combines data from APIs and scrapers.
- `cache.py`: Implements a caching mechanism to reduce redundant requests.

#### - **`reports/`**
Generates reports:
- `generator.py`: Handles report generation.
- `translations.py`: Manages Dutch translations for multilingual support.

#### - **`utils/`**
Utility functions shared across the project:
- `helpers.py`: Contains common utilities like string formatting, date manipulation, etc.

---

### **2. `streamlit/`**
This directory houses the Streamlit-based UI components:
- **`app.py`**: Entry point for the Streamlit app.
- **`components/`**: Includes submodules for various app functionalities:
  - `dashboard.py`: For data visualizations.
  - `metrics.py`: To display key SEO metrics.
  - `report.py`: For report display and export.
- **`config.py`**: Manages Streamlit-specific configurations like themes or session states.

---

### **3. `tests/`**
Contains unit tests to ensure code reliability:
- `test_apis.py`: Tests for API integrations.
- `test_scraper.py`: Tests for the web scraper module.
- `test_data.py`: Tests for data collection and aggregation.

---

### **4. `config/`**
Stores configuration settings:
- `settings.py`: API keys and configuration parameters (e.g., rate limits, endpoint URLs).
