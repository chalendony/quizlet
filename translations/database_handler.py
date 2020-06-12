from configparser import ConfigParser

import psycopg2
from reverso import constants as const
from sqlalchemy import create_engine

def dbconf(filename, section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return db


def connect(filename, section="postgresql"):
    db = dbconf(filename, section="postgresql")
    conn = psycopg2.connect(
        host=db['host'], database=db['database'], user=db['user'], password=db['password']
    )
    return conn


def connect_alchemy(filename, section="postgresql"):
    # ====== Connection ======
    # Connecting to PostgreSQL by providing a sqlachemy engine
    db = dbconf(filename, section="postgresql")

    engine = create_engine(
        'postgresql://' + db['user'] + ':' + db['password'] + '@' + db['host'] + ':' + '5432' + '/' + db['database'],
        echo=False)

    return engine

def write_to_file(self, lst, batchnr, filename):
    f = open(const.cards_path + filename + "_" + str(batchnr) + ".txt", 'w')
    with f:
        for i in lst:
            f.write(f"{i}")