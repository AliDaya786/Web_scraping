import asyncio
import os
import csv
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from stagehand import Stagehand, StagehandConfig

# Load environment variables
load_dotenv()

# Define Pydantic model
class Business(BaseModel):
    Name: str = Field(..., description="Business name")
    ProfileURL: str = Field(..., description="Business profile URL")
    Phone: str = Field(..., description="Phone number")
    PrincipalContact: str = Field(..., description="Principal contact name and title")
    Address: str = Field(..., description="Full business address")
    Accredited: str = Field(..., description="BBB Accreditation (Yes/No)")

async def scrape_bbb():
    # Stagehand configuration
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="gpt-4o", 
        model_api_key=os.getenv("OPENAI_API_KEY"),
    )

    stagehand = Stagehand(config)

    try:
        print("\nInitializing Stagehand...")
        await stagehand.init()

        if stagehand.env == "BROWSERBASE":
            print(f"🌐 View session: https://www.browserbase.com/sessions/{stagehand.session_id}")

        page = stagehand.page
        base_url = "https://www.bbb.org/search?filter_category=60548-100&filter_category=60142-000&filter_ratings=A&filter_accreditation=1&find_country=USA&find_text=Medical+Billing&page={page_num}"
        
        businesses = []
        
        for page_num in range(1, 2):  # Adjust the range as needed
            url = base_url.format(page_num=page_num)
            await page.goto(url)
            print(f"Scraping page {page_num}: {url}")
            
            try:
                await page.wait_for_selector("div.card.result-card", timeout=5000)
            except Exception as e:
                print(f"Timeout waiting for business cards on page {page_num}: {e}")
                continue
                
            business_cards = page.locator("div.card.result-card")
            count = await business_cards.count()
            print(f"Found {count} business cards on page {page_num}")
            
            if count == 0:
                break  # No more results
                
            for i in range(count):
                card = business_cards.nth(i)
                name_el = card.locator("h3.result-business-name a")
                name = await name_el.inner_text() if await name_el.count() > 0 else ""
                href = await name_el.get_attribute("href") if await name_el.count() > 0 else ""
                profile_url = href if href and href.startswith("http") else f"https://www.bbb.org{href}" if href else ""
                
                print(f"\nVisiting business {i+1}/{count}: {name} - {profile_url}")
                
                if profile_url:
                    # Visit the business profile page
                    await page.goto(profile_url)
                    
                    # Wait for page to load
                    await asyncio.sleep(2)
                    
                    # Use LLM to extract detailed business info from the profile page
                    detail_prompt = """
                    Extract detailed information about this business from the BBB profile page.
                    Extract:
                    - Name
                    - Profile URL (this should be the current page URL)
                    - Phone (formatted as +1XXXXXXXXXX if available)
                    - Principal contact person and title (look in the leadership section)
                    - Address (single string with full address)
                    - BBB Accreditation (Yes or No)
                    
                    Return a JSON object with these fields.
                    """
                    
                    business_detail = await page.extract(instruction=detail_prompt, schema=Business, strategy="snapshot")
                    businesses.append(business_detail)

                    #await asyncio.sleep(1)
                
                # Return to the search results page to continue scraping
                await page.goto(url)
                await page.wait_for_selector("div.card.result-card", timeout=5000)
                # Refetch the business cards since we navigated away
                business_cards = page.locator("div.card.result-card")

        print(f"\n✅ Extracted and saved {len(businesses)} businesses to medical_billing_companies.csv")

        
        with open("medical_billing_companies.csv", mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=Business.model_fields.keys())
            writer.writeheader()
            for b in businesses:
                writer.writerow(b.model_dump())  
        

    finally:
        print("\n🔒 Closing Stagehand session...")
        await stagehand.close()

if __name__ == "__main__":
    asyncio.run(scrape_bbb())
