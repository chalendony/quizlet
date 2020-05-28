"""
reads text from database to create cards Der, Die, Das cards
"""

import reverso.constants as const
from reverso.database_handler import connect
import psycopg2
from leo.leo import clean_unicode
import json
import reverso.constants as const
import datetime
import time


class Noun_Cards:

    def __init__(self):
        self.target = const.SUBS
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()

    def create(self):
        query = """
            select term ,sense from german 
            where ktype = %s 
            ;
            """
        self.cur.execute(query, (self.target,))
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]
            sense = row[1]
            entry = f"{term} @@@ {sense} §§§{const.nl}"
            #print(entry)
            batch.append(entry)
            if len(batch) == const.MAX_CARDS:
                self.write_to_file(batch, self.create_batch_name())
                batch = []
        self.write_to_file(batch, self.create_batch_name())

    def create_batch_name(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return const.cards_path + self.target + "_" + st + ".txt"

    def write_to_file(self, lst, filename):
        print(f"writing to file {filename}")
        f = open(filename, 'w')
        with f:
            for i in lst:
                f.write(f"{i}")


    def shutdown(self):
        pg.cur.close()
        pg.conn.close()


if __name__ == "__main__":
    pg = Noun_Cards()
    pg.create()
    pg.shutdown()
