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

aline = "\n----------------\n"
target = const.VERB



class Verb_Cards:
    def __init__(self):
        self.target = const.VERB
        self.engine = connect_alchemy(const.postgres_config)

    def create(self, target_date):

        query = f"select  * from german where update = '{target_date}';"
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
                    #sen = clean_unicode(d.loc[d['ktype'] == 'verb'].sense.to_string(index=False))
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

    def prune_translations(self, jobj):
        definition = {}
        en_translations = []
        de_conjugation = jobj[0]['de']
        # TODO: restrict translations
        upper = min(len(jobj), const.max_card_entries)
        for i in jobj[0:upper]:
            ent = i['en']
            print(f"english {ent}")
            split = ent.split('|')[0]
            en_translations.append(split.strip())
        definition[de_conjugation] = en_translations
        return definition


    def construct_string(self,  d):
        # order: translation, reverso, examples, phrase
        #########################################
        ## Leo Translations : TODO get more LEO translations
        #########################################
        bval = ""
        val = d.loc[d['ktype'] == 'verb'].value.values
        if len(val) > 0:
            jobj = json.loads(val[0])
            jobj = self.prune_translations(jobj)
            bval = json.dumps(jobj, ensure_ascii=False)

        #########################################
        ## Reverso Translations :  TODO: only use if there is no LEO
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

        #########################################
        ## Leo Phrases
        #########################################
        bphr = ""
        phr = d.loc[d['ktype'] == 'phrase'].value.values
        if len(phr) > 0:
            jobj = json.loads(phr[0])
            bphr = json.dumps(jobj,  ensure_ascii=False)

        print(f"value***** {bval}")
        print(f"reverso***** {brev}")
        print(f"example***** {bexa}")
        print(f"phrase***** {bphr}")

        # concate
        finalstr = bval + aline + brev + aline + bexa + aline + bphr
        return finalstr



if __name__ == "__main__":

    pg = Verb_Cards()
    pg.create('2020-06-12 16:20:18')
    #pg.shutdown()
