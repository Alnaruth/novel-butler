from urllib.request import Request, urlopen
from pprint import pprint

from site_handler_interface import SiteHandlerInterface


class Tapas(SiteHandlerInterface):
    first_chap_link = 'https://tapas.io/episode/2403209'

    def __init__(self):
        super().__init__()

    def download_novel(self, first_chap_link=None):
        if first_chap_link is not None:
            self.first_chap_link = first_chap_link

        req = Request(self.first_chap_link, headers={'User-Agent': 'Mozilla/5.0'})
        first_page = urlopen(req)
        print(first_page.read().decode('utf-8'))
