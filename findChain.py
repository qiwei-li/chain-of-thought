
def findId(title):
    import requests
    from bs4 import BeautifulSoup

    pre_url = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?querytext='
    mid_url = '%20'.join(title.split())
    url = pre_url + mid_url

    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    return url

tmp = findId('Gradient-based learning applied to document recognition')
print tmp

#//*[@id="LayoutWrapper"]/div[7]/div[3]/main/section[3]/div/div/div[1]/xpl-result/div/div[1]/h2/a