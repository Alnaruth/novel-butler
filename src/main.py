from novel_butler import NovelButler

download_list = [
    {
        'title': 'ATTICUS\'S ODYSSEY - REINCARNATED INTO A PLAYGROUND',
        'first_chapter_url': 'https://freewebnovel.noveleast.com/atticuss-odyssey-reincarnated-into-a-playground/chapter-1',
        'chapter_limit': 250,
        'chapter_offset': 0
    },{
        'title': 'LORD OF THE MYSTERIES',
        'first_chapter_url': 'https://freewebnovel.noveleast.com/lord-of-the-mysteries/chapter-1',
        'chapter_limit': 250,
        'chapter_offset': 0
    },
]


def main():
    nb = NovelButler()

    for book in download_list:
        nb.get_novel(title=book['title'], first_chapter_url=book['first_chapter_url'],
                     chapter_limit=book['chapter_limit'], site='FreeWebnovel', chapter_offset=book['chapter_offset'])


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
