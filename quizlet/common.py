def format_english(self, lst):
    tmp = []
    for i in lst:
        clean = clean_unicode(i['en'])
        clean = clean.replace('AE', "")
        clean = clean.replace('BE', "")
        tmp.append(clean.strip())
    str = ' ▪ '.join(tmp)
    return str