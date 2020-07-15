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
from dwds import  dwds

from googletrans import Translator
translator = Translator()
import requests
import sys
from pons import pons
from leo import leo


class XWord:

    def __init__(self):
        self.target = const.VERB
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_dwds = self.conn.cursor()

    def create(self, target_date):

        query = f"select term , value from german where update = '{target_date}' and  sense = '{self.target}' and ktype = 'pons' order by random() limit {const.MAX_CARDS};"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]  # term
            value = row[1]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                ponsentry = pons.xword_verb(entry[0], self.target, const.WORD_SENSE)
                if len(ponsentry) > 0:
                    ponsentry = f"{term},{ponsentry}"
                    print(ponsentry)
                    batch.append(ponsentry)
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
        return const.cards_path +  "xword_" + st + ".txt"






if __name__ == "__main__":
    v = XWord()
    v.create("2020-06-19 02:09:30")
