from requests_html import HTML
import leo.leo as leo
import time
import reverso.constants as const
from reverso.download_reverso_page import ReversoDictionary
import json
from configparser import ConfigParser
from reverso.database_handler import connect

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
            print(error)

    def parse_all_terms(self, dir):

        lines = []
        with open(dir) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
        lines = self.reverso.remove_dash(lines)

        for term in lines:
            lst = []
            print(f" term:  {term}")

            ### LEO
            leo_res = leo.search(term)
            for k in leo_res.keys():
                sense = leo_res[k][0]['de']
                upper = min(len(leo_res[k]),const.max_translations) ### TODO: do not over-restrict translations when storing in DB
                tup = (term, sense, k , json.dumps(leo_res[k][0:upper], ensure_ascii=False), current_timestamp)
                lst.append(tup)

            ### REVERSO
            url = f"{const.reverso_base_url}{term}"
            soup_html = self.reverso.download(url)
            htm_str = HTML(html=soup_html, default_encoding="ISO-8859-15")
            usage = self.parse_definition(htm_str)
            lst.append((term, term, "reverso", usage, current_timestamp))

            self.insert_entry(lst)
            time.sleep(3)

    def parse_definition(self, res):
        lst = []
        selector = "#ctl00_cC_translate_box > font > div > div"
        res = res.find(selector)
        if len(res) > 0:
            for i in res:
                val = i.text
                lst.append(val)
        return lst

    def shutdown(self):
        pg.cur.close()
        pg.conn.close()


if __name__ == "__main__":

    pg = Page()
    #pg.parse_all_terms("/home/avare/repos/quizlet/data/terms_test.txt")
    pg.parse_all_terms(const.terms_file)
    pg.shutdown()