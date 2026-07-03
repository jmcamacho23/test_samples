from playwright.async_api import async_playwright
import pytest

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
AMAZON_URL = 'https://amazon.com'

@pytest.mark.asyncio
async def test_simple_amazon_search():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=1000)
        page = await browser.new_page()
        await page.set_extra_http_headers(USER_AGENT)
        await page.goto(AMAZON_URL)
        print(f"Page title is {await page.title()}")
        await browser.close()

