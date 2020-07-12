import os
import json
import requests
from bs4 import BeautifulSoup

apikey = os.getenv('PONS')

HITS = 'hits'
ROMS = "roms"
WORD_CLASS = "wordclass"
ARABS = "arabs"
TRANSLATIONS = "translations"
HEADER = "header"

def get(term):

    url = "https://api.pons.com/v1/dictionary"
    headers = {"X-Secret":apikey}
    params = {'q':term, 'l':'deen', 'in':'de'}
    response = requests.get(url, headers=headers, params=params)
    return response


def search(term):
    txt = get(term)
    print(txt.json())


def strip_html(json_str):
    soup = BeautifulSoup(json_str, "lxml")
    txt = soup.text
    return txt


def hits(txt):
    lst = txt[HITS]
    return lst


def roms(txt):
    t = txt[ROMS]
    return t


def parse(s):
    s = strip_html(s)
    s = s.replace('\n', '')
    #print(s)
    s = json.loads(s)
    s = s[0]
    hlst = hits(s)
    #print(f"hits {len(hlst)}")

    for i in hlst:
        rlst = roms(i)
        #print(f"roms {len(rlst)}")

        for j in rlst:
            wordclass = j[WORD_CLASS]
            print(f"wordclass {wordclass}")

            for k in j[ARABS]:
                header = k[HEADER]
                print(f"header{header}")

                for l in k[TRANSLATIONS]:
                    print(f"translations {l}")
                    #translations = l[TRANSLATIONS]
                    #print(f"translations: {translations}")


if __name__ == "__main__":
    search('einführen')
    #parse(json_str)
    #striphtml(json)
#[{"lang":"de","hits":[{"type":"entry","opendict":false,"roms":[{"headword":"war·ten","headword_full":"war·ten1 [ˈvartn̩] VB intr","wordclass":"intransitive verb","arabs":[{"header":"1. warten (harren):","translations":[{"source":"warten","target":"to wait"},{"source":"auf jdn/etw warten
