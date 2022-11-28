from novel_butler import NovelButler

download_list = [
    {
        'title': 'Guild Wars',
        'first_chapter_url': 'https://freewebnovel.com/guild-wars/chapter-1.html',
        'chapter_limit': 500
    },
    {
        'title': 'Will of Chaos',
        'first_chapter_url': 'https://freewebnovel.com/will-of-chaos/chapter-1.html',
        'chapter_limit': 500
    },
    {
        'title': 'Death... and me',
        'first_chapter_url': 'https://freewebnovel.com/death-and-me/chapter-1.html',
        'chapter_limit': 500
    },
    {
        'title': 'The great mage returns after 4000 years',
        'first_chapter_url': 'https://freewebnovel.com/the-great-mage-returns-after-4000-years/chapter-1.html',
        'chapter_limit': 500
    },
    {
        'title': 'Magi craft Meister',
        'first_chapter_url': 'https://freewebnovel.com/magi-craft-meister/chapter-1.html',
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
