### this takes in data2000.p file after Keyword!!
import pickle
import re
import requests
from bs4 import BeautifulSoup

def basic(inputID):
    authors = []
    base ="http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber="
    url = base + str(inputID)
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    try:
        title = soup.find('div', {'class': 'title'}).text.replace('\n', '').replace('\t', '')
    except:
        title = ''
    try:
        author = soup.find_all('span', {'id': 'preferredName'})
        tmp = []
        for item in author:
            tmp.append(str(item).replace('<span class="','').replace('" id="preferredName"></span>',''))
    except:
        author = ''
    authors.append('; '.join(list(set(tmp))))
    try:
        date = str(soup.find_all('dl')[1]).split('Date')[1].replace('\n','').replace('\t','').split('<dd>')[1].split('</dd>')[0]
    except:
        date = ''
    try:
        punumber = str(soup.find_all('a', {'href': re.compile('punumber')})[1]).split('number=')[1].split('">')[0]
    except:
        punumber = ''

    return {'title':title,
            'authors':authors,
            'date':date,
            'punumber':punumber}


data = pickle.load(open("data_2000.p", 'rb'))

current = 0
for id in data:
    ans = basic(id)
    data[id]['title']=ans['title']
    data[id]['authors']=ans['authors']
    data[id]['date']=ans['date']
    data[id]['punumber']=ans['punumber']
    current += 1
    print(current)

pickle.dump(data, open( "data_2000_with_basic_info.p", "wb"))
"""
all_nodes = []
for key, value in data.iteritems():
    all_nodes.append(str(key))
    for item1 in value['refs']:
        all_nodes.append(str(item1))
    for item2 in value['cites']:
        all_nodes.append(str(item2))

unique_nodes = list(set(all_nodes))
print(len(unique_nodes))
"""