import freewebnovel
import file_saver
from pprint import pprint

class NovelButler:
    _supported_sites = {'FreeWebnovel': freewebnovel.NovelDownloader()}

    def get_novel(self, title, first_chapter_url, site, chapter_limit=None, test=False):
        if site not in self._supported_sites:
            print('Selected site is not supported!')
            return None

        chapters = self._supported_sites[site].download_novel(title=title, url=first_chapter_url, limit=chapter_limit)
        if not test:
            file_saver.save_novel(title, chapters)
        else:
            return chapters


def test_get_freewebnovel():
    nb = NovelButler()
    chaps = nb.get_novel('Death guns', 'https://freewebnovel.com/death-guns-in-another-world/chapter-1.html', 'FreeWebnovel',
                 chapter_limit=2, test=True)
    pprint(chaps)


def main():
    test_get_freewebnovel()


if __name__ == '__main__':
    main()
