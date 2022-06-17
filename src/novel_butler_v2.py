from noveltop1 import NovelTop1
from tapas import Tapas

class NovelButler:
    supported_sites = [
        {
            'url': 'www.noveltop1.com',
            'handler': NovelTop1()
        }
    ]

    def __init__(self):
        pass

    def search_novel(self, title):
        results = []
        for site in self.supported_sites:
            results.append(site['handler'].search_novel(title))

    def download_novel(self):
        tapas = Tapas()
        tapas.download_novel()