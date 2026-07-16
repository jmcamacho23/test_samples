"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
"""


from playwright.async_api import Page, expect
from helpers.pom_methods import Ccsearch


#@pytest.mark.asyncio(loop_scope="function")
async def test_calcareers_jobs_pom(page: Page):
   cc_search = Ccsearch(page)

   await cc_search.navigate()
   await cc_search.check_for_toast()
   await cc_search.open_advanced_search()