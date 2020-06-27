import ssl
import urllib.request
from queue import Queue
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# To write all the content of a set to a file
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")


# To write all the content of a file to a set
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Returns the domain name of a website
def get_domain_name(url, remove_http=True):
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        domain_name = f"{uri.netloc}://{uri.netloc}"
    return domain_name


def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


# To extract all the links from a website
def get_links(link,domain_name,queue,crawl):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = urllib.request.urlopen(link, context=ctx).read()
        soup = BeautifulSoup(url,'html.parser')

        tags = soup('a',href=True)
        for tag in tags:
            href = tag['href']
            if href.startswith('/'):
                href = 'https://' + domain_name + href
            if href.endswith('/'):
                href = href[:-1]
            if get_domain_name(href) == domain_name:
                if href not in queue:
                    if href not in crawl :
                        queue.insert(0,href)
            else:
                continue
    except Exception as e:
        print(str(e))


print("General is Imported\n")
