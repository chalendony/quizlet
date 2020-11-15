import duden
from psycopg2.extras import execute_values
import psycopg2

ktype = 'duden'
from time import sleep
from random import randint
import constants as const
from translations.database_handler import connect
import json

def get_word_url(term):
    res = duden.search(term, return_words=False)
    print(f"found {len(res)} sense(s).")
    #if len(res) > 1:
    #    res = res[0] # string
    return res

def get_entry(word_url):
    w = duden.get(word_url)
    if w is not None:
        w = w.export()
    else:
        w = None
    return w

def store(timestamp, insert=True):
    query = "select distinct term, sense from public.german;"
    conn = connect(const.postgres_config)
    cur = conn.cursor()
    cur2 = conn.cursor()
    cur.execute(query)
    res = cur.fetchall()

    for t in res:
        url = get_word_url(t[0])
        if len(url) > 1: # only get the first
            url = url[0]
        pos_of_speech = t[1]
        for l in url:

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

def parse_duden_context(entry):
    ## duden_entry :  {'name': 'zuschlagen', 'urlname': 'zuschlagen', 'title': 'zuschlagen', 'article': None, 'part_of_speech': 'starkes Verb', 'usage': None, 'frequency': 2, 'word_separation': ['zu', 'schla', 'gen'], 'meaning_overview': '\n\nBedeutungen (8)\n\nInfo\n\n\n\n\nmit Schwung, Heftigkeit geräuschvoll schließen\nGrammatik\nPerfektbildung mit „hat“\nBeispiele\n\nden Kofferraum zuschlagen\njemandem die Tür vor der Nase zuschlagen\nein Buch zuschlagen (zuklappen)\n\n\n\nmit einem Schlag (1b) zufallen\nGrammatik\nPerfektbildung mit „ist“\nBeispiel\n\npass auf, dass [dir] die Wohnungstür nicht zuschlägt\n\n\n\n\ndurch [Hammer]schläge [mit Nägeln o.\xa0Ä.] fest zumachen, verschließen\nGebrauch\nselten\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\neine Kiste zuschlagen\n\n\n\ndurch Schlagen, Hämmern in eine bestimmte Form bringen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nSteine für eine Mauer [passend] zuschlagen\n\n\n\nmit einem Schläger zuspielen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\ndem Partner den Ball zuschlagen\n\n\n\n\neinen Schlag (1a), mehrere Schläge gegen jemanden führen\nGrammatik\nPerfektbildung mit „hat“\nBeispiele\n\nkräftig, hart, mit der Faust zuschlagen\nder Täter holte aus und schlug zu\n〈in übertragener Bedeutung:〉 die Polizei schlug zu\n〈in übertragener Bedeutung:〉 das Schicksal, der Tod schlug zu\n\n\n\netwas Bestimmtes tun (besonders etwas, was jemand gewohnheitsmäßig tut, was typisch für ihn ist [und was allgemein gefürchtet ist, nicht gutgeheißen wird])\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nder Mörder hat wieder zugeschlagen\n\n\n\nsich beim Essen, Trinken keinerlei Zurückhaltung auferlegen\nGebrauch\numgangssprachlich\nGrammatik\nPerfektbildung mit „hat“\nBeispiele\n\nnach der Diät wieder [richtig, voll] zuschlagen können\nbeim Champagner haben sie ganz schön zugeschlagen\n〈in übertragener Bedeutung:〉 (umgangssprachlich) die Stadt will jetzt bei den Parkgebühren zuschlagen (will sie kräftig erhöhen)\n\n\n\nein Angebot, eine gute Gelegenheit o.\xa0Ä. wahrnehmen, einen Vorteil nutzen\nGebrauch\numgangssprachlich\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nbei diesem günstigen Angebot musste ich einfach zuschlagen\n\n\n\n\n\n(bei einer Versteigerung) durch Hammerschlag als Eigentum zuerkennen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\ndas Buch wurde [einer Schweizer Bieterin] mit fünftausend Euro zugeschlagen\n\n\n\nim Rahmen einer Ausschreibung (als Auftrag) erteilen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nder Auftrag, der Neubau wurde einer belgischen Firma zugeschlagen\n\n\n\nals weiteren Bestandteil hinzufügen, angliedern o.\xa0Ä.\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\ndas Haus wurde dem Erbe des Sohnes zugeschlagen\n\n\n\n\n(einen Betrag o.\xa0Ä.) auf etwas aufschlagen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\n[zu] dem/auf den Preis werden noch 10\u2004% zugeschlagen\n\n\n\neinen bestimmten Stoff bei der Herstellung von Mörtel und Beton oder bei der Verhüttung von Erzen zusetzen\nGebrauch\nBautechnik, Hüttenwesen\nGrammatik\nPerfektbildung mit „hat“\n\n\n', 'origin': None, 'compounds': {'adjektive': ['blitzschnell', 'eiskalt', 'erbarmungslos', 'erneut', 'gleich', 'gnadenlos', 'hart', 'richtig'], 'substantive': ['Autotür', 'Mal', 'Mörder', 'Nase', 'Schicksal', 'Transfermarkt', 'Tür', 'Wagentür']}, 'grammar_raw': None, 'synonyms': ['schließen, zuklappen, zuschmettern, zuwerfen'], 'words_before': ['zuschicken', 'zuschieben', 'zuschießen', 'zuschippen', 'Zuschlag'], 'words_after': ['zuschlagfrei', 'Zuschlagkalkulation', 'Zuschlagkarte', 'zuschlagpflichtig', 'Zuschlagsatz']}
    entry['article']
    context = entry['meaning_overview']
    parse_context(context)


