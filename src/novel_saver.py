import pypandoc
import aspose.words as aw


class NovelSaver:
    def save_pdf(self, text, path):
        text = text

        #print(text)

        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        builder.write(text)
        doc.save(path)
        '''pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=15)
        with open('tmp.txt', 'rb') as fh:
            txt = fh.read()
            pdf.multi_cell(0, 5, txt)
        pdf.output(path)
        '''
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