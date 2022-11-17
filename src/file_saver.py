import os


def save_novel(title, chapters):
    library_path = '../books/'
    book_dir_path = library_path + title.replace(' ', '-')
    book_path = book_dir_path + '/' + title + '.txt'
    if not os.path.exists(book_dir_path):
        os.mkdir(book_dir_path)

    if os.path.exists(book_path):
        choice = ''
        positive_choices = ['y', 'Y', 'yes', 'Yes', 'ye', 'Ye']
        negative_choices = ['n', 'N', 'no', 'No']
        while choice not in positive_choices and choice not in negative_choices:
            choice = input('book already downloaded, overwrite? [y/n] -> ')

        if choice in negative_choices:
            print('Aborting process.')
            return False

    print(f'\n\nSaving book at {book_path}...')
    with open(book_path, 'w', encoding="utf-8") as fd:
        count = 0
        for chapter in chapters:
            count += 1
            buffer = f'CHAPTER {count}: \n\n\n {chapter} \r\n\n'
            fd.write(buffer)
    print('Done.')