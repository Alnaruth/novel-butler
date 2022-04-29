import logging
import time

# web navigation imports
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# local module imports
import utils
from exceptions import UnsupportedBrowserException

# site handlers
from site_interface import SiteInterface
from noveltop1 import Noveltop1


class NovelButtler:
    headless_browser = False
    site_list = [
        {
            'url': 'noveltop1.com',
            'handler': Noveltop1
        }
    ]
    google_open = False
    connection_timeout = 2

    def __init__(self, browser='chrome', log_level='info'):
        self.utils = utils.Utils()
        self._init_logging(log_level)
        self._init_driver(browser)

    def _init_logging(self, log_level):
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
        utils.clear()
        if not browser_driver or not browser_options:
            logging.error('Unknown error initializing web divers')
            return

    def _open_google(self):
        self.browser.get('https://www.google.com')

        # check for button to accept before searching
        button_id = 'L2AGLb'
        button = self.browser.find_element(By.ID, button_id)
        button.click()
        self.google_open = True

    def _browser_wait(self, search_by, parameter):
        result = None
        try:
            result = WebDriverWait(self.browser, timeout=self.connection_timeout).until(EC.presence_of_element_located((search_by, parameter)))
        except TimeoutException:
            logging.error('Connection to google.com timed out')
            self._exit()
        return result

    def _google_search(self, text_to_search):
        if not self.google_open:
            self._open_google()
        search = self._browser_wait(By.NAME, 'q')
        # search = self.browser.find_element(By.NAME, 'q')
        search.send_keys(text_to_search)
        search.send_keys(Keys.RETURN)
        return search

    def _exit(self):
        logging.critical('Exiting')
        exit()

    # Scan for novel

    def _search_for_site(self, query):
        if not self.google_open:
            self._open_google()
        self._google_search(query)
        url = self._browser_wait(By.CLASS_NAME, self.utils.first_classname)
        return url

    # ACCESSIBLE METHODS

    def test_browser(self, url='https://www.google.com'):
        self._open_google()
        self._google_search('google search through python')
        input()

    def search_novel(self, title, oneshot_search=False):
        logging.info('Searching for the novel "{}"'.format(title))

        query = '{} site:{}'
        if oneshot_search:
            sites = [self.site_list[0]]
        else:
            sites = self.site_list.copy()

        for site in sites:
            obj = site['handler'](self.browser)
            site_url = site['url']
            first_result = self._search_for_site(query.format(title, site_url))
            obj.handle_search(first_result)
