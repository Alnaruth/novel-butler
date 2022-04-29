from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import logging


class SiteInterface:
    connection_timeout = 2

    def __init__(self, browser):
        self.browser = browser
        self.url = None
        self.By = By

    def _browser_wait(self, search_by, parameter, ignore_timeout=False):
        result = None
        try:
            result = WebDriverWait(self.browser, timeout=self.connection_timeout).until(
                EC.presence_of_element_located((search_by, parameter)))
        except TimeoutException:
            if not ignore_timeout:
                logging.error('Connection to {} timed out'.format(self.url))
                self._exit()
        return result

    def _exit(self):
        logging.critical('Exiting')
        exit()
