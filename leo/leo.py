#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Query the dictionary http://dict.leo.org/ from within Python.
# This is based on an equivalent script for German/English by:
#
# Copyright (C) 2015 Ian Denhardt <ian@zenhack.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------
# Usage:
# ------------------------------------------------------------------------------
# import LeoAccess as leo
# ret = leo.search("some string")
# ------------------------------------------------------------------------------
# 'ret' will be {} if nothing found or any error, or contain a dictionary with a
# variable number of 'section_names' (see below) as keys.
# The value of each key is a list of sub-dictionaries of word pairs
# {"sl": "source", "de": "german"}.
# When required, the dictionary 'sn_de' can be used to translate section_names
# into German.
# ------------------------------------------------------------------------------
# Dependencies:
# requests, lxml, io
# ------------------------------------------------------------------------------
import requests
from lxml import etree
from io import StringIO
import unicodedata
import re
import json

import constants as const
from translations.database_handler import connect
conn = connect(const.postgres_config)
cur = conn.cursor()

matcher = re.compile(r"^[^\|]*")
# ==============================================================================
# Constants
# ==============================================================================
sl = 'en'  # default source language (Spanish - Español)
tl = 'de'  # target language (German). Actually a constant:
# LEO is a German company

uri = 'https://dict.leo.org/german-english/'

#uri = 'http://dict.leo.org/german-english/'  # LEO uri
section_names = (
    'subst',
    'verb',
    'adjadv',
    'praep',
    'definition',
    'phrase',
    'example',
)

# ==============================================================================
# for translating section names to target language (German) - not used here
# ==============================================================================
sn_de = {'subst': "Substantiv",
         'verb': "Verb",
         'adjadv': "Adj./Adv.",
         'praep': "Praeposition",
         'definition': "Definition",
         'phrase': "Phrase",
         'example': "Beispiel", }


def _get_text(elt):
    buf = StringIO()

    def _helper(_elt):
        if _elt.text is not None:
            buf.write(str(_elt.text))
        for child in _elt:
            _helper(child)
        if _elt.tail is not None:
            buf.write(str(_elt.tail))

    _helper(elt)
    return buf.getvalue()

def search(term, timeout=None):
    '''term = search term
    lang = source language, one of en, es, it, fr, pt, ch, ru, pt, pl
    timeout = None or max. number of seconds to wait for response'''
    url = uri + term
    print(f"url {url}")
    resp = requests.get(url, params={'search': term}, timeout=timeout)
    ret = {}
    if resp.status_code != requests.codes.ok:
        return ret
    p = etree.HTMLParser()
    html = etree.parse(StringIO(resp.text), p)
    for section_name in section_names:
        section = html.find(".//div[@id='section-%s']" % section_name)
        if section is None:
            continue
        ret[section_name] = []
        results = section.findall(".//td[@lang='%s']" % (sl,))  # source language
        for r_sl in results:
            r_tl = r_sl.find("./../td[@lang='%s']" % (tl,))  # target language
            ret[section_name].append({
                sl: _get_text(r_sl).strip(),
                tl: _get_text(r_tl).strip(),
            })
    return ret


def clean_english_ppt(str):
    m = matcher.match(str)
    return m.group(0)


def clean_unicode(str):
    new_str = unicodedata.normalize("NFKD", str)
    return new_str

# def de_get_verbs_german_translation(res):
#     lst = []
#     if 'verb' in res:
#         upper_val = min(3,len(res['verb']))
#         for i in range(0,1):
#             str = res['verb'][i]['de']
#             clean = clean_unicode(str)
#             lst.append(clean.strip())
#     else:
#         lst.append('-')
#     return lst
#
#
#
# def get_verbs_english_definitions(res):
#     lst = []
#     if 'verb' in res:
#         upper_val = min(3,len(res['verb']))
#         for i in range(0,upper_val):
#             str = res['verb'][i]['en']
#             clean = clean_unicode(str)
#             clean = clean_english_ppt(clean)
#             lst.append(clean.strip())
#     else:
#         lst.append('-')
#     return lst
#####


def de_get_german_translation(res,part_of_speech):
    lst = []
    if part_of_speech in res:
        #print(f" leo dict  {res[part_of_speech]}")
        upper_val = min(3,len(res[part_of_speech]))
        for i in range(0,1):
            str = res[part_of_speech][i]['de']
            clean = clean_unicode(str)
            lst.append(clean.strip())
    else:
        lst.append('-')
    return lst



def get_english_definitions(res, part_of_speech):
    lst = []
    if part_of_speech in res:
        upper_val = min(3,len(res[part_of_speech]))
        for i in range(0,upper_val):
            str = res[part_of_speech][i]['en']
            clean = clean_unicode(str)
            clean = clean_english_ppt(clean)
            lst.append(clean.strip())
    else:
        lst.append('-')
    return lst

def leo_verb_conjugations(term, target_date):
    query = f"select value from german where update = '{target_date}' and  sense = '{const.VERB}' and  ktype = 'leo' and term = '{term}';"
    cur.execute(query)
    records = cur.fetchall()
    lst = []
    de_conjugation = ""
    for row in records:
        value = row[0]  # value
        entry = json.loads(value)
        if const.VERB.lower() in entry.keys():
            lst = entry[const.VERB.lower()]
            de_conjugation = lst[0]["de"]
    return de_conjugation



def leo_noun_(term, target_date):
    query = f"select value from german where update = '{target_date}' and  sense = '{const.SUBS}' and  ktype = 'leo' and term = '{term}';"
    cur.execute(query)
    records = cur.fetchall()
    lst = []
    de_conjugation = ""
    for row in records:
        value = row[0]  # value
        entry = json.loads(value)
        if 'subst' in entry.keys():
            lst = entry['subst']
            de_conjugation = lst[0]["de"]
    return de_conjugation


def leo_article(term, target_date):
    query = f"select value from german where update = '{target_date}' and  sense = '{const.SUBS}' and  ktype = 'leo' and term = '{term}';"
    cur.execute(query)
    records = cur.fetchall()
    lst = []
    article = ""
    de_conjugation = ""
    for row in records:
        value = row[0]  # value
        entry = json.loads(value)
        if 'subst' in entry.keys():
            lst = entry['subst']
            de_conjugation = lst[0]["de"]
            splits = de_conjugation.split()
            article = splits[0]
    return article


if __name__ == "__main__":
    # get term
    res = search('wirken')
    print(res)

    #en = get_verbs_english_definitions(res)
    #print(en)

    #de = de_get_verbs_german_translation(res)
    #print(de)


