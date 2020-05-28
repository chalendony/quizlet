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
        df = pd.read_sql(query, self.engine)
        pd.set_option('display.max_rows', 20)
        pd.set_option('display.max_columns', 20)
        pd.set_option('display.width', 1000)
        # pivot
        group = df.groupby('term')
        terms = [key for key, _ in group]
        print(terms)

        g = group.get_group('abarbeiten')


        blas = group.get_group('abarbeiten').ktype
        blas.values
        print (type(blas))
        if 'verb' in set(blas):
            print(f"Hallo world :" )

            d = group.get_group('abarbeiten')

            #print(d.loc[d['ktype'] == 'verb'])

            # check verb
            if ('|' in str(d.loc[d['ktype'] == 'verb'].sense)):
                print("found it")
                # order: sense, translation, prep, reverso, examples, phrase
                sen = clean_unicode(d.loc[d['ktype'] == 'verb'].sense.to_string(index=False))
                val = d.loc[d['ktype'] == 'verb'].value

                #### TODO: Pack this code into a function
                bval = ""
                for i in val: # hack:  gets the first and only  element of the series????
                    s = json.loads(i)
                    for j in s:
                        en = clean_unicode(j['en'])
                        de = clean_unicode(j['de'])
                        bval = bval + de + "  "

                rev = d.loc[d['ktype'] == 'reverso'].value
                brev = ""
                for i in rev:
                    brev = brev + i + "  "

                exa = d.loc[d['ktype'] == 'example'].value.values
                bexa = ""
                for i in exa:
                    bexa = bexa + + i + "  "

                phr = d.loc[d['ktype'] == 'phrase'].value.values
                bphr = ""
                for i in phr:
                    bphr = bphr + + i + "  "
                phr = d.loc[d['ktype'] == 'phrase'].value.values
                print(f"sense***** {sen}")
                print(f"value***** {bval}")
                print(f"reverso***** {brev}")
                print(f"example***** {bexa}")
                print(f"phrase***** {bphr}")

            # concate



        # print

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

if __name__ == "__main__":

    pg = Verb_Cards()
    pg.create()
    #pg.shutdown()
