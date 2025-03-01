import sqlite3
from playwright.sync_api import sync_playwright
import time

# LinkedIn login details (Replace with your credentials)
LINKEDIN_EMAIL = "email"
LINKEDIN_PASSWORD = "Password"

def login_to_linkedin(page):
    """Logs into LinkedIn."""
    page.goto("https://www.linkedin.com/login")
    page.fill("#username", LINKEDIN_EMAIL)
    page.fill("#password", LINKEDIN_PASSWORD)
    page.click("[type='submit']")
    time.sleep(5)  # Wait for page to load

def save_job_to_db(title, company, link, location, easy_apply):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            link TEXT,
            location TEXT,
            easy_apply TEXT
        )
    """)
    conn.commit()
    cursor.execute("INSERT INTO jobs (title, company, link, location, easy_apply) VALUES (?, ?, ?, ?, ?)",
                   (title, company, link, location, easy_apply))
    
    conn.commit()
    conn.close()

def scrape_jobs(search_keyword, location, max_jobs=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True for silent scraping
        page = browser.new_page()

        login_to_linkedin(page)  # Ensure this function logs in properly

        search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_keyword}&location={location}"
        page.goto(search_url)
        time.sleep(5)  # Allow page to load

        job_cards = page.query_selector_all(".job-card-container")

        if not job_cards:
            print("⚠️ No jobs found. LinkedIn's structure may have changed. Try updating selectors.")

        for job in job_cards[:max_jobs]:
            title_element = job.query_selector(".job-card-container__link")
            company_element = job.query_selector(".artdeco-entity-lockup__subtitle")
            link_element = job.query_selector(".job-card-container__link")
            location_element = job.query_selector(".maycnkXzNlqPrXMaIkFrLbgpWwcOEDs")
            easy_apply_element = job.query_selector(".job-card-container__footer-item span")

            title = title_element.inner_text().strip() if title_element else "N/A"
            company = company_element.inner_text().strip() if company_element else "N/A"
            link = f"https://www.linkedin.com{link_element.get_attribute('href')}" if link_element else "N/A"
            location = location_element.inner_text().strip() if location_element else "N/A"
            easy_apply = "Yes" if easy_apply_element and "Easy Apply" in easy_apply_element.inner_text() else "No"

            print(f"🔍 Scraped: {title} at {company} ({link}) - {location} | Easy Apply: {easy_apply}")

            save_job_to_db(title, company, link, location, easy_apply)

        browser.close()
        print("✅ Job scraping completed!")

# Run Scraper
if __name__ == "__main__":
    scrape_jobs("Azure Data Engineer", "New Delhi", max_jobs=5)
