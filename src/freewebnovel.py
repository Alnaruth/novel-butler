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

import os


class FreeWebNovel:
    connection_timeout = 5

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

    def _get_novel_text(self, first_chap_url):
        self.browser.get(first_chap_url)
        last_chap = False
        text = ''
        chap_count = 1
        while not last_chap:
            print('downloading chapter ', chap_count)
            chap_count += 1
            try:
                text += self._browser_wait(By.CLASS_NAME, value='txt').text
                next_button = self.browser.find_element(By.ID, value='next_url')
                next_button.click()
            except NoSuchElementException:
                last_chap = True
            text += '\n\n\f\n\n'

        return text

    def download_novel(self, first_chap_url, title):
        text = self._get_novel_text(first_chap_url)
        out_path = '../books/' + title.lower().replace(' ', '-')
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        out_path += f'/{title}.txt'
        with open(out_path, 'w') as file:
            file.write(text)

def main():
    fwn = FreeWebNovel()
    fwn.download_novel('https://freewebnovel.com/shadow-slave/chapter-1.html', 'Shadow Slave')


if __name__ == '__main__':
    main()
