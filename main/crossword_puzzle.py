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

    # todo
    # combine
    # with nouns for crossword puzzle


    # def create(self, target_date):
    #     query = f"select  ROW_NUMBER() OVER(ORDER BY term Asc) AS Row, term , value from german where update = '{target_date}' and  sense = '{self.target}' and ktype = 'pons';"
    #     self.cur.execute(query)
    #     records = self.cur.fetchall()
    #     batch = []
    #     for row in records:
    #         rownr = row[0]  # value
    #         term = row[1]  # term
    #         value = row[2]  # value
    #         entry = json.loads(value)
    #         if len(entry) > 0:
    #             ponsentry = pons.flippity_verb(entry[0], self.target, term)
    #             if len(ponsentry) > 0:
    #                 batch.append(ponsentry)
    #
    #     random.seed(160)
    #     batch = list(itertools.chain(*batch)) # flatten the list
    #     random.shuffle(batch)
    #     #print(batch)
    #     #batch = batch[0:const.MAX_CROSSWORD]
    #     self.write_to_file(batch, self.create_batch_name())


    def xword_entry_noun(self,target_date):
        query = f"select ROW_NUMBER() OVER(ORDER BY term Asc) AS Row, term , value from german where update = '{target_date}' and  sense = '{const.SUBS}' and ktype = 'reverso_en';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            rownr = row[0]  # value
            term = row[1]  # term
            value = row[2]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                print(entry)
                art = leo.leo_article(term, target_date)
                art = art.replace(',','')
                tmp = []
                for i in entry:
                    tmp.append(i)
                entry = tmp[0:5]
                entry = f"({art}) " + " ; ".join(entry)
                entry = f"{entry},{term}{const.nl}"
                batch.append(entry)
                # print(entry)

        # #random.seed(161)
        # random.shuffle(batch)
        # batch = batch[0:const.MAX_CROSSWORD]
        # self.write_to_file(batch, self.create_batch_name() )
        return batch


    def xword_entry_verb(self,target_date):
        query = f"select ROW_NUMBER() OVER(ORDER BY term Asc) AS Row, term , value from german where update = '{target_date}' and  sense = '{const.VERB}' and ktype = 'reverso_en';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            rownr = row[0]  # value
            term = row[1]  # term
            value = row[2]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                tmp = []
                for i in entry:
                    tmp.append(i)
                entry = tmp[0:3]
                entry = " ; ".join(entry)
                # entry = f"{term}@@@{leo_conjugations}{const.aline}{const.nl}{entry}§§§"
                entry = f"{entry},{term}{const.nl}"
                batch.append(entry)
                #print(entry)
            # if (rownr % const.MAX_CARDS) == 0:
            #     self.counter = self.counter + 1
            #     self.write_to_file(batch, self.create_batch_name() + str(self.counter))
            #     batch = []

        # random.seed(161)
        # random.shuffle(batch)
        # # print(batch)
        # batch = batch[0:const.MAX_CROSSWORD]
        # self.write_to_file(batch, self.create_batch_name() )
        return batch

    def xword_entry_all(self,target_date):
        batch =[]
        noun = self.xword_entry_noun(target_date)
        vb = self.xword_entry_verb(target_date)

        batch.extend(noun)
        batch.extend(vb)
        random.seed(161)
        random.shuffle(batch)
        batch = batch[0:const.MAX_CROSSWORD]
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
    v.xword_entry_all("2020-06-19 02:09:30")
