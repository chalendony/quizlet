"""
reads text from database to create cards Der, Die, Das cards
"""

from translations.database_handler import connect
from leo.leo import clean_unicode
import json
import constants as const
import datetime
import time



class Noun_Cards:

    def __init__(self):
        self.target = const.SUBS
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()

    def create(self, target_date):
        query = f"select term ,sense , value from german where ktype = %s and update = '{target_date}';"

        self.cur.execute(query, (self.target,))
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]
            sense = row[1]
            value = row[2]
            leo_res = json.loads(value)
            #print(leo_res)
            en = self.format_english(leo_res)
            subst = self.getSubst(sense)
            entry = f"{subst} @@@ {sense} {const.nl} {const.nl} {en} §§§{const.nl}"

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


    def getSubst(self, lst):
        res = lst.split()[1]

        return res

    def format_english(self, lst):
        tmp = []
        for i in lst:
            clean = clean_unicode(i['en'])
            clean = clean.replace('AE',"")
            clean = clean.replace('BE', "")
            tmp.append(clean.strip())
        str = ' ▪ '.join(tmp)
        return str

if __name__ == "__main__":
    pg = Noun_Cards()
    pg.create('2020-06-13 00:50:31')
    pg.shutdown()
