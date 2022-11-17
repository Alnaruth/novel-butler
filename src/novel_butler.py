import freewebnovel
import file_saver


class NovelButler:
    _supported_sites = {'FreeWebnovel': freewebnovel.NovelDownloader()}

    def get_novel(self, title, first_chapter_url, site, chapter_limit=None):
        if site not in self._supported_sites:
            print('Selected site is not supported!')
            return None

        chapters = self._supported_sites[site].download_novel(title=title, url=first_chapter_url, limit=chapter_limit)
        file_saver.save_novel(title, chapters)
