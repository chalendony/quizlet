"""
reads text from database to create cards Der, Die, Das cards
"""
import random

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
import itertools


class XWord:

    def __init__(self):
        self.target = const.VERB
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_dwds = self.conn.cursor()

    def create(self, target_date):
        query = f"select  ROW_NUMBER() OVER(ORDER BY term Asc) AS Row, term , value from german where update = '{target_date}' and  sense = '{self.target}' and ktype = 'pons';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            rownr = row[0]  # value
            term = row[1]  # term
            value = row[2]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                ponsentry = pons.flippity_verb(entry[0], self.target, term)
                if len(ponsentry) > 0:
                    batch.append(ponsentry)

        random.seed(160)
        batch = list(itertools.chain(*batch)) # flatten the list
        random.shuffle(batch)
        #print(batch)
        #batch = batch[0:const.MAX_CROSSWORD]
        self.write_to_file(batch, self.create_batch_name())


    def write_to_file(self, lst, filename):
        print(f"writing to file {filename}")
        f = open(filename, "w",  encoding="UTF8")
        with f:
            for i in lst:
                f.write(f"{i}")

    def create_batch_name(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        return const.cards_path +  "crossword_" + st + ".csv"



if __name__ == "__main__":
    v = XWord()
    v.create("2020-06-19 02:09:30")
