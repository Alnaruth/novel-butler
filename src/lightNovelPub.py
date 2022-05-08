from site_interface import SiteInterface


class LightNovelPub(SiteInterface):
    next_chapter_class = 'nextchap'
    chapter_content_id = 'chapter-container'

    def __init__(self, browser):
        super().__init__(browser)

    # returns title, last_chapter, first_chapter_url
    def handle_search(self, page):
        page.click()
        cookie_element = self._browser_wait(self.By.CLASS_NAME, 'css-47sehv')
        cookie_element.click()
        page = self._get_title_from_chapter()
        title_found = None
        if page is not None:
            title_found = page.text
            page.click()
        if title_found is None:
            page = self._browser_wait(self.By.CLASS_NAME, 'novel-title text2row')
            title_found = page.text
        page = self._browser_wait(self.By.ID, 'readchapterbtn')
        last_chapter = self._browser_wait(self.By.CLASS_NAME, 'header-stats').text
        last_chapter = last_chapter.split('\n')[0]
        first_chapter_url = page.get_attribute('href')

        return title_found, last_chapter, first_chapter_url

    # returns text as string
    def get_text(self, infos, starting_chapter=1, ending_chapter=None):
        self.browser.get(infos['first_chapter_url'])
        text = ""

        chapter_count = 1
        previous_url = None
        current_url = self.browser.current_url
        while current_url != previous_url and starting_chapter <= chapter_count and (
                ending_chapter is None or chapter_count <= ending_chapter):
            text += self.browser.find_element(self.By.ID, self.chapter_content_id).text
            chapter_count += 1
            previous_url = current_url
            next_chapter_button = self.browser.find_element(self.By.ID, self.next_chapter_class)
            next_chapter_button.click()
            current_url = self.browser.current_url
        return text

    def _get_title_from_chapter(self):
        return self._browser_wait(self.By.CLASS_NAME, 'booktitle', ignore_timeout=True)
