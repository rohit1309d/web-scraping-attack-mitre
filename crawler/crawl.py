import re
from general import *


f = open('url.txt','r')
line = f.readline()
fline = re.findall(r'\S+',line)
if fline[-1].startswith(':'):
    homepage = fline[-1][1:]
else:
    homepage = fline[-1]

domain_name = get_domain_name(homepage)

queue = list(file_to_set('queue.txt'))
crawl = list(file_to_set('crawl.txt'))

if (len(queue) == 0) and (len(crawl) == 0):
    queue.insert(0,homepage)

while len(queue) > 0:
    link = queue[0]
    print('Working on ', ' url --- ', link)
    if link.endswith('.pdf') or link.endswith('.json') or link.endswith('.png') or link.endswith('.jpg') or link.endswith('.xlsx'):
        queue.remove(link)
        crawl.insert(0,link)
    else:
        get_links(link,domain_name,queue,crawl)
        queue.remove(link)
        crawl.insert(0,link)
    set_to_file(queue, 'queue.txt')
    set_to_file(crawl, 'crawl.txt')
