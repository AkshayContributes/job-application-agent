from playwright.sync_api import sync_playwright
import csv
import time
import os

CHROME_USER_DATA_DIR = "/Users/akshaykumarthakur/Library/Application\ Support/Google/Chrome"
PROFILE = "Default"


def launch_browser_with_profile():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=os.path.join(CHROME_USER_DATA_DIR, PROFILE),
            headless=False,
            args=["--start-maximized"]
        )

        page = browser.new_page()
        page.goto("https://wellfound.com/location/europe", timeout=60000)

        input("👉 Login manually & solve any CAPTCHA. Press Enter once the jobs are visible...")

        html = page.content()
        print(html)  # Debug: check what’s loaded

        # Scraping logic can go here once jobs are visible
        browser.close()

def scrape_wellfound_europe_jobs(max_scrolls=10):

    # SET THIS TO YOUR OWN PATH
    CHROME_USER_DATA_DIR = "/Users/akshaykumarthakur/Library/Application\ Support/Google/Chrome"
    PROFILE = "Default"

    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wellfound.com/europe", timeout=60000)


        for _ in range(max_scrolls):
            page.mouse.wheel(0, 10000)
            time.sleep(2)

        print("🔍 Page content snippet:\n", page.content()[:1000])

        job_cards = page.query_selector_all("div.job-listing")

        for card in job_cards:
            title = card.query_selector("div.title").text_content()
            company = card.query_selector("div.company-title").text_content()
            location = card.query_selector("div.location").text_content()
            url_element = card.query_selector("a")

            job = {
                "title": title.inner_text().strip() if title else "Title Not Found",
                "company": company.inner_text().strip() if company else "Company Not Found",
                "location": location.inner_text().strip() if location else "Location Not Found",
                "url": f"https://wellfound.com{url_element.get_attribute('href')}" if url_element else "URL Not Found"
            }

            jobs.append(job)

        breakpoint()
        print(f"🎉 Found {len(jobs)} jobs")
        browser.close()
    
    return jobs

def save_to_csv(jobs, filename):

    dir_path = os.path.dirname(filename)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    if not jobs:
        print("⚠️ No jobs found to save.")
        return

    keys = jobs[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)

def main():
    jobs = scrape_wellfound_europe_jobs()
    save_to_csv(jobs, "wellfound_jobs.csv")
            


        
        

