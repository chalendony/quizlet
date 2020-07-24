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



class Verb_RoteMemory:

    def __init__(self):
        self.target = const.VERB
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_dwds = self.conn.cursor()
        self.counter = 0



    def create(self, target_date):
        query = f"select ROW_NUMBER() OVER(ORDER BY term Asc) AS Row, term , value from german where update = '{target_date}' and  sense = '{self.target}' and ktype = 'reverso_en';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            rownr = row[0]  # value
            term = row[1]  # term
            value = row[2]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                #print(entry)
                #leo_conjugations = leo.leo_verb_conjugations(term, target_date)
                tmp = []
                for i in entry:
                    tmp.append(i)
                entry = tmp[0:8]
                entry = ",  ".join(entry)
                #entry = f"{term}@@@{leo_conjugations}{const.aline}{const.nl}{entry}§§§"
                entry = f"{term}@@@{entry}§§§{const.nl}"
                batch.append(entry)
                print(entry)
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
        return const.cards_path + self.target + "_" + st + ".txt"






if __name__ == "__main__":
    v = Verb_RoteMemory()
    v.create("2020-06-19 02:09:30")
