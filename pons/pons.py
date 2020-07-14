import os
import json
import requests
from bs4 import BeautifulSoup
import constants as const

apikey = os.getenv('PONS')

HITS = 'hits'
ROMS = "roms"
WORD_CLASS = "wordclass"
ARABS = "arabs"
TRANSLATIONS = "translations"
HEADER = "header"
SOURCE = "source"
TARGET = 'target'

MAX_HEADER = 2
MAX_TRANSLATION = 3
def get(term):

    url = "https://api.pons.com/v1/dictionary"
    headers = {"X-Secret":apikey}
    params = {'q':term, 'l':'deen','in':'de'}
    response = requests.get(url, headers=headers, params=params)
    return response


def search(term):
    resp = get(term)
    #print(f"response:{resp}")
    #print(f"text:{resp.text}")
    if resp.status_code == 200:
        s = strip_html(resp.text)
        s = s.replace('\n', '')
        s = json.loads(s)
    else:
        s = ""
    return s


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

def underline(string):
    emptystring = ''
    for i in range(0, len(string)):

        if string[i] == ' ':
            emptystring = emptystring + string[i]
        else:
            emptystring = emptystring + string[i] + str('\u0332')
            print
            f"\033[4m{string}033[0m"
    return  "\033[4m{string}033[0m"


def rote_memory_verb(s , pos):
    res = ""
    temp = []
    #s = s[0]
    hlst = hits(s)
    for i in hlst: # there is only one hits
        rlst = roms(i)

        for j in rlst:
            #print(f"j {j} ")

            if WORD_CLASS in j.keys() and pos.lower() in j[WORD_CLASS]:

                ul = "\033[4m" + j[WORD_CLASS] + "\033[0m"

                temp.append(f"{ul}\n") # word class

                for k in j[ARABS][0:MAX_HEADER]:
                    header = k[HEADER]
                    #temp.append(f"{const.aline}\n")
                    for l in k[TRANSLATIONS][0:MAX_TRANSLATION]:

                        # source
                        de = l[SOURCE].strip()

                        en = l[TARGET].strip()

                        temp.append("▢  " + de + " ▪ " + en + "\n\n")

    res = "".join(temp)
    return res

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
    search('abarbeiten')
    #parse(json_str)
#[{"lang":"de","hits":[{"type":"entry","opendict":false,"roms":[{"headword":"war·ten","headword_full":"war·ten1 [ˈvartn̩] VB intr","wordclass":"intransitive verb","arabs":[{"header":"1. warten (harren):","translations":[{"source":"warten","target":"to wait"},{"source":"auf jdn/etw warten
