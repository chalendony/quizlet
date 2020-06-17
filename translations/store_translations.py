import leo.leo as leo
import constants as const
from reverso.download_reverso_page import ReversoDictionary
import dwds.dwds as dwds

import json
from translations.database_handler import connect

import psycopg2
from psycopg2.extras import execute_values
import  time
current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


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

    def parse_all_terms(self, dir):

        lines = []
        with open(dir) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
        lines = self.reverso.remove_dash(lines)

        lst = []
        for term in lines:
            wordart = dwds.get_pos(term)
            print(f" term: {term} : wordart:  {wordart}")
            #### DWDS
            dwds_res = dwds.search(term)
            lst.append((term, wordart, "dwds", json.dumps(dwds_res, ensure_ascii=False), current_timestamp))


            #### LEO
            leo_res = leo.search(term)
            tup = (term, wordart, "leo", json.dumps(leo_res, ensure_ascii=False), current_timestamp)
            lst.append(tup)
            time.sleep(5)
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
    pg.parse_all_terms(const.terms_file)
    #pg.shutdown()