def parse_context(c):
    # find meaning
    splits = c.split('Beispiel')
    print(splits)
    cnt = 0
    definition = []
    examples = []

    for i in splits:

        s2 = i.split('\n')
        cl = clean(s2)
        if cnt == 0:
            # first element is a def
            definition.append(cl[0])
        else:
            # last element is def
            definition.append(cl[-1])
            # rest example
            examples.append(cl[0:-1])
        cnt = cnt + 1


        print(f"DONE {cl}")

    merg = list(zip(definition, examples))
    for i in merg:

        print(i)



def clean(lst):
    temp = []
    for i in lst:
        if len(i) == 0 or i == 'e' or i.startswith('Bedeutungen', 0)  or i.startswith('Info', 0)  or i.startswith('Grammatik',0) \
                or i.startswith('Perfektbildung',0) or i.startswith('Gebrauch') or i.startswith('selten'):
            pass
        else:
            temp.append(i)

    return temp


timestamp = '2020-11-14 18:23:58'
if __name__ == '__main__':

    context = {'name': 'zuschlagen', 'urlname': 'zuschlagen', 'title': 'zuschlagen', 'article': None, 'part_of_speech': 'starkes Verb', 'usage': None, 'frequency': 2, 'word_separation': ['zu', 'schla', 'gen'], 'meaning_overview': '\n\nBedeutungen (8)\n\nInfo\n\n\n\n\nmit Schwung, Heftigkeit geräuschvoll schließen\nGrammatik\nPerfektbildung mit „hat“\nBeispiele\n\nden Kofferraum zuschlagen\njemandem die Tür vor der Nase zuschlagen\nein Buch zuschlagen (zuklappen)\n\n\n\nmit einem Schlag (1b) zufallen\nGrammatik\nPerfektbildung mit „ist“\nBeispiel\n\npass auf, dass [dir] die Wohnungstür nicht zuschlägt\n\n\n\n\ndurch [Hammer]schläge [mit Nägeln o.\xa0Ä.] fest zumachen, verschließen\nGebrauch\nselten\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\neine Kiste zuschlagen\n\n\n\ndurch Schlagen, Hämmern in eine bestimmte Form bringen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nSteine für eine Mauer [passend] zuschlagen\n\n\n\nmit einem Schläger zuspielen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\ndem Partner den Ball zuschlagen\n\n\n\n\neinen Schlag (1a), mehrere Schläge gegen jemanden führen\nGrammatik\nPerfektbildung mit „hat“\nBeispiele\n\nkräftig, hart, mit der Faust zuschlagen\nder Täter holte aus und schlug zu\n〈in übertragener Bedeutung:〉 die Polizei schlug zu\n〈in übertragener Bedeutung:〉 das Schicksal, der Tod schlug zu\n\n\n\netwas Bestimmtes tun (besonders etwas, was jemand gewohnheitsmäßig tut, was typisch für ihn ist [und was allgemein gefürchtet ist, nicht gutgeheißen wird])\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nder Mörder hat wieder zugeschlagen\n\n\n\nsich beim Essen, Trinken keinerlei Zurückhaltung auferlegen\nGebrauch\numgangssprachlich\nGrammatik\nPerfektbildung mit „hat“\nBeispiele\n\nnach der Diät wieder [richtig, voll] zuschlagen können\nbeim Champagner haben sie ganz schön zugeschlagen\n〈in übertragener Bedeutung:〉 (umgangssprachlich) die Stadt will jetzt bei den Parkgebühren zuschlagen (will sie kräftig erhöhen)\n\n\n\nein Angebot, eine gute Gelegenheit o.\xa0Ä. wahrnehmen, einen Vorteil nutzen\nGebrauch\numgangssprachlich\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nbei diesem günstigen Angebot musste ich einfach zuschlagen\n\n\n\n\n\n(bei einer Versteigerung) durch Hammerschlag als Eigentum zuerkennen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\ndas Buch wurde [einer Schweizer Bieterin] mit fünftausend Euro zugeschlagen\n\n\n\nim Rahmen einer Ausschreibung (als Auftrag) erteilen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\nder Auftrag, der Neubau wurde einer belgischen Firma zugeschlagen\n\n\n\nals weiteren Bestandteil hinzufügen, angliedern o.\xa0Ä.\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\ndas Haus wurde dem Erbe des Sohnes zugeschlagen\n\n\n\n\n(einen Betrag o.\xa0Ä.) auf etwas aufschlagen\nGrammatik\nPerfektbildung mit „hat“\nBeispiel\n\n[zu] dem/auf den Preis werden noch 10\u2004% zugeschlagen\n\n\n\neinen bestimmten Stoff bei der Herstellung von Mörtel und Beton oder bei der Verhüttung von Erzen zusetzen\nGebrauch\nBautechnik, Hüttenwesen\nGrammatik\nPerfektbildung mit „hat“\n\n\n', 'origin': None, 'compounds': {'adjektive': ['blitzschnell', 'eiskalt', 'erbarmungslos', 'erneut', 'gleich', 'gnadenlos', 'hart', 'richtig'], 'substantive': ['Autotür', 'Mal', 'Mörder', 'Nase', 'Schicksal', 'Transfermarkt', 'Tür', 'Wagentür']}, 'grammar_raw': None, 'synonyms': ['schließen, zuklappen, zuschmettern, zuwerfen'], 'words_before': ['zuschicken', 'zuschieben', 'zuschießen', 'zuschippen', 'Zuschlag'], 'words_after': ['zuschlagfrei', 'Zuschlagkalkulation', 'Zuschlagkarte', 'zuschlagpflichtig', 'Zuschlagsatz']}
    parse_duden_context(context)
