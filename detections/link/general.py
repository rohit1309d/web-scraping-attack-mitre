import urllib.request
import re

from rake_nltk import Rake
from bs4 import BeautifulSoup


# To convert html content into readable text
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# To remove whitespace
def remove(string):
    return string.replace(" ", "")


# To extract only the techniques links to a set
def file_to_setl(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            if line.__contains__('https://attack.mitre.org/techniques/T'):
                results.add(line.replace('\n', ''))
    return sorted(results)


# To extract detection from a link
def detection(link):
    try:
        url = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(url,'html.parser')
        text = soup.find('h2',id = 'detection')
        if text is None:
            text = soup.find('h2',id = 'detectable')
            if text is not None:
                det = text.next_elements
                eng = str(list(det)[2])
                para = remove_html_tags(eng)
                return para,soup
            else:
                return None,soup
        else:
            det = text.next_elements
            eng = str(list(det)[2])
            para = remove_html_tags(eng)
            return para,soup
    except Exception:
        return None,soup


# To extract all the keywords from a given text
def keywords(text,bad_words):
    words = set()
    r = Rake()
    r.extract_keywords_from_text(text)
    key = dict(r.get_word_degrees())
    for wrd in key:
        if wrd not in bad_words:
            if wrd.isalpha() and len(wrd) > 3:
                words.add(wrd)
    return list(words)


# To extract all the mitigations in a particular link
def mitigations(soup):
    a_tags = soup.select("td > a[href*=mitigations]")
    if a_tags is not None:
        miti = list()
        for lin in list(a_tags):
            miti += list(lin)
        return miti
    else:
        return None


# To convert a list of words to a string
def list_to_str(words):
    str1 = ""
    for ele in words:
        str1 += ele + ' , '

    return str1[:-2]
