"""
reads text from database to create cards Der, Die, Das cards
"""
from translations.database_handler import connect
import constants as const
import json
import datetime
import time
import quizlet.common as common

from googletrans import Translator
translator = Translator()

class Verb_Cards:

    def __init__(self):
        self.target = const.VERB
        self.conn = connect(const.postgres_config)
        self.cur = self.conn.cursor()
        self.cur_dwds = self.conn.cursor()

    def create(self, target_date):

        query = f"select term , value from german where update = '{target_date}' and  sense = '{self.target}' and  ktype = 'leo';"
        self.cur.execute(query)
        records = self.cur.fetchall()
        batch = []
        for row in records:
            term = row[0]  # term
            value = row[1]  # value

            en = ""
            if self.target.lower() in json.loads(value).keys():
                leo_res = json.loads(value)[self.target.lower()]

                ### LEO
                en = self.leo_translations(leo_res)
                en = common.remove_dangling_letter(en)

            ### DWDS ## move to dw module ...
            dw_query = f"select value from german where update = '{target_date}' and  sense = '{self.target}' and  ktype = 'dwds' and term = '{term}';"
            self.cur_dwds.execute(dw_query)
            dw_records = self.cur_dwds.fetchall()
            dw_val = ""

            for dw_row in dw_records:
                dw_val = dw_row[0]
                #print(dw_val)
                dw_lst = json.loads(dw_val)
                #print(f"loaded json ---------------------------- {type(dw_lst)}")
                inline_examples = self.dwds_inline_examples(dw_lst)
                korpora_examples = self.dwds_korpora_examples(dw_lst)
                entry = f"{term} @@@{en}{const.nl}{const.aline}{const.nl}{inline_examples}{const.aline}{const.nl}{korpora_examples}§§§"
                print(entry)
                batch.append(entry)
        if len(batch) == const.MAX_CARDS:
            self.write_to_file(batch, self.create_batch_name())
            batch = []

        self.write_to_file(batch, self.create_batch_name())


    def write_to_file(self, lst, filename):
        print(f"writing to file {filename}")
        f = open(filename, "w")
        with f:
            for i in lst:
                f.write(f"{i}")

    def create_batch_name(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        return const.cards_path + self.target + "_" + st + ".txt"

    def leo_translations(self, lst):
        str = ""
        definition = {}
        en_translations = []
        de_conjugation = lst[0]["de"]
        # restrict translations
        upper = min(len(lst), const.max_card_entries)
        for i in lst[0:upper]:
            ent = i["en"]
            # print(f"english {ent}")
            split = ent.split("|")[0]
            en_translations.append(split.strip())
        definition[de_conjugation] = en_translations
        # format
        str = de_conjugation + const.aline + "\n" + "  ▪  ".join(en_translations)
        str = common.remove_dangling_letter(str)
        return str



    def dwds_inline_examples(self, dict):


        temp = []
        dwds = ""

        if "inline_examples" not in dict.keys():
            return dwds

        lst = dict["inline_examples"]


        for i in lst:

            definition = i["definition"]
            temp.append(definition + "\n\n")

            examples = i["examples"]

            for ex in examples:
                splits = ex.split("\n")
                for de in splits:
                    if ("Beispiele" in de) or ("Beispiel" in de):
                        pass
                    else:
                        translator = Translator()
                        en = translator.translate(de, src='de', dest='en').text
                        #en = "This is english"
                        time.sleep(5)
                        temp.append("▢  " + de + " ▪ " + en + "\n\n")
            dwds = "".join(temp)

        return dwds

    def dwds_korpora_examples(self, dict):
        """
        :param dict:
        :return:
        """

        dwds = ""
        temp = []
        lst = dict["korpora_examples"]
        if len(lst) > 0:
            nr = min(2, len(lst))
            for de in lst[0:nr]:
                translator = Translator()
                en = translator.translate(de, src='de', dest='en').text
                #en = "This is english"
                time.sleep(5)
                temp.append("▢  " + de + " ▪ " + en + "\n\n")
        dwds = "".join(temp)
        return dwds


if __name__ == "__main__":

    pg = Verb_Cards()
    pg.create('2020-06-18 19:54:47')
