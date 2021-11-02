import pypandoc
import pdfminer
# from pdfminer.high_level import extract_text_to_fp, extract_text


class FileChanger:
    def __init__(self, file_name):
        self.file = file_name
        # self.file = r'/{}'.format(file_name)

    def text(self):
        opf = "somefile.txt"
        end = self.file.split(".")[-1]
        if end != "pdf":
            assert pypandoc.convert_file(
                self.file, "plain", outputfile=opf) == ""
        else:
            with open(self.file, 'rb') as inf:
                with open(opf, 'w') as outf:
                    outf.writelines(pdfminer.high_level.extract_text(inf))
        return opf
