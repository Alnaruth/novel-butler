from requests import HTTPError

from novel_butler import NovelButtler


from googleapiclient.discovery import build
import pprint

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']



def main():
    nb = NovelButtler(headless=False)
    nb.search_novel('only I level up')

def test():
    my_cse_id = ''
    my_api_key = ''
    results = google_search(
        'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=1)
    for result in results:
        pprint.pprint(result)
if __name__ == '__main__':
    test()
