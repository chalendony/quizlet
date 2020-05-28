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
import datetime
import time


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
        df = pd.read_sql(query, self.engine)
        pd.set_option('display.max_rows', 20)
        pd.set_option('display.max_columns', 20)
        pd.set_option('display.width', 1000)

        group = df.groupby('term')
        terms = [key for key, _ in group]
        print(terms)
        batch = []
        for term in terms:
            d = group.get_group(term)
            if 'verb' in set(d.ktype):
                print(f"Found Verb :" )

                # check verb
                if ('|' in str(d.loc[d['ktype'] == 'verb'].sense)):
                    print("Found Conjugation")
                    sen = clean_unicode(d.loc[d['ktype'] == 'verb'].sense.to_string(index=False))

                    finalstr = self.construct_string(d)
                    entry = f"{term} @@@ {finalstr} §§§"
                    batch.append(entry)
                    if len(batch) == const.MAX_CARDS:
                        self.write_to_file(batch, self.create_batch_name())
                        batch = []

        self.write_to_file(batch, self.create_batch_name())


    def write_to_file(self, lst, filename):
        print(f"writing to file {filename}")
        f = open(filename, 'w')
        with f:
            for i in lst:
                f.write(f"{i}")

    def create_batch_name(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return const.cards_path + self.target + "_" + st + ".txt"


    def format_sense(self, lst):
        tmp = []
        for i in lst:
            clean = clean_unicode(i['en'])
            tmp.append(clean.strip())
        str = '['+ '; '.join(tmp) + ']'
        return str


    def shutdown(self):
        #self.engine.
        #pg.conn.close()
        pass

    def construct_string(self,  d):
        # order: sense, translation, reverso, examples, phrase
        #########################################
        ## Leo Translations
        #########################################
        bval = ""
        val = d.loc[d['ktype'] == 'verb'].value.values
        if len(val) > 0:
            jobj = json.loads(val[0])
            bval = json.dumps(jobj, ensure_ascii=False)


        # for i in val:
        #
        #     s = json.loads(i)
        #     for j in s:
        #         en = clean_unicode(j['en'])
        #         de = clean_unicode(j['de'])
        #         bval = bval + de + "  "

        #########################################
        ## Reverso Translations
        #########################################
        rev = d.loc[d['ktype'] == 'reverso'].value
        brev = ""
        for i in rev:
            brev = brev + i + "  "

        #########################################
        ## Leo Examples
        #########################################
        bexa = ""
        exa = d.loc[d['ktype'] == 'example'].value.values
        if len(exa) > 0:
            jobj = json.loads(exa[0])
            bexa = json.dumps(jobj, ensure_ascii=False)


        # for i in exa:
        #     bexa = bexa + i + "  "

        #########################################
        ## Leo Phrases
        #########################################
        bphr = ""
        phr = d.loc[d['ktype'] == 'phrase'].value.values
        if len(phr) > 0:
            jobj = json.loads(phr[0])
            bphr = json.dumps(jobj,  ensure_ascii=False)

        # for i in jobj:
        #     clener = clean_unicode(json.loads(i)['en'])
        #     print(clener)
        #
        #
        #
        # bphr = ""
        #
        # for i in phr: # leo
        #     en = clean_unicode(i['en'])
        #     de = clean_unicode(j['de'])
        #     bphr = bphr  + en + "  " + de + " "

        #print(f"sense***** {sen}")
        print(f"value***** {bval}")
        print(f"reverso***** {brev}")
        print(f"example***** {bexa}")
        print(f"phrase***** {bphr}")

        # concate
        #finalstr = sen + '\n' + bval + '\n\n' + brev + '\n\n' + bexa + '\n\n' + bphr
        finalstr = bval + '\n\n' + brev + '\n\n' + bexa + '\n\n' + bphr
        return finalstr


if __name__ == "__main__":

    pg = Verb_Cards()
    pg.create()
    #pg.shutdown()
