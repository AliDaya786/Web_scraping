# 🏥 BBB Medical Billing Scraper

This project is a Playwright-based web scraper that acccurately extracts structured data about accredited **Medical Billing** companies from the [Better Business Bureau (BBB). The base_url used is "https://www.bbb.org/search?filter_category=60548-100&filter_category=60142-000&filter_ratings=A&find_country=USA&find_text=Medical+Billing&page={page_num}". The extracted data is saved to a clean CSV file with standardized formatting.

---

## 🧠 High-Level Extraction Method

1. **Navigate to each paginated search result page (page 1-15)**
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
## Issues Encountered
<details> <summary><strong>1. Duplicate Businesses in CSV</strong></summary>
Problem: Some businesses appeared multiple times across paginated search results.

Cause: Deduplication based on business name or profile URL was unreliable due to inconsistencies and variations.

Solution: Extracted a stable BBB business ID from the URL using a regex (-(\d{4}-\d+)$) and used a seen_ids set to avoid duplicates.

</details> <details> <summary><strong>2. JSON-LD Parsing Failures</strong></summary>
Problem: Some business profile pages failed to return usable structured data.

Causes: JSON-LD content structure varied — sometimes it was a list, sometimes a dictionary.

Solution: Wrapped parsing in try/except, handled both list and dict formats, and safely pulled structured fields like address, phone, and contact name.

</details> <details> <summary><strong>3. Timeout on Profile Page Navigation</strong></summary>
Problem: Page.goto(profile_url) occasionally failed with a timeout.

Solution: Introduced time.sleep(2) between requests to throttle scraping and prevent overwhelming the server. 

</details> <details> <summary><strong>4. Inconsistent Principal Contact Field</strong></summary>
Problem: Principal contact details weren't always available in a consistent DOM location.

Solution: Extracted this from the JSON-LD employee object (when present), combining honorifics, names, and job titles. Gracefully handled missing fields.

</details> <details> <summary><strong>5. Phone Numbers Missing Country Code in CSV file</strong></summary>
Problem: Phone numbers scraped from JSON and with clean _phone() function had phone number displayed properly but when writing to CSV lost the '+'.

Solution: When Excel saw + at the beginning it stripped it so I included prefix with single quote

</details> <details> <summary><strong>6. BBB Accreditation Detection</strong></summary>
Problem: Determining if a business was BBB-accredited required inspecting subtle UI elements.

Solution: Checked for the presence of an img tag with alt="Accredited Business" inside each card.

</details> <details> <summary><strong>7. Missing or Malformed Address Data</strong></summary>
Problem: JSON-LD sometimes omitted the full address, or fields were incomplete.

Solution: Fallback to scraping visible DOM elements (.bpr-overview-address p.bds-body) to reconstruct a usable address string.

</details>

## 🚀 How to Run

1. **Install dependencies + Run file**:
```bash
pip install playwright
playwright install
py playwright_medical

---
