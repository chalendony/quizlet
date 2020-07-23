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

class Page:
    def __init__(self):
        self.COUNTER_VERB = 0
        self.COUNTER_NOUN = 0

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

        ##--------------------------------
        # Initialize Batch Verbs - put in structure pawh...
        ##--------------------------------
        batch_verbs = []
        batch_name_verbs = "leo_verbs"
        INIT_BATCHNR_VERBS = 17 ## automate this value - goodness just put a timestamp on it
        batchnr_verbs = INIT_BATCHNR_VERBS
        ##--------------------------------
        # Initialize Batch Nouns
        ##--------------------------------
        batch_nouns = []
        batch_name_nouns = "leo_nouns"
        INIT_BATCHNR_NOUNS = 1
        batchnr_nouns = INIT_BATCHNR_NOUNS
        ##--------------------------------

        for i in files_lst[0]:
            print(f"file {i}")
            # parse reverso file...
            ## logic: if reverso sees it as a verb, then use leo verb stuff, if reverso sees it as a noun then get leo noun stuff
            lemma, usage , is_verb = self.parse_from_file(i)
            #print(f"lemma {lemma}")
            if lemma is None:
                continue
            leo_res = leo.search(lemma)
            ###  BLAHHH dump into single structre with pos as key name
            if is_verb: # reverso lists it as a verb
                self.COUNTER_VERB = self.COUNTER_VERB + 1
                print(f"{i}")
                usage = usage[0:]
                leo_en = leo.get_english_definitions(leo_res,const.VERB)
                leo_de = leo.de_get_german_translation(leo_res,const.VERB)
                entry = f"{lemma} @@@ {leo_en} {nl} {leo_de} {nl2} {nl2.join(usage)}  §§§{nl}"
                batch_verbs.append(entry)
            if lemma[0].isupper(): # reverso lists it as a substantiv
                self.COUNTER_NOUN = self.COUNTER_NOUN + 1
                usage = usage[0:]
                usage = nl2.join(usage)
                usage = usage.replace(lemma+'\n', "") # remove repeated term
                #print(f"usage {usage}")
                leo_en = leo.get_english_definitions(leo_res, const.SUBS)
                leo_de = leo.de_get_german_translation(leo_res, const.SUBS)
                entry = f"{lemma} @@@ {leo_de} {nl} {leo_en} {nl2} {usage}  §§§{nl}"
                batch_nouns.append(entry)
            time.sleep(5)
            # write batches
            if len(batch_verbs) == MAX_CARDS:
                self.write_to_file(batch_verbs, batchnr_verbs, batch_name_verbs)
                batch_verbs = []
                batchnr_verbs = batchnr_verbs + 1
            if len(batch_nouns) == MAX_CARDS:
                self.write_to_file(batch_nouns, batchnr_nouns, batch_name_nouns)
                batch_nouns = []
                batchnr_nouns = batchnr_nouns + 1
        self.write_to_file(batch_verbs, batchnr_verbs, batch_name_verbs)
        self.write_to_file(batch_nouns, batchnr_nouns, batch_name_nouns)

    def parse_from_file(self, filename):
        is_verb = False
        res = self.load(filename)
        term = self.parse_term(res)
        definition, is_verb = self.parse_definition(res)
        return term, definition, is_verb


    def parse_term(self,res):
        selector = '#ctl00_cC_translate_box > font > div > div > b:nth-child(1) > span'
        res = res.find(selector)
        if len(res) == 0:
            val = None
        else:
            val = res[0].text
        return val

    def parse_definition(self, res):
        lst = []
        is_verb = False
        selector = '#ctl00_cC_translate_box > font > div > div'
        res = res.find(selector)
        if len(res) > 0:
            # peek if verb
            is_verb = self.is_verb(res)
            for i in res:
                val = i.text
                lst.append(val)
        return lst, is_verb


    # def parse_definition_OLD(self, res):
    #     lst = []
    #     is_verb = False
    #     selector = '#ctl00_cC_translate_box > font > div > div'
    #     res = res.find(selector)
    #     if len(res) > 0:
    #         # peek if verb
    #         is_verb = self.is_verb(res)
    #         ####
    #         ### BLAM I do not even parse the nouns - HACK, HACK
    #         ###
    #         if is_verb:
    #             self.COUNTER = self.COUNTER + 1
    #             for i in res:
    #                     val = i.text
    #                     lst.append(val)
    #     return lst, is_verb


    def is_verb(self,res):
        str = ""
        for i in res:
            str += i.text
        return "ptp" in str or " vt" in str or " vi" in str or " vtr" in str


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
    pg = Page()
    pg.parse_all_files('/home/avare/repos/quizlet/data/html_files/*.html')

    #term, definition, is_verb = pg.parse_from_file('/home/avare/repos/quizlet_input/data/html_files_05_12_2020/DONE_/Scheiterhaufen.html')

    #print(f"term, definition, is_verb {definition}")
    print(f"All Done **************** verb count is:  {pg.COUNTER_VERB}")
    print(f"All Done **************** noun count is:  {pg.COUNTER_NOUN}")

