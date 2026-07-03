"""
Author: Jose Camacho
a City of Fresno jobs scraper using BeautifulSoup
no javascript loading, so this can be directly scraped from the url
"""

from bs4 import BeautifulSoup
import requests
import pytest

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',
    'Connection': 'close'
}
cof_url = 'https://www.fresno.gov/personnel/jobs/'

@pytest.mark.asyncio
async def test_scrape_cof_jobs():
    jobdata = requests.get(cof_url, headers=HEADERS)
    jobdata.raise_for_status()

    soup = BeautifulSoup(jobdata.text, 'html.parser')
    print(f'Attempting to find info for City of Fresno Jobs...')

    all_job_titles = soup.find_all('span', class_='neogov-jobs-title')
    job_title_amount = len(all_job_titles)
    print(f'Displaying all jobs found ({job_title_amount})\n')
    for job in all_job_titles:
        url = job.find('a').get('href')
        if url and not url.startswith('http'):
            url = f'https://www.fresno.gov{url}'

        print(f'{job.find('a').text}')
        print(f'-- {url}')


