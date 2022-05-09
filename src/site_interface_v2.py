class SiteInterface:
    def __init__(self):
        pass

    # returns title, last_chapter, first_chapter_url
    def handle_search(self, first_result_url: str) -> tuple:
        pass

    # returns text as string
    def get_text(self, info: dict, starting_chapter=0, ending_chapter=None) -> str:
        pass
