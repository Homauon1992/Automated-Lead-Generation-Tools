🕵️‍♂️ Lead Extractor - Simple Contact Scraper
A specialized Python-based tool designed to automate the discovery of contact information from web pages. It streamlines the lead generation process by identifying and collecting communication channels directly from the source.

🛠 Key Technical Features
Email Discovery Logic: Uses advanced regular expressions (Regex) to find and extract email addresses hidden in page text or mailto links.

Social Media Link Tracking: Specifically targets and extracts links for Instagram, LinkedIn, and X (Twitter).

Clean Data Output: Automatically formats and saves the results into a professional CSV file for immediate use in CRM or outreach tools.

Robust Content Fetching: Implements secure HTTP requests to handle page content retrieval efficiently.

📦 Tech Stack
Python: Core engine.

BeautifulSoup4: For HTML structure parsing and link analysis.

Requests: For handling web communication.

Colorama: For a clean and interactive Command Line interface.



------------------------------------------------------Update To V2 With Selenium--------------------------------------------------------------------

## 🚀 Version 2.0 Update: Selenium Integration
The engine has been upgraded to support **Dynamic Content Extraction**. By integrating **Selenium WebDriver**, the tool can now interact with JavaScript-heavy websites and perform automated scrolling to capture lazy-loaded data.

### What's New in v2.0:
* **Headless Browser Automation:** Uses Chrome in headless mode for fast, invisible data collection.
* **Dynamic Content Support:** Bypasses limitations of static scrapers by rendering JavaScript.
* **Automated Interaction:** Implements window scrolling to trigger data loading.