from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

import time
import logging


class SiteInterface:
    connection_timeout = 2

    def __init__(self, browser):
        self.browser = browser
        self.url = None
        self.By = By

    def _browser_wait(self, search_by, parameter, ignore_timeout=False, timeout=None):
        result = None
        if timeout is None:
            timeout = self.connection_timeout
        try:
            result = WebDriverWait(self.browser, timeout=timeout).until(
                EC.presence_of_element_located((search_by, parameter)))

        except TimeoutException:
            if not ignore_timeout:
                logging.error('Connection to {} timed out'.format(self.url))
                self._exit()
        except NoSuchElementException:
            logging.error('element {} not found in the page'.format(parameter))
            self._exit()
        return result

    def _unsafe_get_element(self, search_by, parameter):
        return self.browser.find_element(search_by, parameter)

    def _exit(self):
        logging.critical('Exiting')
        exit()

    # returns title, last_chapter, first_chapter_url
    def handle_search(self, page):
        pass

    # returns text as string
    def get_text(self, info, starting_chapter=0, ending_chapter=None):
        pass
