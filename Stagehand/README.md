# AI BBB Medical Billing Company Scraper 🧠💼

This project is an AI-powered web scraper that uses [Stagehand](https://github.com/browserbase/stagehand-python) and [Browserbase](https://browserbase.com) to extract structured business data from the Better Business Bureau (BBB) website for medical billing companies. It mimics human navigation to click into each profile, reads the page like an accessibility tool, and uses GPT-4o to intelligently extract business contact details.


Instead of relying on brittle manual scraping logic, this solution uses **AI-powered extraction (LLMs)** to flexibly and intelligently parse business profile pages.


---

## 🚀 Features + Design

### ✅ Overview
- Targets search url on BBB.org & supports pagination.
- Navigates through **search result listings**
- Clicks into each **individual business profile**
- Uses **natural language AI prompts** to extract structured data via GPT-4o
- Outputs results into a clean **CSV file**

### 🤖 AI Extraction with Stagehand
This scraper leverages `page.extract()` from Stagehand, which lets an LLM (GPT-4o) interpret a webpage’s content and return structured JSON according to a prompt and schema. Key design choices include:
- **Prompt-based tasking**: The LLM is asked to extract only relevant fields using natural language.
- **Schema-enforced output**: Uses [Pydantic](https://docs.pydantic.dev/) to validate the response and structure the output.
- **Snapshot strategy**: Uses a full visual DOM snapshot to give the LLM a rich representation of the page.

### 🔧 Technologies Used
- Python 3.10+
- [Stagehand](https://github.com/browserbase/stagehand-python)
- Browserbase (cloud browser automation)
- OpenAI GPT-4o API
- Pydantic for schema validation
- dotenv for local config

---

## ⚠️ Issues Encountered

### 1. **Principal Contact Field Was Missing**
Initially, the scraper tried to extract all fields directly from the search result cards (e.g., name, phone, contact, etc.). However, **the "Principal Contact" field wasn’t available on the search results page**, only inside the detailed company profile. 

**Solution**:  
The scraper was refactored to **click into each business profile**, wait for the page to load, and then run a targeted AI prompt using Stagehand to extract structured data from that deeper page.

### 2. **Prompt Quality and Completeness**
Initial prompts failed to consistently extract all fields, especially `PrincipalContact`. This required multiple prompt refinements to ensure the AI understood exactly what was expected from the page.

### 3. **Schema Definition for Snapshot Strategy**
When using the `strategy="snapshot"` mode with Stagehand, it is critical that each schema field is accompanied by a **descriptive `Field(..., description="...")`**. The snapshot strategy relies on these descriptions to semantically guide the LLM’s extraction process based on the page’s visual and accessibility tree.

Omitting descriptions resulted in incomplete or null extractions - even if the field was present in the prompt and data. Adding accurate field descriptions fixed this and enabled reliable schema-based scraping.

---
