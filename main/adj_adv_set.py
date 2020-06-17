"""
reads text from database to create cards Der, Die, Das cards
"""

from translations.database_handler import connect
from leo.leo import clean_unicode
import json
import constants as const
import datetime
import time


from googletrans import Translator

translator = Translator()

class AdjAdv_Cards:

    def __init__(self):
        self.target = const.ADJADV
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
            en = self.format_english(leo_res)

            ## get examples
            examples = self.get_examples(term, target_date)
            entry = f"{term} @@@ {term} {const.nl} {const.nl} {en} {const.nl} {const.aline}  {const.nl} {examples} §§§{const.nl}"

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

    def get_examples(self, term, target_date):
        """
        Note there is a difference if you pull the data into a dataframe or if you pull directly... pulling into dataframe is more overhead when  processing json - rather use multiple queries  if possible
        # the original idea was to use group by ... was painful decision .. one day refactor this idea to directly perform database fetch
        :param term:
        :param target_date:
        :return:
        """
        query = f"select value from german where ktype = '{const.DWDS}' and term = '{term}' and update = '{target_date}';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            val = row[0]
            ## DUPLICATED from non-modular code in verb module ...
            if val is not None:
                dwds = ""
                print(f"text: {val}")
                jobj = json.loads(val)
                if len(jobj) > 0:
                    for i in jobj:
                        splits = i.split('\n')
                        # translate and format
                        for de in splits:
                            if 'Beispiele' not in de:
                                try:
                                    en = translator.translate(de, src='de', dest='en')
                                    dwds = dwds + "▢  " + de + ' ▪ ' + en.text + '\n\n'
                                except:
                                    pass
                        #print(f"dwds: {dwds}")
            ##################### DUPLICATED
        return dwds


    def shutdown(self):
        pg.cur.close()
        pg.conn.close()


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
    pg = AdjAdv_Cards()
    pg.create('2020-06-13 01:43:57')
    pg.shutdown()
