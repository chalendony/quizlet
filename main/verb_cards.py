"""
reads text from database to create cards Der, Die, Das cards
"""

import reverso.constants as const
from reverso.database_handler import connect
import psycopg2
from leo.leo import clean_unicode
import json

target = const.SUBS


class Verb_Cards:
    def __init__(self):

        db = connect(const.postgres_config)
        print(db)
        self.conn = psycopg2.connect(
            host=db["host"],
            database=db["database"],
            user=db["user"],
            password=db["password"],
        )
        self.cur = self.conn.cursor()

    def create(self):
        query = """
            select  lemma, value from german 
            where ktype = %s 
            ;
            """

        self.cur.execute(query, (const.SUBS,))
        records = self.cur.fetchall()
        for row in records:
            lemma = row[0]
            value = row[1]
            # clean and format
            # value = value[0]
            value = clean_unicode(value)
            value = json.loads(value)
            value = value[0]["de"]

            entry = f"{lemma} @@@ {value} §§§{const.nl}"
            print(entry)

    def shutdown(self):
        pg.cur.close()
        pg.conn.close()


if __name__ == "__main__":

    pg = Noun_Cards()
    pg.create()
    pg.shutdown()
