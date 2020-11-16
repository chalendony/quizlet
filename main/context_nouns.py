"""
reads text from database to create cards Der, Die, Das cards
"""
import itertools

from translations.database_handler import connect
import constants as const
import json
import datetime
import time
import quizlet.common as common
import os
from dwds import  dwds

from googletrans import Translator
translator = Translator()
import requests
import sys
from pons import pons
from leo import leo
from reverso import reverso_context_simple
from translations.store_duden_examples import parse_duden_context


class Noun_RoteMemory:

    def __init__(self):
        self.target = '%ubstantiv%'

        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_B = self.conn.cursor()
        self.counter = 0



    def create(self):
        query = f"select ROW_NUMBER() OVER(ORDER BY term Asc) AS Row, term , value from german where sense like  '{self.target}' and ktype = 'reverso_senses';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []

        ## get english translations
        for row in records:
            rownr = row[0]  # value
            term = row[1]  # term
            value = row[2]  # value
            english = json.loads(value) # english
            #print(term)
            if len(english) > 0: # there may be reverso, but no duden !!

                # get context in german : IF EXISTS
                query_B = f"select value from german where sense like '{self.target}' and ktype = 'duden' and term = '{term}';"
                self.cur_B.execute(query_B)
                recordsB = self.cur_B.fetchall()
                for r in recordsB:
                    if r is not None:
                        contents = r[0]
                        contents = json.loads(contents)
                        context = parse_duden_context(contents)

                        if context is not None:
                            # format english and limit to 5 entries
                            tmp = []
                            for i in english:
                                tmp.append(i)
                            english = tmp[0:5]
                            english = ",  ".join(english)

                            # proper formating for nouns
                            article = contents['article']
                            if article is None:
                                german = contents['name']
                            else:
                                german =  article + " " + contents['name']


                            entry = f"{german}@@@{english}{const.nl}{const.nl}{context}§§§{const.nl}"
                            batch.append(entry)
                            #print(entry)
                        else:
                            print(f"NOT FOUND ************************************* {term}")
            if (rownr % const.MAX_CARDS) == 0:
                self.counter = self.counter +1
                self.write_to_file(batch, self.create_batch_name() + str(self.counter))
                batch = []
        self.counter = self.counter + 1
        self.write_to_file(batch, self.create_batch_name() + str(self.counter))


    def write_to_file(self, lst, filename):
        print(f"writing to file {filename}")
        f = open(filename, "w")
        with f:
            for i in lst:
                f.write(f"{i}")

    def create_batch_name(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        return const.cards_path + self.target.replace('%', '') + "_" + st + ".txt"






if __name__ == "__main__":
    v = Noun_RoteMemory()
    v.create()


# schwaches Verb
# starkes und schwaches Verb
# Verb
# unregelmäßiges Verb
# starkes Verb
#
#
# Substantiv, maskulin
# Substantiv, feminin
# substantiviertes Adjektiv, feminin
# Substantiv
# Substantiv, Neutrum
#
# partizipiales Adverb
# Pronominaladverb
# Adverb
# partizipiales Adjektiv
# Adjektiv
#
# Präposition
# Indefinitpronomen
# Pronomen
# Eigenname
# Pluralwort
# Demonstrativpronomen
# Konjunktion

