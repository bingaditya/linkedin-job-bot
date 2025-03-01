from playwright.sync_api import sync_playwright
import sqlite3
import time
from fill_fields import fill_additional_fields

# Function to automate LinkedIn Easy Apply
def apply_to_jobs():
    conn = sqlite3.connect("D:\linkedin-job-bot\jobs.db")
    cursor = conn.cursor()
    
    # Fetch job links where Easy Apply is available
    cursor.execute("SELECT link FROM jobs WHERE applied = 0")
    jobs = cursor.fetchall()

    if not jobs:
        print("⚠️ No Easy Apply jobs found!")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for silent execution
        page = browser.new_page()

        # 1️⃣ **Login to LinkedIn**
        page.goto("https://www.linkedin.com/login")
        page.fill("#username", "cusat.adityaraj@gmail.com")  # 🔹 Replace with your LinkedIn email
        page.fill("#password", "Anandi@14021998")  # 🔹 Replace with your LinkedIn password
        page.click("button[type='submit']")
        time.sleep(5)  # Wait for login

        for job in jobs:
            job_link = job[0]
            print(f"🔵 Applying to: {job_link}")

            # 2️⃣ **Open Job Page**
            page.goto(job_link)
            time.sleep(5)  # Allow the page to load
            # 3️⃣ **Click "Easy Apply" if available**
           # Wait for the Easy Apply button to appear (max 10s)
            try:
                # Locate all Easy Apply buttons (multiple elements found)
                easy_apply_buttons = page.locator("button.jobs-apply-button")
                print(f"🔍 Found {easy_apply_buttons.count()} Easy Apply buttons.")
                if easy_apply_buttons.count() > 0:
                    easy_apply_button = easy_apply_buttons.nth(1)  # Get the first match
            
                    # Wait for it to become visible & enabled
                    #easy_apply_button.wait_for(state="visible", timeout=15000)
                    easy_apply_button.scroll_into_view_if_needed()
                    easy_apply_button.click()
                    print("✅ Easy Apply button clicked!")
                    time.sleep(3)  # Allow modal to open
                else:
                    print("⚠️ Easy Apply button not found on this page.")
            except Exception as e:
                print(f"❌ Error clicking Easy Apply button: {e}")
            fill_additional_fields(page)
            

            # 4️⃣ **Check for Submit Button & Click**
            submit_button = page.query_selector("button:has-text('Submit application')")
            if submit_button:
                submit_button.click()
                print("✅ Application submitted!")

                # Mark job as applied in the database
                cursor.execute("UPDATE jobs SET applied = 1 WHERE link = ?", (job_link,))
                conn.commit()
            else:
                print("⚠️ Additional form fields detected. Skipping...")

            time.sleep(2)

        browser.close()
        print("🎉 All Easy Apply jobs processed!")

    conn.close()

# Run the automation
apply_to_jobs()
