from site_interface import SiteInterface


class LightNovelPub(SiteInterface):
    def __init__(self, browser):
        super().__init__(browser)

    def handle_search(self, element):
        pass

    def get_text(self, info, starting_chapter=0, ending_chapter=None):
        pass
