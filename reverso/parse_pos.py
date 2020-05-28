from requests_html import HTML
import leo.leo as leo
import time
import reverso.constants as const
from reverso.download_reverso_page import ReversoDictionary
import json
from configparser import ConfigParser

import psycopg2
from psycopg2.extras import execute_values


class Page:
    def __init__(self):
        print(const.postgres_config)

        db = self.config(const.postgres_config)
        print(db)
        self.conn = psycopg2.connect(
            host=db['host'], database=db['database'], user=db['user'], password=db['password']
        )

        self.cur = self.conn.cursor()
        self.reverso = ReversoDictionary()

    def insert_entry(self, lst):
        sql = """INSERT INTO german(lemma, ktype, value)
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

        for lemma in lines:
            lst = []
            print(f" lemma:  {lemma}")
            leo_res = leo.search(lemma)

            url = f"{const.reverso_base_url}{lemma}"
            soup_html = self.reverso.download(url)
            htm_str = HTML(html=soup_html, default_encoding="ISO-8859-15")
            usage = self.parse_definition(htm_str)
            for k in leo_res.keys():
                tup = (lemma, k, json.dumps(leo_res[k][0:3]))
                lst.append(tup)
            lst.append((lemma, "reverso", usage))
            self.insert_entry(lst)

            # time.sleep(5)

    def config(self, filename, section="postgresql"):
        print(f"filename {filename}")
        parser = ConfigParser()
        parser.read(filename)
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                "Section {0} not found in the {1} file".format(section, filename)
            )

        return db

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
    pg.parse_all_terms("/home/avare/repos/quizlet/data/terms_test.txt")
    pg.shutdown()
