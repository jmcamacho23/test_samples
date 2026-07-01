import cusd_jobs_scraper_with_playwright as scraper
import asyncio

def run_the_scraper():
    print(f'Running the Edjoin scraper')

    asyncio.run(scraper.scrape_cusd_jobs())

    print(f'Scaper script should be done!')

if __name__ == "__main__":
    run_the_scraper()