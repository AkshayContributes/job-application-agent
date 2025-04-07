from thehub_scraper.scraper import scrape_thehub_paginated, save_to_csv

if __name__ == "__main__":
    jobs = scrape_thehub_paginated()
    save_to_csv(jobs, "output/thehub_jobs.csv")
    print(f"✅ Scraped {len(jobs)} jobs from TheHub.io")
