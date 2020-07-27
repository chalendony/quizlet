## https://dictionary.reverso.net/german-english/besuchen


import requests
from bs4 import BeautifulSoup
import constants as const

import configuration
from random import randint
from time import sleep

#TODO merge this code into parse reverso context

#TODO rename so we know its context and not dictionary

class ReversoDictionary:

    def download_pages(self):
        """
        Download a page and save to local directory
        :param term:
        :return:
        """
        print(f"project root: {configuration.root_dir}" )

        lines = []

        # read input, skip empty lines
        with open(const.terms_file) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
        lines = self.remove_dash(lines)

        for term in lines:
            print(term)
            url = f"{const.reverso_context_url}{term}"
            html = self.download(url)
            try:
                with open(f"{const.html_path}{term}.html", "wb") as file:
                    file.write(html)
            except Exception as e:
                print("Exception: skipping " + term)
            time = randint(const.min_secs, const.max_secs)
            print(time)
            sleep(time)

    def remove_dash(self,lines):
        lst = []
        for l in lines:
            l = l.strip()
            idx = l.find("-")
            if idx != -1: ## TODO: or starts with comment ignore
                found = l.split('-')[0].strip()
                lst.append(found)
            else:
                lst.append(l)
        return lst


    def download(self, url):
        try:
            response = requests.get(url, headers=const.headers) #  send request
            if response.status_code == 200:
                #print(response.status_code, 'OK')
                pass
        except requests.exceptions.ConnectionError:
            print('Something wrong ')
            return False
        soup = BeautifulSoup(response.text, "lxml")  #  parse web page
        html = soup.prettify("utf-8")
        return html


def translate_word():
    '''
    This bot about parsing and translating. You can use command line arguments. To do this run:
    python3 "your_file_name" "your_language_name" "language_you_want_to_translate_on (or "all")" "word"
    Example:  python3 ./reverso/context_1.py  german english besuchen


    '''
    #  init variables:

    languages_list = ['german']




    translation_text = ''
    for lang in languages_list:
        #  create request:
        #URL = f'https://context.reverso.net/translation/{default_lang}-{lang}/' + word.replace(" ", "+").lower().replace("'", "%27")

        URL = 'https://dictionary.reverso.net/german-english/besuchen'
        URL = 'https://dictionary.reverso.net/german-english/Buchdeckel'
        #URL = 'https://dictionary.reverso.net/german-definition/besuchen'
        #print(f'URL = {URL}')  #  if URL is correct, we will see it


        try:
            response = requests.get(URL, headers=headers) #  send request
            if response.status_code == 200:
                #print(response.status_code, 'OK')
                pass

        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
            return False
        soup = BeautifulSoup(response.text, "html_files.parser")  #  parse web page

        print(soup.text)
        html = soup.prettify("utf-8")
        with open("/home/avare/repos/quizlet_input/data/html_files/translation/Buchdeckel.html_files", "wb") as file:
            file.write(html)


if __name__ == "__main__":
    rev = ReversoDictionary()
    rev.download_pages()
