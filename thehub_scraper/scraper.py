from playwright.sync_api import sync_playwright
import csv
import os


def scrape_thehub_paginated(max_pages=10):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for page_num in range(1, max_pages + 1):
            url = f"https://thehub.io/jobs?countryCode=EU&sorting=mostPopular&page={page_num}"
            print(f"🌐 Visiting page {page_num}: {url}")
            page.goto(url, timeout=60000)

            try:
                page.wait_for_selector("div.card.card-job-find-list", timeout=10000)
                job_cards = page.query_selector_all("div.card.card-job-find-list")

                if not job_cards:
                    print("🚪 No jobs found on this page. Ending scrape.")
                    break

                for card in job_cards:
                    title_el = card.query_selector("span.card-job-find-list__position")
                    info_spans = card.query_selector_all("div.bullet-inline-list span")
                    link_el = card.query_selector("a.card-job-find-list__link")

                    company = info_spans[0].inner_text().strip() if len(info_spans) > 0 else ""
                    location = info_spans[1].inner_text().strip() if len(info_spans) > 1 else ""
                    type_ = info_spans[2].inner_text().strip() if len(info_spans) > 2 else ""

                    job = {
                        "title": title_el.inner_text().strip() if title_el else "",
                        "company": company,
                        "location": location,
                        "type": type_,
                        "url": "https://thehub.io" + link_el.get_attribute("href") if link_el else ""
                    }

                    jobs.append(job)

            except Exception as e:
                print(f"⚠️ Failed on page {page_num}: {e}")
                break

        browser.close()
        return jobs


def save_to_csv(jobs, filename):
    if not jobs:
        print("⚠️ No jobs to save.")
        return

    dir_path = os.path.dirname(filename)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    keys = jobs[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Saved {len(jobs)} jobs to {filename}")
