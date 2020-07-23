import leo.leo as leo
import constants as const
from reverso.download_reverso_page import ReversoDictionary
import dwds.dwds as dwds

import json
from translations.database_handler import connect

import psycopg2
from psycopg2.extras import execute_values
import  time
from pons import pons
from reverso import reverso_context_simple

#current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#current_timestamp = '2020-06-19 02:09:30'

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

    def parse_all_terms(self, dir, current_timestamp=None):

        lines = []
        with open(dir) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
        lines = self.reverso.remove_dash(lines)

        lst = []
        for term in lines:
            print(f"term:{term}")
            lst = []
            wordart = dwds.get_pos(term)

            # print(f" term: {term} : wordart:  {wordart}")
            # #### DWDS nicely structures parts of speech overcomes problem Leo
            # dwds_res = dwds.search(term)
            # lst.append((term, wordart, "dwds", json.dumps(dwds_res, ensure_ascii=False), current_timestamp))
            #
            #
            # #### LEO :  using conjugations : parts of speech senses and examples not ordered,
            # leo_res = leo.search(term)
            # tup = (term, wordart, "leo", json.dumps(leo_res, ensure_ascii=False), current_timestamp)
            # lst.append(tup)
            # time.sleep(5)
            # self.insert_entry(lst)

            #### PONS hard to study for rote memorization need simple single word translation with matching sense
            # pons_result = pons.search(term)
            # print(f"pons: {pons_result}")
            # tup = (term, wordart, "pons", json.dumps(pons_result, ensure_ascii=False), current_timestamp)
            # lst.append(tup)
            # time.sleep(3)
            # self.insert_entry(lst)

            ### Reverso : overcomes problems of pons : too many requests .. seriously!!
            reverso_result =  reverso_context_simple.reverso_examples(term)
            print(f"reverso: {reverso_result}")
            tup = (term, wordart, "reverso", json.dumps(reverso_result, ensure_ascii=False), current_timestamp)
            lst.append(tup)

            self.insert_entry(lst)



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

    pg = Page()
    pg.parse_all_terms(const.terms_file, "2020-06-19 02:09:30")
