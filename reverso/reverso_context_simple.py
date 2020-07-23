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

def reverso_examples(de, max_examples=3):
    temp = []
    # serve call
    sense = translation(de) # i could get the senses on my own after downloading the page to avoid a call
    val = min(len(sense),max_examples)
    for en in sense[0:val]:
        a = {}
        a['sense'] = en
        # service call is good because i can specify the sense for the context
        #ex = examples(de, en, max_examples) # limit examples
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

    return temp


def translation(de):
    v = list(client.get_translations(de))
    return v

def examples(de, en_target, limit):
    ## modified to only call once
    #ex = list(itertools.islice(client.my_get_translation_samples(de, target_text=en_target ,cleanup=False), limit))
    ex = client.my_get_translation_samples(de, target_text=en_target, cleanup=False)
    return ex



if __name__ == "__main__":
    rev = reverso_examples("stellen", 5)
    print(rev)


  #  "{"subst": [{"en": "job", "de": "die Stelle  pl.: die Stellen"}, {"en": "place", "de": "die Stelle  pl.: die Stellen"}, {"en": "appointment", "de": "die Stelle  pl.: die Stellen"}, {"en": "position", "de": "die Stelle  pl.: die Stellen"}, {"en": "post", "de": "die Stelle  pl.: die Stellen"}, {"en": "spot", "de": "die Stelle  pl.: die Stellen"}, {"en": "location", "de": "die Stelle  pl.: die Stellen"}, {"en": "point", "de": "die Stelle  pl.: die Stellen"}, {"en": "site", "de": "die Stelle  pl.: die Stellen"}, {"en": "situation", "de": "die Stelle  pl.: die Stellen"}, {"en": "stead", "de": "die Stelle  pl.: die Stellen"}, {"en": "digit", "de": "die Stelle  pl.: die Stellen"}, {"en": "engagement", "de": "die Stelle  pl.: die Stellen"}, {"en": "station", "de": "die Stelle  pl.: die Stellen"}], "verb": [{"en": "to put   | put, put |", "de": "stellen  | stellte, gestellt |"}, {"en": "to set so./sth.   | set, set |", "de": "jmdn./etw. stellen  | stellte, gestellt |"}, {"en": "to place   | placed, placed |", "de": "stellen  | stellte, gestellt |"}, {"en": "to lay   | laid, laid |", "de": "stellen  | stellte, gestellt |"}, {"en": "to provide sth.   | provided, provided |", "de": "etw.acc. stellen  | stellte, gestellt |   - bereitstellen"}, {"en": "to position   | positioned, positioned |", "de": "stellen  | stellte, gestellt |"}, {"en": "to regulate   | regulated, regulated |", "de": "stellen  | stellte, gestellt |"}, {"en": "to supply   | supplied, supplied |", "de": "stellen  | stellte, gestellt |"}, {"en": "to switch   | switched, switched |", "de": "stellen  | stellte, gestellt |"}, {"en": "to throw   | threw, thrown |", "de": "stellen  | stellte, gestellt |"}, {"en": "to give oneself up (to so.)", "de": "sichacc. (jmdm.) stellen  | stellte, gestellt |"}, {"en": "to turn oneself in   - to the police", "de": "sichacc. stellen  | stellte, gestellt |   - der Polizei"}, {"en": "to adjust sth.   | adjusted, adjusted |", "de": "etw.acc. stellen  | stellte, gestellt |"}, {"en": "to surrender   | surrendered, surrendered |", "de": "sichacc. stellen  | stellte, gestellt |"}], "adjadv": [{"en": "to the fore", "de": "zur Stelle"}, {"en": "ranking  adj.", "de": "eine Stelle innehabend"}, {"en": "in place", "de": "an der Stelle"}, {"en": "quarantinable  adj.", "de": "unter Quarantäne zu stellen"}, {"en": "in many places", "de": "an vielen Stellen"}, {"en": "elsewhere  adv.", "de": "an anderer Stelle"}, {"en": "at this point", "de": "an dieser Stelle"}, {"en": "in lieu thereof", "de": "an dessen Stelle"}, {"en": "tertiary  adj.", "de": "an dritter Stelle"}, {"en": "in respective area", "de": "an entsprechender Stelle"}, {"en": "in the first place", "de": "an erster Stelle"}, {"en": "second to none", "de": "eindeutig an erster Stelle"}, {"en": "in situ", "de": "an Ort und Stelle"}, {"en": "on the spot", "de": "an Ort und Stelle"}], "praep": [{"en": "in lieu of", "de": "anstelle   or: an Stelle  prep.  +gen."}], "definition": [{"en": "braai (S.A.)", "de": "offene Grill- und Feuerstelle"}], "phrase": [{"en": "Keep the set. [SPORT.]", "de": "Boot stellen!   - Ruderkommando"}, {"en": "Set the boat. [SPORT.]", "de": "Boot stellen!   - Ruderkommando"}, {"en": "to turn everything topsy-turvy", "de": "alles auf den Kopf stellen"}, {"en": "to turn the place upside down", "de": "die Bude auf den Kopf stellen"}, {"en": "to turn so.'s place upside down", "de": "jmdm. die Bude auf den Kopf stellen"}, {"en": "to severely criticiseBE so./sth.", "de": "jmdn./etw. an den Pranger stellen [fig.]"}, {"en": "to severely criticizeAE so./sth.", "de": "jmdn./etw. an den Pranger stellen [fig.]"}, {"en": "to turn sth. inside out [fig.]", "de": "etw.acc. auf den Kopf stellen [fig.]"}, {"en": "to turn sth. upside down", "de": "etw.acc. auf den Kopf stellen [fig.]"}, {"en": "You can talk until you're blue in the face!", "de": "Und wenn du dich auf den Kopf stellst!"}, {"en": "a sensitive spot", "de": "eine empfindliche Stelle"}, {"en": "a tender spot", "de": "eine empfindliche Stelle"}, {"en": "a tender spot", "de": "eine empfindsame Stelle"}, {"en": "a sore spot", "de": "eine schmerzhafte Stelle"}, {"en": "top priority", "de": "an erster Stelle"}], "example": [{"en": "Make sure that ...", "de": "Stellen Sie sicher, dass ..."}, {"en": "He's a hard man to please.", "de": "Er ist kaum zufrieden zu stellen."}, {"en": "would like to demonstrate our proficiency", "de": "möchten unsere Leistung unter Beweis stellen"}, {"en": "We place our services at your disposal.", "de": "Wir stellen Ihnen unsere Dienste zur Verfügung."}, {"en": "with an accuracy of two digits after the decimal point", "de": "mit einer Genauigkeit von zwei Stellen hinter dem Komma"}, {"en": "in order to provide", "de": "um bereitzustellen"}, {"en": "He set the alarm for seven o'clock.", "de": "Er stellte den Wecker auf sieben Uhr."}, {"en": "I conclude that", "de": "Ich stelle fest, dass"}, {"en": "Two of the men turned out to have family problems.", "de": "Bei zwei Männern stellte sich heraus, dass sie familiäre Probleme hatten."}, {"en": "She acts like the queen bee.", "de": "Sie stellt sich immer in den Mittelpunkt."}, {"en": "the party making a request for conciliation", "de": "die Partei, die einen Schlichtungsantrag stellt"}, {"en": "in his place", "de": "an seiner Stelle"}, {"en": "a particular point", "de": "eine bestimmte Stelle"}, {"en": "a lonely spot", "de": "eine einsame Stelle"}]}"