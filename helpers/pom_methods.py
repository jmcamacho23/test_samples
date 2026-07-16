from playwright.async_api import Page, Locator
from support import vars


class Ccsearch:
    def __init__(self, page: Page):
        self.page = page
        self.toast: Locator = page.locator("div.toast-title")
        self.refine_icon: Locator = page.locator("#filterIcon")

    async def navigate(self):
        print(f'Going to URL at : {vars.CCSEARCHPAGEURL}')
        await self.page.goto(vars.CCSEARCHPAGEURL, wait_until="networkidle")

    async def check_for_toast(self):
        try:
            if await self.toast.is_visible(timeout=2000):
                await self.toast.click()
                print(f'Toast was present and closed')
        except Exception:
            print('No toast was present')

    async def open_advanced_search(self):
        print('Opening Advanced search options')
        await self.refine_icon.click()