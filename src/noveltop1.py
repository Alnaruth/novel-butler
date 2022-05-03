from site_interface import SiteInterface
import time


class Noveltop1(SiteInterface):
    next_chapter_id = 'next_chap'
    chapter_content_id = 'chr-content'

    def __init__(self, browser):
        super().__init__(browser)
        self.url = 'noveltop1.com'

    def handle_search(self, page):
        title = self._get_title(page)
        first_url = self.browser.current_url
        latest_chapter = self._get_latest_chapter()

        return title, latest_chapter, first_url

    def get_text(self, infos, starting_chapter=1, ending_chapter=None):
        self.browser.get(infos['first_chapter_url'])

        text = ""

        chapter_count = 1
        previous_url = None
        current_url = self.browser.current_url

        while current_url != previous_url and starting_chapter <= chapter_count <= ending_chapter:
            text += self.browser.find_element(self.By.ID, self.chapter_content_id).text
            chapter_count += 1
            previous_url = current_url
            next_chapter_button = self.browser.find_element(self.By.ID, self.next_chapter_id)
            next_chapter_button.click()
            current_url = self.browser.current_url
        return text

    def _get_latest_chapter(self):
        page = self._browser_wait(self.By.XPATH, "//div[@id='chr-nav-top']//button[@type='button']")
        page.click()
        page = self._browser_wait(self.By.XPATH, "//div[@id='chr-nav-top']//select")
        chapter_list = page.text.split('\n')
        return chapter_list[-1]

    def _get_title(self, page):
        page.click()
        page = self._get_title_from_chapter()
        title_found = None
        if page is not None:
            title_found = page.text
        if title_found is None:
            self._goto_chapter()
            title_found = self._get_title_from_chapter().text
        return title_found

    def _get_title_from_chapter(self):
        return self._browser_wait(self.By.CLASS_NAME, 'novel-title', ignore_timeout=True)

    def _goto_chapter(self):
        page = self._browser_wait(self.By.ID, 'tab-chapters-title')
        page.click()
        time.sleep(3)
        page = self._browser_wait(self.By.XPATH, "//ul[@class='list-chapter']//span[@class='nchr-text']", timeout=10)
        page.click()
