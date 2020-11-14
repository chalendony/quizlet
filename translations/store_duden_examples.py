import duden
from psycopg2.extras import execute_values
import psycopg2
timestamp = '2020-11-14 18:23:58'
ktype = 'duden'
from time import sleep
from random import randint
import constants as const
from translations.database_handler import connect
import json

def get_word_url(term):
    res = duden.search(term, return_words=False)
    print(f"found {len(res)} sense(s).")
    if len(res) > 1:
        res = res[0]
    return res

def get_entry(word_url):
    w = duden.get(word_url)
    if w is not None:
        w = w.export()
    else:
        w = None
    return w

def store(insert=True):
    query = "select distinct term, sense from public.german;"
    conn = connect(const.postgres_config)
    cur = conn.cursor()
    cur2 = conn.cursor()
    cur.execute(query)
    res = cur.fetchall()

    for t in res:
        url = get_word_url(t[0])
        if len(url) > 1:
            url = url[0]
        # make lst
        #bhla = []
        #bhla.append(url)
        pos_of_speech = t[1]
        for l in url: # assume there is only 1

            print(f" get entry {l}")
            entry = get_entry(l)
            if entry is not None:
                print(entry)
                tup = (t[0], pos_of_speech, ktype, json.dumps(entry, ensure_ascii=False), timestamp)
                lst = []
                lst.append(tup)
                insert_entry(lst, cur2, conn)
                print(lst)
                time = randint(const.min_secs, const.max_secs)
                print(f"time : {time}")
                sleep(time)


def insert_entry(lst, cur, conn):
    sql = """INSERT INTO german(term, sense, ktype, value, update)
             VALUES %s
             on conflict do nothing;"""
    try:
        execute_values(cur, sql, lst)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"postgress error::  {error}")



if __name__ == '__main__':
    store()
