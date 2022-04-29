import logging

# web navigation imports
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# local module imports
import utils
from exceptions import UnsupportedBrowserException


class NovelButtler:
    headless_browser = False

    def __init__(self, browser='chrome', log_level='info'):
        self.utils = utils.Utils()
        self._logging_init(log_level)
        self._init_driver(browser)

    def _logging_init(self, log_level):
        log_level = log_level.upper()
        pre_init_log = ''
        if log_level not in self.utils.log_levels:
            log_level = 'INFO'
            pre_init_log = 'The logging level given is illegal, allowed levels are: {}, defaulting to INFO'.format(
                self.utils.log_levels)
        logging.basicConfig(level=self.utils.log_levels[log_level])
        if pre_init_log != '':
            logging.info(pre_init_log)

    def _init_driver(self, browser_str):
        logging.debug('Initializing web drivers')
        if browser_str not in self.utils.supported_browsers:
            raise UnsupportedBrowserException()
        browser_driver = None
        browser_options = None
        if browser_str == 'chrome':
            browser_driver = ChromeDriverManager().install()
            browser_options = ChromeOptions()
            browser_options.headless = self.headless_browser
            self.browser = Chrome(service=Service(browser_driver), options=browser_options)
        if not browser_driver or not browser_options:
            logging.error('Unknown error initializing web divers')
            return

    def test_browser(self, url='https://www.google.com'):
        self.open_google()
        self.search()
        input()

    def open_google(self):
        self.browser.get('https://www.google.com')

        # check for button to accept before searching
        button_id = 'L2AGLb'
        button = self.browser.find_element(By.ID, button_id)
        button.click()

    def search(self):
        search = self.browser.find_element(By.NAME, 'q')
        search.send_keys("google search through python")
        search.send_keys(Keys.RETURN)
