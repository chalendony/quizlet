import leo.leo as leo
import constants as const
from reverso.download_reverso_context_page import ReversoDictionary
import dwds.dwds as dwds

import json
from translations.database_handler import connect

import psycopg2
from psycopg2.extras import execute_values
import  time
from pons import pons
from reverso import reverso_context_simple
from random import randint
from time import sleep
import re
from reverso.reverso_context_simple import examples

pattern = "<em>.*<\/em>"
p = re.compile(pattern)



class Page:
    def __init__(self):

        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.reverso = ReversoDictionary()


    def insert_entry(self, lst):
        sql = """INSERT INTO german(term, sense, ktype, value, update)
                 VALUES %s
                 on conflict do nothing;"""
        try:
            execute_values(self.cur, sql, lst)
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"postgress error {error}")


    def get_terms_and_senses(self, target_date):
        query = f"select distinct term , value, sense from german where update = '{target_date}' and   ktype = 'reverso_senses';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]  # term
            value = row[1]  # value
            pos = row[2]  # value
            entry = json.loads(value)
            if len(entry) > 0:
                tmp = {}
                tmp["term"] = term
                tmp["senses"] = entry
                tmp["pos"] = pos
                batch.append(tmp)
        return batch


    def get_sentences(self, current_timestamp, limit):
        print(f" The current timestamp {current_timestamp}")

        lines = self.get_terms_and_senses(current_timestamp)
        for term in lines:
            german = term['term']
            senses = term['senses'][0:limit]
            pos = term['pos']

            lst = []
            dbentry = []

            for sense in senses:
                ## Carefull  - call to API!!
                tup =  list(examples(german, sense)) #  tuple

                baustein = []
                sense_baustein = {}
                for j in tup: # many sentences are here, stuff them all in database ..
                    s = re.sub(r'<em>.*<\/em>', ' [~] ', j[0]) ## german sentence
                    print(f"baustein: {sense} : {s} : {german} ")
                    baustein.append(s)

                sense_baustein['sense'] = sense
                sense_baustein['baustein'] = baustein

                dbentry.append(sense_baustein)

            print(dbentry)

            # store result
            tup = (german, pos, "reverso_context", json.dumps(dbentry, ensure_ascii=False), current_timestamp)
            dummy = []
            dummy.append(tup)
            self.insert_entry(dummy)

            #sleep
            time = randint(const.min_secs, const.max_secs)
            print(time)
            sleep(time)



if __name__ == "__main__":
    pg = Page()
    pg.get_sentences("2020-08-02 02:00:04", 2)


