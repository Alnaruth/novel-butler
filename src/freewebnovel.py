from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# test for commit
import os
import sys

class FreeWebNovel:
    connection_timeout = 5
    title = ''

    def __init__(self):
        browser_driver = ChromeDriverManager().install()
        browser_options = ChromeOptions()
        browser_options.headless = True
        self.browser = Chrome(service=Service(browser_driver), options=browser_options)
        self.browser.maximize_window()

    def _browser_wait(self, search_by, value):
        result = None
        try:
            result = WebDriverWait(self.browser, timeout=self.connection_timeout).until(
                EC.presence_of_element_located((search_by, value)))
        except TimeoutException:
            return -1
        return result

    def _get_novel_text(self, first_chap_url, limit):
        self.browser.get(first_chap_url)
        last_chap = False
        text = ''
        chap_count = 1
        while not last_chap and (limit is None or limit > chap_count):
            print(f'{self.title}: downloading chapter {chap_count}')
            chap_count += 1
            try:
                text += self._browser_wait(By.CLASS_NAME, value='txt').text
                next_button = self.browser.find_element(By.ID, value='next_url')
                next_button.click()
            except NoSuchElementException:
                last_chap = True
            text += '\n\n\f\n\n'

        return text

    def download_novel(self, first_chap_url, title, limit=None):
        self.title = title
        text = self._get_novel_text(first_chap_url, limit)
        out_path = '../books/' + title.lower().replace(' ', '-')
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        out_path += f'/{title}.txt'
        #text = text.encode(sys.stdout.encoding, errors='replace').
        #print(text)
        with open(out_path, 'w', encoding='utf-8') as file:
            file.write(text)


def main():
    fwn = FreeWebNovel()
    choice = ''

    download_list = [
        {
            'url': 'https://freewebnovel.com/guild-wars/chapter-1.html',
            'title': 'Guild Wars'
        }
    ]

    for download in download_list:
        fwn.download_novel(download['url'], download['title'], limit=500)


if __name__ == '__main__':
    main()
