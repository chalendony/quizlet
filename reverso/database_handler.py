from configparser import ConfigParser

import psycopg2


def connect(filename, section="postgresql"):
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

    conn = psycopg2.connect(
        host=db['host'], database=db['database'], user=db['user'], password=db['password']
    )
    return conn


def write_to_file(self, lst, batchnr, filename):
    f = open(const.cards_path + filename + "_" + str(batchnr) + ".txt", 'w')
    with f:
        for i in lst:
            f.write(f"{i}")