from linguee.linguee import Page

filename = '/home/avare/repos/linguee/linguee/test/data/Ernaehrung.html'
term = 'Ern%C3%A4hrung'

def test_empty_page():
    filename = '/home/avare/repos/linguee/linguee/test/data/no_content.html'
    target = 'No results for'
    page = Page()
    result = page.load(filename)
    flag = page.is_empty(result)
    assert flag == True

def test_notempty_page():
    target = 'No results for'
    page = Page()
    result = page.load(filename)
    flag = page.is_empty(result)
    assert flag == False

def getpage():
    selector = 'head > meta:nth-child(2)'
    term = "Ernährung"
    page = Page()
    result = page.get(term)
    res = result.html.find(selector)
    assert "Ernährung" in str(res[0].attrs.get('content'))


def test_load_page():
    selector = 'head > meta:nth-child(2)'
    page = Page()
    result = page.load(filename)
    res = result.find(selector)
    assert "Ernährung" in res[0].attrs.get('content')


def test_single_line():
    page = Page()
    result = page.load(filename)
    lst = page.single_lines(result)
    print(lst)
    assert "Ernährung" in lst[0].get('definition')

def test_sentence():
    page = Page()
    result = page.load(filename)
    pairs = page.sentence(result)
    lines = len(pairs)
    assert lines == 4

def test_format():
    page = Page()
    result = page.load(filename)

    sent = page.sentence(result)
    terms = page.single_lines(result)
    sent.extend(terms)
    print(len(sent))
