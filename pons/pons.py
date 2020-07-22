import os
import json
import random


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



def flippity_verb(s , pos, term):
    "create flippity crossword cards, term comes first"
    res = ""
    temp = []
    hlst = hits(s)
    for i in hlst: # there is only one hits
        rlst = roms(i)
        for j in rlst:
            if WORD_CLASS in j.keys() and pos.lower() in j[WORD_CLASS] and 'adjective and adverb' not in j[WORD_CLASS]:
                for k in j[ARABS][0:MAX_HEADER]:
                    header = k[HEADER]
                    for l in k[TRANSLATIONS][0:MAX_TRANSLATION]:
                        en = l[TARGET].strip()
                        if en.startswith("to"):
                            en = en.replace(',', ' ')
                            temp.append(term + ','+ en + "\n")
    return temp



def remove_dups(lst):
    t = []
    for x in lst:
        if x not in t:
            t.append(x)
    return t

def remove_empty(lst):
    filtered = [x for x in lst if len(x.strip()) > 0]
    return filtered

def rote_memory_verb(s , pos):
    "repeat senses, remove the example sentences because cards are too long"
    res = ""
    temp = []
    #s = s[0]
    hlst = hits(s)
    for i in hlst: # there is only one hits
        rlst = roms(i)

        for j in rlst:
            if WORD_CLASS in j.keys() and pos.lower() in j[WORD_CLASS] and 'adjective and adverb' not in j[WORD_CLASS]:

                temp.append(f"{j[WORD_CLASS]}\n\n") # word class

                for k in j[ARABS][0:MAX_HEADER]:
                    header = k[HEADER]
                    for l in k[TRANSLATIONS][0:MAX_TRANSLATION]:

                        # source
                        de = l[SOURCE].strip()

                        en = l[TARGET].strip()

                        temp.append("▢  " + de + " ▪ " + en + "\n\n") # make a function so same code can be used for qui
    if len(temp) > 0:
        temp[-1] =temp[-1].rstrip()
        temp[-1] = temp[-1] + "\n"
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
