import requests


class AbstractNovelDownloader:
    def download_novel(self, title, url, limit=None):
        self._internal_error()

    def search_novel(self, title):
        self._internal_error()

    def _internal_error(self):
        print("INTERNAL ERROR: download_novel not implemented")
    @staticmethod
    def _get_request(url, headers):
        return requests.get(url, headers=headers)

    @staticmethod
    def _post_request(url, headers, body):
        return requests.post(url, headers=headers, json=body)
