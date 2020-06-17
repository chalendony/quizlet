import constants as const
import requests
from requests_html import HTMLSession
from translations.database_handler import connect_alchemy
import json
engine = connect_alchemy(const.postgres_config)



def get_pos(term):
    # pos
    url = (f"https://www.dwds.de/api/wb/snippet?q={term}")

    try:
        session = HTMLSession()
        response = session.get(url)

    except requests.exceptions.RequestException as e:
        print(e)

    txt = response.text
    # [{"url":"https://www.dwds.de/wb/Haus","wortart":"Substantiv","lemma":"Haus","input":"Haus"}]
    jobj = json.loads(txt)
    wortart = jobj[0]["wortart"]
    return wortart



import time



def search(term):



    url = const.dwds_base_url + term
    print(f"url {url}")

    try:
        session = HTMLSession()
        response = session.get(url)

    except requests.exceptions.RequestException as e:
        print(e)

    korpora_examples = get_korpora_examples(response)
    print(korpora_examples)

    selector = ".dwdswb-lesart"
    lesart = response.html.find(selector)
    #print(f"Number entries: {len(lesart)}")

    lst = []
    if len(lesart) > 0:
        for i in lesart:
            if 'id' in i.attrs:
                id = i.attrs['id']
                definition = get_definition(id,response)
                print(definition)
                lst.append(definition + "\n")

                examples_level1 = get_examples_level1(id,response.html)
                print(f"examples: {examples_level1}")

                #examples_level2 = get_examples_level2(id, i)
                #print(f"examples-2: {examples_level2}")

                #"#d-1-1-1 > div.dwdswb-lesart-content > div.dwdswb-lesart > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele"
                # selector = f".dwdswb-kompetenzbeispiel"
                #"#d-1-1-1 > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele"
                #"#d-1-1-1 > div.dwdswb-lesart-content > div.dwdswb-lesart > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele"
                # ex = i.find(selector)
                # if len(ex) > 0:
                #     for j in ex:
                #        print(f"text {j.text}")
                #        lst.append(j.text + "\n")
                # else:
                #     print(f"alternative examples: ")
                #     selector = "div.dwds-gb-list > div"
                #     lesart = response.html.find(selector)
                #     print(f"length {len(lesart)}")
                #     if len(lesart) > 0:
                #         for i in lesart:
                #             print(i.text)
                #             lst.append(i.text + "\n")
                #     else:
                #         print("***********************  No Translations obtained **********************")
    return lst

def get_korpora_examples(res):
    lst = []
    selector = "div.dwds-gb-list > div"
    lesart = res.html.find(selector)
    #print(f"length {len(lesart)}")
    if len(lesart) > 0:
        for i in lesart:
            #print(i.text)
            lst.append(i.text + "\n")
    return lst

def get_examples_level1(id,i):
    result = []
    selector = f"#{id} > div.dwdswb-lesart-content > div.dwdswb-verwendungsbeispiele"
    #selector = f".dwdswb-kompetenzbeispiel"
    ex = i.find(selector)
    if len(ex) > 0:
        for t in ex:
            result.append(t.text)
    return  result


def get_examples_level2(id,i):
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
    txt = txt.replace('Beispiel:', "")
    return  txt


if __name__ == "__main__":
    search('erwerben')
