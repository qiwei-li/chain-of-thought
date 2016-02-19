import time

def basic(inputIDs):
    import re
    import requests
    from bs4 import BeautifulSoup

    ids = []
    titles = []
    authors = []
    dates = []
    base ="http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber="

    for inputID in inputIDs:
        ids.append(inputID)
        url = base + str(inputID)
        r = requests.get(url)
        soup = BeautifulSoup(r.content)

        try:
            title = soup.find('div', {'class': 'title'}).text.replace('\n', '').replace('\t', '')
        except:
            title = 'NA'
        titles.append(title)

        try:
            author = soup.find_all('span', {'id': 'preferredName'})
            tmp = []
            for item in author:
                tmp.append(str(item).replace('<span class="','').replace('" id="preferredName"></span>',''))
        except:
            author = 'NA'
        authors.append('; '.join(list(set(tmp))))

        try:
            date = str(soup.find_all('dl')[1]).split('Date')[1].replace('\n','').replace('\t','').split('<dd>')[1].split('</dd>')[0]
        except:
            date = 'NA'
        dates.append(date)

    return [ids, titles, authors, dates]


id = range(4492360, 4492370)
start_time = time.time()
ans = basic(id)
end_time = time.time()
print(ans)
print end_time - start_time