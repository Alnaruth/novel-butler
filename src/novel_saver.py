import pypandoc


class NovelSaver:
    def save_epub(self, text, path, title):
        epub_path = path + title + '.epub'
        txt_path = self._save_txt(text, path, title)
        extra_args = []
        extra_args.append(f'--metadata=title:"{title}"')
        extra_args.append(f'--metadata=author:"Novel Butler"')

        output = pypandoc.convert_text(text, 'epub', format='md', outputfile=epub_path, extra_args=extra_args)


    def _save_txt(self, text, path, title):
        txt_path = path + title + '.txt'
        with open(txt_path, 'w', encoding="utf-8") as file:
            file.write(text)
        return txt_path