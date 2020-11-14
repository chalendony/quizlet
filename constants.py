import os
import configuration
from pathlib import Path


################################
# Linguee
################################

lingue_base_url = 'https://www.linguee.com/german-english/translation/'
lingue_urlfile = '/home/avare/repos/quizlet/data/urls.txt'
lingue_termfile = '/home/avare/repos/quizlet/data/terms_2020-06-13 00:44:33.txt'
dwds_base_url = "https://www.dwds.de/wb/"

#################################
# Paths
#################################

root_dir = configuration.root_dir
terms_file = root_dir + '/data/terms.txt'
html_path = root_dir + '/data/html_files/'
html_dir = 'html_files'
extension = ".html_files"
cards_path = "/home/avare/repos/quizlet/data/quizlet_input/"

WORD_SENSE=1
min_secs = 1 # 60, 300 all day
max_secs = 5
max_card_entries = 7

# html
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
reverso_base_url = 'https://dictionary.reverso.net/german-english/'
reverso_context_url = "https://context.reverso.net/translation/german-english/"
CROSSWORD = "crossword"
# defining structure of each quizlet set
SUBS = 'Substantiv'
VERB = 'Verb'
KONJ = "Konjunktion"
PADJ = "partizipiales Adjektiv"
ADJ = "Adjektiv"
ADV = "Adverb"
PADV = "partizipiales Adverb"
INDPRON = "Indefinitpronomen"
### all dwds word arten
# "Adjektiv
# Adverb
# Affix
# Ausruf
# Bruchzahl
# Demonstrativpronomen
# Eigenname
# Imperativ
# Indefinitpronomen
# Interrogativpronomen
# Kardinalzahl
# Komparativ
# Konjunktion
# Mehrwortausdruck
# Ordinalzahl
# Personalpronomen
# Possessivpronomen
# Pronomen
# Pronominaladverb
# Präposition
# Reflexivpronomen
# Relativpronomen
# Substantiv
# Superlativ
# Verb
# bestimmter Artikel
# partizipiales Adjektiv
# partizipiales Adverb
# reziprokes Pronomen"
PREP= 'praep'
EXAMPLE = 'example'
REVERSO = 'reverso'
DEFINTION = 'definition'
ADJADV = 'adjadv'
PHRASE = 'phrase'
DWDS = 'dwds'

MAX_CARDS = 50
MAX_EXAMPLES = 5
MAX_CROSSWORD = 50

# formating quizlet
nl = "\n"
nl2 = "\n\n"
comma = ", "
aline = "\n----------------\n" ## move to const

postgres_config = os.environ['DATABASE']
dlapikey = os.getenv('DLAPIKEY')
from_language = 'DE'
to_language = 'EN'



