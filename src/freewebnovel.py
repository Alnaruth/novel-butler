# test url: https://freewebnovel.com/only-i-level-up-novel/chapter-1.html
import time
from sys import *
import re
from pprint import pprint
from abstract_novel_downloader import AbstractNovelDownloader

class NovelDownloader(AbstractNovelDownloader):
    _test_url = 'https://freewebnovel.com/only-i-level-up-novel/chapter-1.html'
    _headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    _base_url = 'https://freewebnovel.noveleast.com'

    def download_novel(self, title, url, limit=None, chapter_offset=0):
        current_chapter = chapter_offset

        keep_downloading = True
        throttle_value = 0

        chapters = []

        print(f'\n\t\tStarting download of the novel {title}...\n')

        while keep_downloading:
            current_chapter += 1
            print('\rCurrently downloading chapter: ', str(current_chapter), end='')
            retry = True
            content = None
            max_retries = 50
            while retry and max_retries > 0:
                time.sleep(throttle_value)
                status, content = self._get_page_content(url)
                if status is None:
                    print('Connection error, stopping now')
                    return chapters
                if status == 429:
                    max_retries -= 1
                    throttle_value += 0.01
                else:
                    throttle_value -= (0.001/(current_chapter-chapter_offset))
                    if throttle_value < 0:
                        throttle_value = 0
                    retry = False
                if status == 404:
                    print(f'url not found: {url}')
                    return None
            text, next_url = self._mine_data(content)
            if text is not None:
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


    def _get_page_content(self, url, retries_counter=0):
        try:
            response = super()._get_request(url=url, headers=self._headers)
        except:
            if retries_counter > 10:
                return None, None
            return self._get_page_content(url, retries_counter + 1)

        if response.status_code == 200:
            return 200, response.text
        elif response.status_code != 429:
            print('Error ', response.status_code)
        return response.status_code, None

    def _mine_data(self, content):
        text = self._mine_text(content)
        if text is None:
            return None, None
        text = self._sanitize_text(text)

        next_url = self._find_next_chapter(content)
        return text, next_url

    def _find_next_chapter(self, content):
        page = content.split('<')
        for line in page:
            if 'href' in line and '"next_url"' in line:
                sections = line.split('"')
                for section in sections:
                    if '/' in section:
                        if 'bednovel' in section.lower():
                            return section
                        elif 'libread' in section.lower():
                            #self._base_url = self._base_url.replace('bednovel/', 'libread')
                            return section
                        elif 'chapter-' in section:
                            return section
        return None

    def _sanitize_text(self, text: str):
        text = self._remove_script_tags(text) # must remove before other html tags
        text = self._remove_html_tags(text)
        text = self._replace_special_chars(text)

        return text


    def _replace_special_chars(self, text: str):
        special_chars = {
            '&lt;': '<',
            '&gt;': '>',
            ',': ',',
            '’': '\'',
            '“': '"',
            '”': '"',
            '𝙡𝓲𝙗𝒓𝙚𝓪𝙙.𝒄𝒐𝙢': '',
            '𝓁𝘪𝑏𝓇𝑒𝑎𝑑.𝑐𝘰𝑚': '',
            '𝙡𝙞𝙗𝒓𝙚𝓪𝙙.𝒄𝓸𝓶': '',
            '𝙡𝙞𝓫𝙧𝙚𝓪𝒅.𝒄𝒐𝓶': ''
        }
        for key, value in special_chars.items():
            text = text.replace(key, value)
        return text

    def _remove_html_tags(self, text: str):
        script_tag_regex = '<script>.*?<\/script>'
        html_tag_regex = '<(?:"[^"]*"[\'"]*|\'[^\']*\'[\'"]*|[^\'">])+>'
        text = re.sub(html_tag_regex, '', text)
        #text = re.sub(script_tag_regex, '', text)
        return text

    def _remove_script_tags(self, input_string):
        string = input_string
        while True:
            start_index = string.find("<script")
            if start_index == -1:
                break  # No more "<script>" tags found, exit loop
            end_index = string.find("</script>", start_index)
            if end_index == -1:
                break  # No corresponding "</script>" tag found, exit loop
            string = string[:start_index] + string[end_index + len("</script>"):]
        return string

    def _legacy_mine_text(self, content):
        split_content = content.split('class="chapter-start"')
        if len(split_content) < 2:
            return None
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

    def _mine_text(self, content):
        split_content = content.split('<div id="article">')
        if len(split_content) < 2:
            return None
        chapter_body = split_content[1].split('<div class="chapter-end"></div>')[0]

        paragraphs = chapter_body.split('<p>')
        result = ''
        for paragraph in paragraphs:
            if paragraph is None or paragraph == '':
                continue
            result += paragraph
            result += '\n\n\r'
        return result

    def test(self):
        content = self._get_page_content(self._test_url)
        if not content:
            return None
        print("content: ", content)
        result = self._mine_data(content)
        pprint(result)


def test_downloader():
    nd = NovelDownloader()
    chapters = nd.download_novel('solo leveling', 'https://freewebnovel.com/only-i-level-up-novel/chapter-1.html', 1)
    i = 0
    for chapter in chapters:
       i += 1
       print(f'CHAPTER {i}:\n {chapter}\n\n\n')

if __name__ == '__main__':
    test_downloader()