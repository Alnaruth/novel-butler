from novel_butler import NovelButler

download_list = [
    {
        'title': 'Only I level up',
        'first_chapter_url': 'https://freewebnovel.com/only-i-level-up-novel/chapter-1.html',
        'chapter_limit': None
    },
    {
        'title': 'Death guns in another world',
        'first_chapter_url': 'https://freewebnovel.com/death-guns-in-another-world/chapter-1.html',
        'chapter_limit': 500
    },
    {
        'title': 'Level up legacy',
        'first_chapter_url': 'https://freewebnovel.com/level-up-legacy/chapter-2.html',
        'chapter_limit': 500
    }
]


def main():
    nb = NovelButler()

    for book in download_list:
        nb.get_novel(title=book['title'], first_chapter_url=book['first_chapter_url'],
                     chapter_limit=book['chapter_limit'], site='FreeWebnovel')


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
