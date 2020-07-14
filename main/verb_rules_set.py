"""
reads text from database to create cards Der, Die, Das cards
"""
from translations.database_handler import connect
import constants as const
import json
import datetime
import time
import quizlet.common as common
import os


from googletrans import Translator
translator = Translator()
import requests
import sys


class Verb_Cards:

    def __init__(self):
        self.target = const.VERB
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_dwds = self.conn.cursor()

    def create(self, target_date):

        query = f"select term , value from german where update = '{target_date}' and  sense = '{self.target}' and  ktype = 'dwds';"
        print(query)
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]  # term
            value = row[1]  # value
            dw_lst = json.loads(value)
            inline_examples = self.dwds_inline_examples(dw_lst)
            #korpora_examples = self.dwds_korpora_examples(dw_lst)
            entry = f"{term} @@@{en}{const.nl}{const.aline}{const.nl}{inline_examples}§§§"
            print(entry)
            batch.append(entry)
        if len(batch) == const.MAX_CARDS:
            self.write_to_file(batch, self.create_batch_name())
            batch = []

        self.write_to_file(batch, self.create_batch_name())


    def write_to_file(self, lst, filename):
        print(f"writing to file {filename}")
        f = open(filename, "w")
        with f:
            for i in lst:
                f.write(f"{i}")

    def create_batch_name(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        return const.cards_path + self.target + "_" + st + ".txt"

    def leo_translations(self, lst):
        str = ""
        definition = {}
        en_translations = []
        de_conjugation = lst[0]["de"]
        # restrict translations
        upper = min(len(lst), const.max_card_entries)
        for i in lst[0:upper]:
            ent = i["en"]
            # print(f"english {ent}")
            split = ent.split("|")[0]
            en_translations.append(split.strip())
        definition[de_conjugation] = en_translations
        # format
        str = de_conjugation + const.aline + "\n" + "  ▪  ".join(en_translations)
        str = common.remove_dangling_letter(str)
        return str






if __name__ == "__main__":

    #pg = Verb_Cards()
    #pg.create('2020-06-19 02:09:30')

    headers = {'X-Secret': 'cffcdd1c60b8c18d2b3efa758cf8d96d74895609cdacc3f5695ff508be83a1b0'}
    url = f"""https://api.pons.com/v1/dictionary?q=warten&l=deen&in=de"""
    r = requests.get(url, headers=headers)
    print(r.text)
