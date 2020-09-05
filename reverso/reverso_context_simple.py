import itertools

##['get', 'reach', 'arrive', 'enter', 'go', 'access', 'come', 'achieve', 'move', 'find', 'pass', 'getting', 'will take', 'attain', 'reached', 'attain to']
##[('Außerdem können solche gefälschten Arzneimittel zu Patienten in Drittländern <em>gelangen</em>.', 'In addition, those falsified medicinal products may <em class="both">reach</em> patients in third countries.'), ('Aufgrund dieser Fakten <em>gelangen</em> die Mitglieder dieses Parlaments allerdings zu unterschiedlichen Schlussfolgerungen.', 'The Members of this Parliament do, however, <em class="both">reach</em> different conclusions based on facts.'), ('Hierdurch kann immer Bremsdruck an wenigstens eine Radbremse <em>gelangen</em>.', 'In this way brake pressure can always <em class="both">reach</em> at least one wheel brake.')]
import re
import time
from random import randint
from time import sleep
import constants as const

from reverso_context_api import Client


client = Client("de", "en")

# not using at moment...
def reverso_context(de, max_examples=5):
    temp = []
    # serve call
    sense = translation(de) # i could get the senses on my own after downloading the page to avoid a call
    val = min(len(sense),max_examples)
    for en in sense[0:val]:
        a = {}
        a['sense'] = en
        # service call is good because i can specify the sense for the context
        #ex = examples(de, en, max_examples) # limit examples
        ## call to server
        ex = client.my_get_translation_samples(de, target_text=en, cleanup=True) # only called for one page

        b = []
        for j in ex:
            d = {}
            d['de'] = j[0]
            d['en'] = j[1]
            b.append(d)
        a['examples'] = b
        temp.append(a)
        print(a)
        time = randint(const.min_secs, const.max_secs)
        print(time)
        sleep(time)
    # store temp to database
    return temp


def reverso_senses(de, max_examples=2):
    # only one call to the server for each term, do not get the context
    # serve call
    sense = translation(de)
    return sense

def translation(de):
    v = list(client.get_translations(de))
    return v


def examples(de, sense):
    '''
    get example sentence for a word and its sense. Modified to only call the server once per term, html
    tags are returned (by setting cleanup to false) so that baustein text can easily be created by replace html with placeholder
    :param de:
    :param sense:
    :return:
    '''
    ## modified to only call once
    #ex = list(itertools.islice(client.my_get_translation_samples(de, target_text=en_target ,cleanup=False), limit))
    res = client.my_get_translation_samples(de, target_text=sense, cleanup=False)
    return res



if __name__ == "__main__":
    ## get the translations
    #rev = reverso_senses("stellen", 5)
    #print(rev)

    ## get example sentences
    de  = examples("fortan", "henceforth")
    print(list(de))

