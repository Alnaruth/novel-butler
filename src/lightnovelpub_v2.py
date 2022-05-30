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
'''
testabfdb

'''
import time

class LightNovelPub:
    first_chap_url = ''
    def __init__(self):
        browser_driver = ChromeDriverManager().install()
        browser_options = ChromeOptions()
        browser_options.headless = False
        self.browser = Chrome(service=Service(browser_driver), options=browser_options)

    def download_novel(self):
        self.browser.get(self.first_chap_url)
        self.browser.maximize_window()
        agree_button = self.browser.find_element(By.CLASS_NAME, value='css-1hy2vtq')
        agree_button.click()
        text = ''
        chapter_counter = 1
        last_chapter = False
        while not last_chapter and chapter_counter < 3:
            text += f'\n\nCHAPTER{chapter_counter}\n\n'
            chapter_content = self.browser.find_element(By.ID, value='chapter-container').text
            text += chapter_content
            xpath = "//a//span[text()='Next']"
            next_button = self.browser.find_element(By.CLASS_NAME, value='nextchap')
            last_chapter = not next_button.is_enabled()
            if not last_chapter:
                next_url = next_button.get_attribute('href')
                self.browser.get(next_url)
                input()
                '''
                try:
                    next_button.click()
                except ElementClickInterceptedException:
                    try:
                        dismiss_ad_button = self.browser.find_element(By.ID, value='dismiss-button')
                        dismiss_ad_button.click()
                    except NoSuchElementException:
                        time.sleep(10)
                '''
            chapter_counter += 1
        return text


    def test_download(self, url):
        self.first_chap_url = url
        print(self.download_novel())

def main():
    lnp = LightNovelPub()
    lnp.test_download('https://www.lightnovelpub.com/novel/shadow-slave/1365-chapter-1')
    input()
if __name__ == '__main__':
    main()
