import codecs
from requests_html import HTML
from collections import namedtuple
import csv
import glob
import leo.leo as leo
import time
import constants as const

csv.register_dialect("atters", delimiter="@")
base_url = 'https://www.linguee.com/german-english/translation/'
extension = '.html_files'

cards_path = '/home/avare/repos/quizlet/data/quizlet_input/'
TERM_LIMIT = 2
ENGLISH = 'english'
GERMAN = 'german'
MAX_CARDS = 500


pos_verb = ['vi, vt']
VERB = True

Entry = namedtuple(
    "Entry",
    [
        "term",
        "definition",
        "en",
        "de",
    ],
)

nl = "\n"
nl2 = "\n\n"
comma = ", "

class Context:


    def load(self, filename):
        f = codecs.open(filename, "r", "ISO-8859-15")
        str = f.read()
        f.close()
        html = HTML(html=str.encode('ISO-8859-15'), default_encoding="ISO-8859-15")
        return html

    def is_empty(self, page):
        target = 'No results for'
        idx = page.text.find(target)
        print(f"Check empty {idx}")
        flag = idx != -1
        return flag

    def parse_all_files(self, dir):
        lst = []
        files_lst = glob.glob(dir)
        for i in files_lst:
            print(f"file {i}")
            term = self.parse_from_file(i)
            print(term)

    def parse_from_file(self, filename):
        is_verb = False
        res = self.load(filename)
        term = self.parse_term(res)
        return term


    def parse_term(self,res):
        lst = []
        selector =  "#translations-content"
        res = res.find(selector)
        if len(res) == 0:
            val = None
        else:
            txt = res[0]
            splits = txt.text.split("\n")
            for i in splits:
                lst.append(i)

        return lst


    def write_to_file(self, lst, batchnr, filename):
        f = open(cards_path + filename + "_" + str(batchnr) + ".txt", 'w')
        with f:
            for i in lst:
                f.write(f"{i}")

    def clean_defintion(self,lst):
        res = []
        # drop first element
        # replace newline with colon
        # limit the number of defintions to 5
        upper_val = min(5, len(lst))
        for i in range(1,upper_val):
            str = lst[i]
            str = str.replace('\n', '  \n  ')
            res.append(str)
        return res


if __name__ == "__main__":
    pg = Context()
    pg.parse_all_files('/home/avare/repos/quizlet/data/html_files/*.html')


