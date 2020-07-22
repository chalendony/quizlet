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
import re


class Crossword:

    def __init__(self):
        self.target = const.CROSSWORD
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()

    def create(self, target_date):


                    #'select  term, value from public.german where sense = 'Verb' and ktype ='dwds';'
        dw_query = f"select term , value from public.german where ktype = 'dwds' and sense = 'Verb';"
        self.cur.execute(dw_query)
        dw_records = self.cur.fetchall()
        batch = []

        for dw_row in dw_records:
            term = dw_row[0]  # term
            value = dw_row[1]  # value
            print(f"term {term}")
            dw_lst = json.loads(value)
            definition = self.crossword(term, dw_lst)
            if definition is not None:
                entry = f"{term}\t{definition}{const.nl}"
                batch.append(entry)
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

    def remove_id(self, definition, id):
        str = definition.replace(id,'')
        return str

    def remove_term(self, term, definition):
        str = definition.replace(term,'')
        return str

    def remove_brace(self, definition):
        #pattern, repl, string,
        str = re.sub(r"⟨.*⟩", '', definition)
        return str

    def clean(self, term, definition, id):

        s = self.remove_id(definition, id).strip()
        if '⟨' in s:
            s = self.remove_brace(s).strip()
        return s

    def crossword(self, term, dict):
        id = 'd-1-1'
        definition = None
        if "inline_examples" in dict.keys():
            lst = dict["inline_examples"]
            for i in lst:
                definition = i["definition"]
                if (id in definition):
                    definition = self.clean(term, definition.strip(), id)
                    return definition


if __name__ == "__main__":

    pg = Crossword()
    #pg.create('2020-06-18 19:54:47')
    pg.create('2020-06-19 02:09:30')

#
