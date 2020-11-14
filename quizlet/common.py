from leo.leo import clean_unicode

def format_english(lst):
    tmp = []
    for i in lst:
        clean = clean_unicode(i['en'])
        clean = clean.replace('AE', "")
        clean = clean.replace('BE', "")
        tmp.append(clean.strip())
    str = ' ▪ '.join(tmp)
    return str

def remove_dangling_letter(str):
    clean = str.replace("AE", "")
    clean = clean.replace("BE", "")
    return clean

def terms_from_list():
    pass
