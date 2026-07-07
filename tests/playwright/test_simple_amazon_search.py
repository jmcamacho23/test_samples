from playwright.async_api import async_playwright
import pytest

UA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',
    'Connection': 'close'
}
URL = 'https://amazon.com'

@pytest.mark.asyncio
async def test_simple_amazon_search():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=1000)
        page = await browser.new_page()
        await page.set_extra_http_headers(UA)
        await page.goto(URL)
        continue_button = page.get_by_role("button", name="Continue Shopping")
        try:
            await continue_button.click(timeout=2000)
            print(f'Button of "Continue Shopping" was present')
        except:
            print('"Continue Shopping" button was not present')
            pass
        print(f"Page title is {await page.title()}")
        searchbox = page.locator("#twotabsearchtextbox")
        await searchbox.fill("Fire TV Stick 4K")
        await searchbox.press("Enter") # initiate search by keyboard input
        await page.locator("div[data-cy='title-recipe']").locator('a').first.click()
        # search for a different item
        await searchbox.fill("Scotts Green Max")
        await page.locator("#nav-search-submit-button").click()  # use search by clicking instead
        await page.locator("h2[aria-label*='Green Max Lawn Food, 33.33 lbs.']").first.click()
        print(f"Page title is now {await page.title()}")
        product_price = page.locator("div[data-feature-name='corePrice']").locator("span[aria-hidden='true']").first
        product_price_text = product_price.text_content()
        print(f'The product price is: {await product_price_text}')
        assert product_price is not None
        # take a whole-page screenshot to verify
        await page.screenshot(path="./screens/amazon_screenshot.png", full_page=True)
        # and take a screenshot of just the price
        await product_price.screenshot(path='./screens/price_screenshot.png')
        await browser.close()

