from pprint import pprint

from exceptions import NoResultsSearchException
from site_handler_interface import SiteHandlerInterface


class NovelTop1(SiteHandlerInterface):
    def __init__(self):
        super().__init__()

    def search_novel(self, title):
        try:
            query = title + ' site:tapas.io'
            print(f'searching "{query}"')
            search_results = super()._google_search(query, num=10)
        except NoResultsSearchException as e:
            print('no results')
            return None

        for result in search_results['items']:
            pprint(result['link'])
