import os
import configuration
from pathlib import Path

#################################
# Paths
#################################

root_dir = configuration.root_dir
terms_file = root_dir + '/data/terms.txt'



html_path = root_dir + '/data/html_files/'
html_dir = 'html_files'
extension = ".html_files"

min_secs = 10
#max_secs = 300
max_secs = 15
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
reverso_base_url = 'https://dictionary.reverso.net/german-english/'

NOUN = 'subst'
VERB = 'verb'
PREP= 'praep'


nl = "\n"
nl2 = "\n\n"
comma = ", "
cards_path = "/home/avare/repos/quizlet/data/quizlet_input/"
postgres_config = os.environ['DATABASE']