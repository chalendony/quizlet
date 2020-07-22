import itertools

##['get', 'reach', 'arrive', 'enter', 'go', 'access', 'come', 'achieve', 'move', 'find', 'pass', 'getting', 'will take', 'attain', 'reached', 'attain to']
##[('Außerdem können solche gefälschten Arzneimittel zu Patienten in Drittländern <em>gelangen</em>.', 'In addition, those falsified medicinal products may <em class="both">reach</em> patients in third countries.'), ('Aufgrund dieser Fakten <em>gelangen</em> die Mitglieder dieses Parlaments allerdings zu unterschiedlichen Schlussfolgerungen.', 'The Members of this Parliament do, however, <em class="both">reach</em> different conclusions based on facts.'), ('Hierdurch kann immer Bremsdruck an wenigstens eine Radbremse <em>gelangen</em>.', 'In this way brake pressure can always <em class="both">reach</em> at least one wheel brake.')]
import re

from reverso_context_api import Client

client = Client("de", "en")

def translation(de):
    v = list(client.get_translations(de))
    return v

def examples(de, en_target, limit):
    ex = list(itertools.islice(client.get_translation_samples("gelangen", target_text="reach" ,cleanup=False), limit))
    return ex

def reverso_translation(de, limit):
    temp = []
    lst = translation(de)
    for en in lst:
        ex = examples(de, en, limit)
        for j in ex:
            d = {}
            d['source'] = cleanup_html_tags(j[0])
            d['target'] = cleanup_html_tags(j[1])
            temp.append(d)
    return temp


def cleanup_html_tags(text):
    """Remove html tags like <b>...</b> or <em>...</em> from text
    I'm well aware that generally it's a felony, but in this case tags cannot even overlap
    """
    return re.sub(r"<.*?>", "", text)



if __name__ == "__main__":
    rev = reverso_translation("gelangen", 2)
    print(rev)