import time
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
        s = str(soup.find_all('dl')).replace("\\n","").replace("\\t","")
        d4 = re.findall(r"\D(\d{4})\D", s)
        ll = []
        for item in d4:
            if(int(item) > 1900 and int(item) <= 2016):
                ll.append(item)
        date = min(ll)
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


"""
id = 4492360
ans = basic(id)
print(ans)
"""
