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

        title = soup.find('div', {'class': 'title'}).text.replace('\n', '').replace('\t', '')
        titles.append(title)

        author = soup.find_all('span', {'id': 'preferredName'})
        tmp = []
        for item in author:
            tmp.append(str(item).replace('<span class="','').replace('" id="preferredName"></span>',''))
        authors.append('; '.join(list(set(tmp))))

        dates.append(str(soup.find_all('dl')[1]).split('Date')[1].replace('\n','').replace('\t','').split('<dd>')[1].split('</dd>')[0])

    return [ids, titles, authors, dates]


id = [4492360, 4492364]
ans = basic(id)
print(ans)