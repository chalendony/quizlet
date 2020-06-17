from requests_html import HTMLSession
import codecs
from requests_html import HTML
from collections import namedtuple
import csv

csv.register_dialect("atters", delimiter="@")
base_url = 'https://www.linguee.com/german-english/translation/'
extension = '.html'
session = HTMLSession()
dump = '/home/avare/repos/linguee/data/DUMP.txt'
cards = '/home/avare/repos/linguee/data/cards.txt'
TERM_LIMIT = 2
ENGLISH = 'english'
GERMAN = 'german'

Entry = namedtuple(
    "Entry",
    [
        "term",
        "definition",
    ],
)


class Page:

    def get(self, term):
        url = base_url + term + extension
        print(url)
        page = session.get(url)
        return page

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

    def parse_from_url(self, term):
        result = self.get(term)
        sent = self.sentence(result.html)
        terms = self.single_lines(result.html)
        sent.extend(terms)
        self.formatter(sent)


    def parse_from_file(self, filename):
        ## TODO move check from this code!!
        result = self.load(filename)
        # skip if file empty
        if (self.is_empty(result)):
            return
        lemmalines = self.lemma_line(result)
        translationblock = self.translationblock(result)
        res = self.featured_translations(translationblock)
        print(f"featured translations: {len(res)}")
        counter = 0
        for i in range(0,len(res)):
            featured = res[i]
            if self.has_sentence(featured): # maybe  example usage does not exist
                sense = self.translation(featured)
                usage = self.sentence(featured)
                print(f"Sense: {sense}")
                print(f"Usage: {usage}")
                self.formatter(lemmalines, sense, usage)
                counter = counter + 1
                if counter == TERM_LIMIT:
                    break


    def featured_translations(self, result):
        # dictionary > div.isForeignTerm > div.exact > div:nth-child(1) > div > div > div > div > div:nth-child(1)
        selector = 'div.translation.sortablemg.featured'
        res = result.find(selector)
        return res




    def lemma_line(self,result):
        print(result)
        selector = '#dictionary > div.isForeignTerm > div.exact > div:nth-child(1) > div > h2 > span.tag_lemma'
        res = result.find(selector)
        text = res[0].text
        print(f"Lemma lines: {text}")
        return text


    def single_lines(self, result):
        selector = 'div.example_lines'
        res = result.find(selector)
        pairs = []
        lines = len(res)
        #print(f'Lines {lines}')
        for i in range(0, lines):
            split = res[i].text.split('\n')
            #print(f'Number Newlines {len(split)}')
            if len(split) == 2:
                #print(f'Found Pair {str}')
                de = split[0]
                en = split[1]
                definition = self.drop_case(de)
                term = self.drop_case(en)
                e = {
                    ENGLISH: term,
                    GERMAN: definition,
                }
                pairs.append(e)
            else:
                # dump to file and clean manually
                with open(dump, "a") as file_object:
                    file_object.write('\n'.join(split))
        return pairs

    def translation(self, result):
        selector = 'h3.translation_desc'
        res = result.find(selector)
        return res[0].text

    def translationblock(self, result):
        selector = '#dictionary > div.isForeignTerm > div.exact > div:nth-child(1) > div > div > div > div'
        res = result.find(selector)
        return res[0]

    def has_sentence(self, result):
        selector = 'div.example_lines'
        res = result.find(selector)
        return len(res)

    def sentence(self, result):
        selector = '.tag_e'

        res = result.find(selector)
        lines = len(res)
        pairs = []
        for i in range(0, lines):
            str = res[i].text
            split = res[i].text.split('—')
            if len(split) == 2:
                definition = split[0]
                term = split[1]
                e = {
                    ENGLISH: term,
                    GERMAN: definition,
                }
                pairs.append(e)
        return pairs

    def drop_case(self,str):
        split = str.split()
        return ' '.join(split[0:2])

    def formatter(self, lemma, translation, sentence):
        # list of dict
        print(sentence)
        f = open(cards, 'a')
        with f:
            for e in sentence:
                f.write(f"\n{lemma}: {e.get(ENGLISH)}" '@@@' f" {translation} : {e.get(GERMAN)} §§§")



if __name__ == '__main__':
    page = Page()
    p = page.parse_from_file('/home/avare/repos/quizlet/data/wget/ableiten.html')
