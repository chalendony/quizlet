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
from translations.store_duden_examples import get_entry, get_word_url


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

    def parse_all_terms(self, dir, current_timestamp):
        print(f" The current timestamp {current_timestamp}")

        lines = []
        with open(dir) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
        lines = self.reverso.remove_dash(lines)

        lst = []
        for term in lines:
            print(f"term:{term}")


            # DUDEN:
            word_url = get_word_url(term)
            print(f"word url:  {word_url}")

            if len(word_url) > 0:
                duden_entry = get_entry(word_url[0])
                print(f"duden_entry :  {duden_entry}")
                part_of_speech = duden_entry['part_of_speech']
                lst.append((term, part_of_speech, "duden", json.dumps(duden_entry, ensure_ascii=False), current_timestamp))

                # LEO
                leo_res = leo.search(duden_entry['name'])
                tup = (term, part_of_speech, "leo", json.dumps(leo_res, ensure_ascii=False), current_timestamp)
                lst.append(tup)

                self.insert_entry(lst)

                time = randint(const.min_secs, const.max_secs)
                sleep(time)
            else:
                print(f"Not found ************* {term}")

    def parse_definition(self, res):
        lst = []
        selector = "#ctl00_cC_translate_box > font > div > div"
        res = res.find(selector)
        if len(res) > 0:
            row = []
            for i in res:
                val = i.text
                split = val.split('\n')
                row.append(split)
            lst.append(row)
        return lst

    def shutdown(self):
        pg.cur.close()
        pg.conn.close()


if __name__ == "__main__":
    current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    pg = Page()
    pg.parse_all_terms(const.terms_file, '2020-11-14 23:00:00')
