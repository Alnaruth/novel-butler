from novel_butler import NovelButtler


def main():
    nb = NovelButtler(headless=True)
    #result = nb.search_novel('seoul station necromancer')
    #result = nb.search_novel('only i level up')

    #chosen_site = result[0]
    #status_code = nb.download_novel(chosen_site, ending_chapter=1)

    #print(text)

    while True:
        nb.menu()
    #infos = nb.debug_search_novel('only i level up')
    #print(infos)
    #print(nb.debug_download_novel(infos[0], ending_chapter=3))

if __name__ == '__main__':
    main()
