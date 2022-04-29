from site_interface import SiteInterface


class Noveltop1(SiteInterface):
    def __init__(self, browser):
        super().__init__(browser)
        self.url = 'noveltop1.com'

    def handle_search(self, page):
        page.click()
        page = self._browser_wait(self.By.CLASS_NAME, 'novel-title', ignore_timeout=True)
        if page is not None:
            page.click()
        input()
