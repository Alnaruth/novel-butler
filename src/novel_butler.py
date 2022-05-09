import logging
import time
import os
import traceback

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

from googlesearch import search
import requests, json

# local module imports
import utils
from exceptions import UnsupportedBrowserException

# site handlers
from noveltop1 import Noveltop1
from novel_saver import NovelSaver
from ligthNovelPub import LightNovelPub


class NovelButtler:
    headless_browser = False
    site_list = [
        {
            'url': 'noveltop1.com',
            'handler': Noveltop1
        },
        {
            'url': 'lightnovelpub.com',
            'handler': LightNovelPub
        }
    ]
    google_open = False
    connection_timeout = 2

    def __init__(self, browser='chrome', log_level='info', headless=True):
        self.headless_browser = headless
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
            self.browser.maximize_window()
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
            result = WebDriverWait(self.browser, timeout=self.connection_timeout).until(
                EC.presence_of_element_located((search_by, parameter)))
        except TimeoutException:
            return -1
        return result

    def _google_search(self, text_to_search):
        if not self.google_open:
            self._open_google()
        search = self._browser_wait(By.NAME, 'q')
        if isinstance(search, int) and search == -1:
            return search
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
        status = self._google_search(query)
        if isinstance(status, int) and status < 0:
            return status
        url = self._browser_wait(By.CLASS_NAME, self.utils.first_classname)
        return url

    def _check_directory(self, title):
        dir_path = '../books/' + title
        if os.path.isdir(dir_path):
            return None, -1
        else:
            os.mkdir(dir_path)
        return dir_path, 0

    def _get_element_url(self, element) -> str:
        url = self.browser.current_url

        headers = {
            'User-agent':
                "useragent"
        }
        html = requests.get('https://www.google.com/search?q=hello', headers=headers).text
        #soup = BeautifulSoup(html, 'lxml')
        # locating div element with a tF2Cxc class
        # calling for <a> tag and then calling for 'href' attribute
        #link = soup.find('div', class_='tF2Cxc').a['href']
        return html
    # ACCESSIBLE METHODS

    def test_browser(self, url='https://www.google.com'):
        self._open_google()
        self._google_search('google search through python')
        input()

    def search_novel(self, title, oneshot_search=False):
        logging.info('Searching for the novel "{}"'.format(title))
        search_results = []
        query = '{} site:{}'
        if oneshot_search:
            sites = [self.site_list[0]]
        else:
            sites = self.site_list.copy()

        for site in sites:
            obj = site['handler'](self.browser)
            site_url = site['url']
            first_result = self._search_for_site(query.format(title, site_url))
            if isinstance(first_result, int) and first_result == -1:
                continue
            first_result_url = self._get_element_url(first_result)
            print(f'result url {first_result_url}')
            exit()
            title, last_chapter, first_chapter_url = obj.handle_search(first_result)
            search_result = {'site': site_url, 'title': title.lower(), 'last_chapter': last_chapter,
                             'first_chapter_url': first_chapter_url}
            search_results.append(search_result)
        return search_results

    def download_novel(self, site_info, starting_chapter=0, ending_chapter=None):
        obj = None
        status_code = 0
        try:
            dir_path, status_code = self._check_directory(title=site_info['title'])
        except Exception as e:
            logging.error('Unknown exception' + traceback.format_exc())
            return status_code
        if status_code < 0:
            return status_code

        output_path = dir_path

        for site in self.site_list:
            if site['url'] == site_info['site']:
                obj = site['handler'](self.browser)
                break
        if obj is None:
            logging.error('no match between selected site and site handlers')
        text = obj.get_text(site_info, starting_chapter=starting_chapter, ending_chapter=ending_chapter)

        novel_saver = NovelSaver()
        print(site_info)
        novel_saver.save_epub(text=text, path=output_path, title=site_info['title'])
        return status_code

    def menu(self, novel_to_search=None):
        self._print_intro()
        if novel_to_search is None:
            novel_to_search = input('Insert novel to search: ')
        results = self.search_novel(novel_to_search)
        row_template = '{0:<30}{1:<20}{2:<10}'
        if len(results) == 0:
            print('NO RESULT FOUND IN ANY SITE')
            return
        print('Risultati: \n' + row_template.format('TITLE', 'SITE', 'LAST CHAPTER'))
        for result in results:
            print(row_template.format(result['title'], result['site'], result['last_chapter']))

    def _print_intro(self):
        with open('../images/icon_1.txt') as icon:
            print(icon.read())
        with open('../images/logo.txt') as logo:
            print(logo.read())

        print('\n\n')
