# test url: https://freewebnovel.com/only-i-level-up-novel/chapter-1.html

from pprint import pprint
from abstract_novel_downloader import AbstractNovelDownloader

class NovelDownloader(AbstractNovelDownloader):
    _test_url = 'https://freewebnovel.com/death-guns-in-another-world/chapter-1.html'
    _headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    _base_url = 'https://freewebnovel.com'

    def download_novel(self, title, url, limit=None):
        current_chapter = 0

        keep_downloading = True

        chapters = []

        print(f'\t\tStarting download of the novel {title}...\n\n')

        while keep_downloading:
            current_chapter += 1
            print(f'Currently downloading chapter {current_chapter}')
            content = self._get_page_content(url)
            text, next_url = self._mine_data(content)
            chapters.append(text)
            url = next_url

            if current_chapter == limit:
                print('\n\nReached prefixed download limit, stopping...\n\n')
                keep_downloading = False
            elif url is None:
                print('\n\nReached last detectable chapter, stopping... \n\n')
                keep_downloading = False
            else:
                url = self._base_url + url

        return chapters
    def search_novel(self, title):
        body = {

        }
        super()._post_request(self._base_url + '/search/')


    def _get_page_content(self, url):
        response = super()._get_request(url=url, headers=self._headers)
        if response.status_code == 200:
            return response.text
        print('Error ', response.status_code)
        return None

    def _mine_data(self, content):
        text = self._mine_text(content)
        text = self._sanitize_text(text)

        next_url = self._find_next_chapter(content)
        return text, next_url

    def _find_next_chapter(self, content):
        page = content.split('<')
        for line in page:
            if 'href' in line and '"next_url"' in line:
                sections = line.split('"')
                for section in sections:
                    if 'chapter' in section.lower() and '/' in section:
                        return section
        return None

    def _sanitize_text(self, text: str):
        special_chars = {
                '&lt;': '<',
                '&gt;': '>'
            }
        for key, value in special_chars.items():
            text = text.replace(key, value)
        return text

    def _mine_text(self, content):
        split_content = content.split('class="chapter-start"')
        chapter_body = split_content[1].split('class="chapter-end"')[0]

        lines = chapter_body.split('\r')
        paragraphs = []
        for line in lines:
            if '<p>' in line:
                paragraphs.append(line.split('<p>'))

        grouped_paragraphs = []
        for p in paragraphs:
            if '<sub>' not in p[1] and '</p>' not in p[1] and '<h' not in p[1]:
                grouped_paragraphs.append(p[1])
            elif '</p>' in p[1] and '<sub>' not in p[1] and '<h' not in p[1]:
                tmp = p[1].split('</p>')
                grouped_paragraphs.append(tmp[0])

            if len(p) > 2:
                grouped_paragraphs.append(p[2])
        text = ''
        for paragraph in grouped_paragraphs:
            text += paragraph
            text += '\n\n\r'
        return text

    def test(self):
        content = self._get_page_content(self._test_url)
        if not content:
            return None

        result = self._mine_data(content)
        pprint(result)


def test_downloader():
    nd = NovelDownloader()

    chapters = nd.download_novel('solo leveling', 'https://freewebnovel.com/only-i-level-up-novel/chapter-1.html', 2)
    i = 0
    for chapter in chapters:
        i += 1
        print(f'CHAPTER {i}:\n {chapter}\n\n\n')

if __name__ == '__main__':
    test_downloader()