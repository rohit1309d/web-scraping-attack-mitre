import urllib.request
import re

from xlsxwriter import Workbook

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


# To convert any file contents to set
def file_to_set(file_name):
    with open(file_name, 'rt') as f:
        st = f.read()
        repl = st.replace(" ", "")
        li = repl.split(',')
        results = set(li)
    return results


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
    for word in key:
        if word not in bad_words:
            if word.isalpha() and len(word) > 3:
                words.add(word)
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


wb = Workbook('data.xlsx')
sheet = wb.add_worksheet()


bad_words = list(file_to_set('bad_words.txt'))
techniques = list(file_to_setl('attack_links.txt'))
row = 1

for link in techniques:
    print("Working on ",link)
    id = link[-5:]
    detcn,soup = detection(link)
    mitigation = mitigations(soup)
    sheet.write(row, 1, id)
    sheet.write(row, 2, link)
    if detcn is not None:
        k = keywords(detcn,bad_words)
        print(k)
        sheet.write(row, 3, detcn)
        sheet.write(row, 4,list_to_str(k))
        sheet.write(row, 5, list_to_str(mitigation))
    row += 1
wb.close()