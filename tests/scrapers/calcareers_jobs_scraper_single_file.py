"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
this gets the list of jobs marked as 'Classified' (based on url vars) and lists them out
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
"""
import re
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

async def scrape_calcareers_jobs():
    # location for Fresno County is 85, but can lose the url var if an update is made in the search
    calcareers_url = 'https://calcareers.ca.gov/CalHRPublic/Search/JobSearchResults.aspx#locid=85'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=1000, args=["--start-maximized"])
        ccpage =  await browser.new_page()
        await ccpage.set_extra_http_headers(user_agent)

        print(f'Going to CalCareers now...')
        await ccpage.goto(calcareers_url, wait_until="networkidle")

        amount_dropdown = ccpage.locator('select[id="cphMainContent_ddlRowCount"]')
        await amount_dropdown.click()
        await amount_dropdown.select_option(value="100")
        county_dropdown = ccpage.locator('td[id="cphMainContent_ddlLocation_B-1"]')
        await county_dropdown.click()
        await county_dropdown.press_sequentially("Fresno County") # since it loses the location id var
        await ccpage.keyboard.press("Enter")
        await ccpage.locator('input[value="Update Results"]').click()

        html_content_for_bs4 = await ccpage.content()
        await browser.close()
        print('Done getting job info from CalCareers')

    calcareers_soup = BeautifulSoup(html_content_for_bs4, 'html.parser')

    calcareers_job_tiles = calcareers_soup.find_all('a', id=re.compile('cphMainContent_rptResults_hlViewJobPosting'))
    count = len(calcareers_job_tiles)
    print(f'CalCareers jobs list ({count}): ')
    if not calcareers_job_tiles:
        print("No jobs found")
        return

    for job in calcareers_job_tiles:
        title = job.text.strip()
        link = job.get('href')

        if link and not link.startswith('http'):
            link = f'https://calcareers.ca.gov{link}'

        print(f'Job Title: {title}')
        print(f'Link: {link}')

if __name__ == "__main__":
    asyncio.run(scrape_calcareers_jobs())
