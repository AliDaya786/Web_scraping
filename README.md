# Web_scraping
# 🏥 BBB Medical Billing Scraper

This project is a Playwright-based web scraper that acccurately extracts structured data about accredited **Medical Billing** companies from the [Better Business Bureau (BBB)](https://www.bbb.org/) website. The extracted data is saved to a clean CSV file with standardized formatting.

---

## 🧠 High-Level Extraction Method

1. **Navigate to each paginated search result page**
2. **Locate each business card**
   - Extract business name, phone number, accreditation status, and profile URL
3. **Visit each business profile**
   - Extract `Name`, `Phone`, `Address`, and `Principal Contact` from embedded **JSON-LD (`<script type='application/ld+json'>`)**
   - Fallback to DOM scraping if JSON-LD is missing
4. **Deduplicate** using the **BBB business ID** extracted from the profile URL
5. **Export** clean, structured results to a CSV file

## 📌 Features + Design

- ✅ Extracts structured business data from embedded `application/ld+json`
- ✅ Deduplicates businesses using unique BBB business IDs
- ✅ Formats phone numbers consistently with `+1` country code
- ✅ Uses fallback methods when structured data is unavailable
- ✅ Outputs results to a clean `medical_billing_companies.csv` file
- ✅ Respectfully scrapes by slowing down requests to avoid overwhelming the site.
- ✅ The scraper uses headless=False for visual representation; change to headless=True for faster, silent runs.

---

## 🧾 Output Fields

| Field              | Description                                  |
|-------------------|----------------------------------------------|
| **Name**          | Business name                                 |
| **Profile URL**   | Direct link to the BBB business page          |
| **Phone**         | Cleaned phone number in `+1XXXXXXXXXX` format |
| **Principal Contact** | Main employee/contact if listed            |
| **Address**       | Full address (street, city, state, zip)       |
| **Accredited**    | "Yes" if BBB Accredited, otherwise "No"       |

---

## 🛠️ Technologies Used

- Python 3.10+
- [Playwright (sync API)](https://playwright.dev/python/docs/intro)
- `csv` for structured output
- `json` and `re` for parsing
- `logging` for debugging and traceability

---

## 🚀 How to Run

1. **Install dependencies + Run file**:
```bash
pip install playwright
playwright install
py playwright_medical