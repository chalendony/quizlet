import codecs
from requests_html import HTML
from collections import namedtuple
import csv
import glob
import leo.leo as leo
import time
import constants as const

import constants as const

# database connection
from translations.database_handler import connect
import psycopg2
from psycopg2.extras import execute_values
import json





class Context:

    def __init__(self):

        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()

    def get_pos(self, term):
        query = f"select distinct sense from german where term = '{term}';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        for row in records:
            val = row[0]  # value
        return val

    def insert_entry(self, lst):
        sql = """INSERT INTO german(term, sense, ktype, value, update)
                 VALUES %s
                 on conflict do nothing;"""
        try:
            execute_values(self.cur, sql, lst)
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"postgress error {error}")

    def load(self, filename):
        f = codecs.open(filename, "r", "ISO-8859-15")
        str = f.read()
        f.close()
        html = HTML(html=str.encode('ISO-8859-15'), default_encoding="ISO-8859-15")
        return html


    def parse_all_files(self, dir,dat):
        lst = []
        files_lst = glob.glob(dir)
        for i in files_lst:
            #print(f"file {i}")
            de = self.parse_german(i)
            print(de)
            pos = self.get_pos(de)
            en = self.parse_from_file(i)
            print(en)
            tup = (de, pos, "reverso_en", json.dumps(en, ensure_ascii=False), dat)
            lst.append(tup)
            #print(lst)
        #self.insert_entry(lst)

    def parse_german(self,i):
        splits = i.split("/")
        v = splits[-1].replace(".html", "")
        return v

    def parse_from_file(self, filename):
        is_verb = False
        res = self.load(filename)
        term = self.parse_term(res)
        return term

    def parse_term(self, res):
        lst = []
        selector = "#translations-content > a"
        res = res.find(selector)
        if len(res) == 0:
            val = None
        else:
            for i in res:
                txt = i.text
                lst.append(txt)
        return lst



    def write_to_file(self, lst, batchnr, filename):
        f = open(const.cards_path + filename + "_" + str(batchnr) + ".txt", 'w')
        with f:
            for i in lst:
                f.write(f"{i}")



if __name__ == "__main__":
    pg = Context()
    pg.parse_all_files('/home/avare/repos/quizlet/data/html_files/*.html', '2020-06-19 02:09:30')


