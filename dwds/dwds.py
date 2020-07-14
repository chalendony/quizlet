import constants as const
import requests
from requests_html import HTMLSession
from translations.database_handler import connect_alchemy
import json

engine = connect_alchemy(const.postgres_config)
from translations.database_handler import connect
import time

conn = connect(const.postgres_config)
cur = conn.cursor()


def examples(term , pos, target_date, limit):

    query = f"select  value from german where update = '{target_date}' and  sense = '{pos}' and  ktype = 'dwds' and term='{term}';"
    #print(query)
    cur.execute(query)
    records = cur.fetchall()
    batch = []
    for row in records:
        value = row[0]  # value
        dw_lst = json.loads(value)
        inline_examples = dwds_inline_examples(dw_lst, limit)
    return inline_examples


def get_translation(term):
    # pos
    wortart = ""
    url = f"https://www.dwds.de/api/wb/snippet?q={term}"

    try:
        session = HTMLSession()
        response = session.get(url)
        txt = response.text
        # [{"url":"https://www.dwds.de/wb/Haus","wortart":"Substantiv","lemma":"Haus","input":"Haus"}]
        jobj = json.loads(txt)
        # wortart = jobj[0]["wortart"]

    except requests.exceptions.RequestException as e:
        print(e)

    return wortart


def get_pos(term):
    # pos
    wortart = ""
    url = f"https://www.dwds.de/api/wb/snippet?q={term}"

    try:
        session = HTMLSession()
        response = session.get(url)
        txt = response.text
        # [{"url":"https://www.dwds.de/wb/Haus","wortart":"Substantiv","lemma":"Haus","input":"Haus"}]
        jobj = json.loads(txt)
        wortart = jobj[0]["wortart"]

    except requests.exceptions.RequestException as e:
        print(e)

    return wortart


def search(term):

    url = const.dwds_base_url + term
    print(f"url {url}")

    try:
        session = HTMLSession()
        response = session.get(url)

    except requests.exceptions.RequestException as e:
        print(e)

    korpora_examples = get_korpora_examples(response)
    # print(korpora_examples)

    selector = ".dwdswb-lesart"
    lesart = response.html.find(selector)
    # print(f"Number entries: {len(lesart)}")
    fin = {}

    if len(lesart) > 0:
        lst = []

        for i in lesart:

            if "id" in i.attrs:
                d = {}
                id = i.attrs["id"]

                definition = get_definition(id, response)
                # print(definition)
                # lst.append(definition + "\n")

                examples_level1 = get_examples_level1(id, response.html)
                # print(f"examples: {examples_level1}")

                d["id"] = id
                d["definition"] = definition
                d["examples"] = examples_level1
                lst.append(d)
        fin["inline_examples"] = lst
    fin["korpora_examples"] = korpora_examples

    return fin


def get_korpora_examples(res):
    lst = []
    selector = "div.dwds-gb-list > div"
    lesart = res.html.find(selector)
    # print(f"length {len(lesart)}")
    if len(lesart) > 0:
        for i in lesart:
            # print(i.text)
            lst.append(i.text + "\n")
    return lst


def get_examples_level1(id, i):
    result = []
    selector = f"#{id} > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele"
    # selector = f".dwdswb-kompetenzbeispiel"
    ex = i.find(selector)
    if len(ex) > 0:
        for t in ex:
            result.append(t.text)
    return result


def get_examples_level2(id, i):
    result = []

    selector = f"#{id} > div.dwdswb-lesart-content > div.dwdswb-lesart > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele"
    selector = f"#{id} > div.dwdswb-lesart-content > div.dwdswb-lesart > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele > div"

    ex = i.find(selector)
    if len(ex) > 0:
        for t in ex:
            result.append(t.text)
    return result


def get_definition(val, response):
    definition = ""
    sel_def = f"#{val} > div.dwdswb-lesart-content > div.dwdswb-lesart-def"
    w = response.html.find(sel_def)  ## examples
    if len(w) > 0:
        definition = val + ": " + w[0].text
    return definition


def clean_text(txt):
    # remove Bei
    txt = txt.replace("Beispiel:", "")
    return txt


def dwds_korpora_examples(dict):
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
            # en = translator.translate(de, src='de', dest='en').text
            # en = "This is english"

            url = f"""https://api.deepl.com/v2/translate?auth_key={const.dlapikey}&text={de}&source_lang=DE&target_lang=EN"""
            r = requests.get(url)
            en = r.json()["translations"][0]["text"]

            time.sleep(5)
            temp.append("▢  " + de + " ▪ " + en + "\n\n")
    dwds = "".join(temp)
    return dwds


def dwds_inline_examples(dict, limit):

    temp = []
    dwds = ""

    if "inline_examples" not in dict.keys():
        return dwds

    lst = dict["inline_examples"]

    # limit the number of examples
    exLimit = limit
    upperexLimit = min(exLimit, len(lst))
    for i in lst[0:upperexLimit]:

        definition = i["definition"]
        temp.append(definition + "\n\n")

        examples = i["examples"]

        for ex in examples:
            splits = ex.split("\n")
            upper = min(3, len(splits))
            for de in splits[0:upper]:
                if ("Beispiele" in de) or ("Beispiel" in de):
                    pass
                else:
                    ## roughly make is a sentence, get better translation is some cases
                    de = de[0].upper() + de[1:] + "."
                    url = f"""https://api.deepl.com/v2/translate?auth_key={const.dlapikey}&text={de}&source_lang=DE&target_lang=EN"""
                    r = requests.get(url)
                    en = r.json()["translations"][0]["text"]
                    temp.append("▢  " + de + " ▪ " + en + "\n\n")
                    time.sleep(1)
        dwds = "".join(temp)

    return dwds


if __name__ == "__main__":
    res = search("erwerben")
    print(res)
