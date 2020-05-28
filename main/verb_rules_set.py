"""
reads text from database to create cards Der, Die, Das cards
"""

import reverso.constants as const
from reverso.database_handler import connect
import psycopg2
from leo.leo import clean_unicode
import json
import pandas as pd
from reverso.database_handler import connect_alchemy

target = const.VERB


class Verb_Cards:
    def __init__(self):
        self.target = const.VERB
        self.engine = connect_alchemy(const.postgres_config)

    def create(self):
        query = """
            select  * from german 
            ;
            """
        # ====== Reading table ======
        # Reading PostgreSQL table into a pandas DataFrame
        df = pd.read_sql(query, self.engine)
        print(df.head)



    def shutdown(self):
        #pg.cur.close()
        #pg.conn.close()
        pass

if __name__ == "__main__":

    pg = Verb_Cards()
    pg.create()
    pg.shutdown()
