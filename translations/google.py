from googletrans import Translator

translator = Translator()

def to_en(term):
    tran = translator.translate(term, src='en', dest='de')
    return tran
