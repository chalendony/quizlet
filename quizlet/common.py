from leo.leo import clean_unicode
from psycopg2.extras import execute_values
import psycopg2
from translations.database_handler import connect
import constants as const


conn = connect(const.postgres_config)
cur = conn.cursor()


def insert_entry(lst):
    sql = """INSERT INTO german(term, sense, ktype, value, update)
             VALUES %s
             on conflict do nothing;"""
    try:
        execute_values(sql, lst)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"postgress error {error}")


def format_english(lst):
    tmp = []
    for i in lst:
        clean = clean_unicode(i['en'])
        clean = clean.replace('AE', "")
        clean = clean.replace('BE', "")
        tmp.append(clean.strip())
    str = ' ▪ '.join(tmp)
    return str

def remove_dangling_letter(str):
    clean = str.replace("AE", "")
    clean = clean.replace("BE", "")
    return clean

def terms_from_list():
    pass

def term_from_db():
    pass