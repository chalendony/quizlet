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


class Verb_RoteMemory:

    def __init__(self):
        self.target = const.VERB
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_dwds = self.conn.cursor()

    def create(self, target_date):

        query = f"select term , value from german where update = '{target_date}' and  sense = '{self.target}' and ktype = 'pons';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]  # term
            value = row[1]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                leo_conjugations = leo.leo_verb_conjugations(term, target_date)
                ponsentry = pons.rote_memory_verb(entry[0], self.target)
                #dwdsexample = dwds.examples(term , self.target, target_date, limit=2)
                dwdsexample = ""
                entry = f"{term} @@@{leo_conjugations}{const.aline}{const.nl}{ponsentry}{const.aline}{dwdsexample}§§§"
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






if __name__ == "__main__":
    v = Verb_RoteMemory()
    v.create("2020-06-19 02:09:30")
