"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
this gets the list of jobs marked as 'Classified' (based on url vars) and lists them out
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
this is a single-file approach
"""

from bs4 import BeautifulSoup
import asyncio
import pytest
from playwright.async_api import async_playwright

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
fusd_url = 'https://www.edjoin.org/FresnoUnified?rows=10&page=1&catID=3&districtID=134'

@pytest.mark.asyncio
async def test_scrape_fusd_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        fusd_page =  await browser.new_page()
        await fusd_page.set_extra_http_headers(user_agent)

        print(f'Going to FUSD EdJoin now...')
        await fusd_page.goto(fusd_url, wait_until="networkidle")

        html_content_for_bs4 = await fusd_page.content()
        await browser.close()

    fusd_soup = BeautifulSoup(html_content_for_bs4, 'html.parser')

    fusd_job_tiles = fusd_soup.find_all('a', attrs={"data-postingid": True})
    sorted_tiles = sorted(fusd_job_tiles, key=lambda tag: tag.text.strip())
    print('FRESNO Unified jobs list: ')
    if not fusd_job_tiles:
        print("No jobs found")
        return

    for job in sorted_tiles:
        title = job.text.strip()
        link = job.get('href')

        if link and not link.startswith('http'):
            link = f'https://edjoin.org{link}'

        print(f'{title}')
        print(f'-- {link}')
