import credentials
from googleapiclient.discovery import build
from exceptions import NoResultsSearchException

class SiteHandlerInterface:
    api_key = credentials.api_key
    search_engine_id = credentials.search_engine_id

    def __init__(self):
        pass

    def _google_search(self, query, **kwargs):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=query, cx=self.search_engine_id, **kwargs).execute()

        # check if search bore results
        if res['searchInformation']['totalResults'] == '0':
            raise NoResultsSearchException()
        return res

    def _test_search(self, title):
        results = self._google_search(title, num=10)
        for result in results['items']:
            print(result['link'])

    '''
        receives a title (site url not included) e.g. "solo leveling"
        returns a dict with this format:
            {
                'title': '...'
            }
        or None if there are no results
    '''
    def search_novel(self, title):
        pass
