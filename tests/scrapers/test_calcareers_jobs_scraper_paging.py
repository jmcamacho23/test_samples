"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
this is a single-file approach to searching a page with multiple results and paging through them to get
them all using Playwright, and then BeautifulSoup to parse
"""
import re
import pytest
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_calcareers_jobs_scraper_paging():
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    calcareers_url = 'https://calcareers.ca.gov/CalHRPublic/Search/JobSearchResults.aspx#empty'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800, args=["--start-maximized"]) # needs to be slowed because of their animation delays
        ccpage =  await browser.new_page(no_viewport=True)
        await ccpage.set_extra_http_headers(user_agent)

        print(f'Going to CalCareers now...')
        await ccpage.goto(calcareers_url, wait_until="networkidle")
        try:
            toast = ccpage.locator("div[class='toast-title']")
            await toast.click()
        except IndexError():
            pass

        amount_dropdown = ccpage.locator('select[id="cphMainContent_ddlRowCount"]')
        await amount_dropdown.click()
        await amount_dropdown.select_option(value="100")
        refine_icon = ccpage.locator('#filterIcon')
        await refine_icon.click()
        posted_within_dropdown = ccpage.locator('td[id="cphMainContent_ddlPostedInLast_B-1"]')
        await posted_within_dropdown.click()
        await posted_within_dropdown.press_sequentially("7 Days", delay=0) # since it loses the location id var
        await ccpage.keyboard.press("Enter")
        work_type_dropdown = ccpage.locator('td[id="cphMainContent_ddlWorkType_B-1"]')
        await work_type_dropdown.click()
        await work_type_dropdown.press_sequentially("Permanent", delay=0)
        await ccpage.keyboard.press("Enter")
        schedule_dropdown = ccpage.locator('td[id="cphMainContent_ddlWorkSchedlue_B-1"]')
        await schedule_dropdown.click()
        await schedule_dropdown.press_sequentially("Fulltime", delay=0)
        await ccpage.keyboard.press("Enter")
        await ccpage.locator('input[value="Update Results"]').click()

        job_listings = [await ccpage.content()]

        paging_present = ccpage.locator('div[id="paging"]')
        await paging_present.click()
        paging_amount = (await ccpage.locator('div.pagination a').count()-1) # since we are not clicking on page 1
        for page in range(1,paging_amount): # start after page 1
            page_to_click = page+1
            await ccpage.locator('div[id="paging"]').locator('a').nth(page_to_click).click()
            job_listings.append(await ccpage.content())
        all_one_job_td = "|||".join(job_listings)
        await browser.close()
        print('Done getting job info from CalCareers')

    # now that all pages are joined, parse the results of all those pages
    calcareers_soup = BeautifulSoup(all_one_job_td, 'html.parser')

    calcareers_job_tiles = calcareers_soup.find_all('div', id=re.compile('cphMainContent_rptResults_pnlCardContainer'))
    sorted_jobs = sorted(calcareers_job_tiles, key=lambda tag: tag.text.strip())
    print(f'CalCareers jobs list ({len(calcareers_job_tiles)}): ')
    if not calcareers_job_tiles:
        print("No jobs found")
        return

    for job in sorted_jobs:
        title = job.find('a', id=re.compile('cphMainContent_rptResults_hlViewJobPosting')).text
        actual_title = job.find('div', class_='working-title details row').find_all('div')[1].text.strip()
        link = job.find('a', id=re.compile('cphMainContent_rptResults_hlViewJobPosting')).get('href').strip()
        pay = job.find('div', class_='salary-range details row').find_all('div')[1].text.strip()
        schedule = job.find('div', class_='schedule details row').find_all('div')[1].text.strip()
        work_place = job.find('div', class_='telework details row').find_all('div')[1].text.strip()


        if link and not link.startswith('http'):
            link = f'https://calcareers.ca.gov{link}'

        print(f'{title} ({actual_title}) | {pay} | {schedule} | {work_place}')
        print(f'-- {link}')
