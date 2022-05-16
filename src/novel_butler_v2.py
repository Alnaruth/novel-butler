import credentials
from googleapiclient.discovery import build
from pprint import pprint

class NovelButler:
    api_key = credentials.api_key
    search_engine_id = credentials.search_engine_id

    def __init__(self):
        pass

    def _google_search(self, query, **kwargs):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=query, cx=self.search_engine_id, **kwargs).execute()
        return res

    def search_novel(self, title):
        results = self._google_search(title, num=5)
        pprint(results['items'])
