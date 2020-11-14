import duden
from  quizlet.common import term_from_db, insert_entry


#term, sense, ktype, value, update
timestamp = '2020-11-14 18:23:58'
ktype = 'duden'
number_senses = 1
#sense = # part of speech

def get_word_url(term,number_senses=1):
    ## TODO handle more senses...
    res = duden.search(term, return_words=False)
    print(f"found {type(res)} sense(s).")
    return res


def get_entry(word_url):
    w = duden.get(word_url)
    return w.export()


def store(terms, insert=True):
    # insert = True insert statement, o.w. update statement

    for t in terms:
        url = get_word_url(t)
        print(url)
        for l in url: # assume there is only 1
            lst = []
            print(l)
            entry = get_entry(l)
            print(entry)
            e = (t, entry['part_of_speech'], ktype, entry['meaning_overview'], timestamp)
            lst.append() # i dont know seems it wanted list last time
            if insert:
                # insert_entry(lst)
            else:
                # update_entry(lst)




if __name__ == '__main__':
    #terms = term_from_db()
    terms = ['abarbeiten']
    store(terms, insert=False) #
