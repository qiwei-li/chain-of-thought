import urllib.request
from bs4 import BeautifulSoup as bs
import pickle

data = pickle.load(open("data_2000.p", 'rb'))
print(data)
print(data[7324672])

def index_term(ID):
    pre_url = 'http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber='
    url = pre_url+str(ID)
    url_html = urllib.request.urlopen(url).read()
    soup = bs(url_html,"html.parser")
    control_index = []
    non_control_index = []
    author_keywords = []
    ieee_terms = []
    for link in soup.find_all('h2'):
        if (link.get_text() == 'INSPEC: CONTROLLED INDEXING'):
            ul = link.next_sibling.next_sibling
            data = ul.get_text().strip().split("\n")
            control_index = data
        if (link.get_text() == 'INSPEC: NON CONTROLLED INDEXING'):
            ul = link.next_sibling.next_sibling
            data = ul.get_text().strip().split("\n")
            non_control_index = data
        if (link.get_text() == 'AUTHOR KEYWORDS'):
            ul = link.next_sibling.next_sibling
            data = ul.get_text().strip().split("\n")
            author_keywords = data
        if (link.get_text() == 'IEEE TERMS'):
            ul = link.next_sibling.next_sibling
            data = ul.get_text().strip().split("\n")
            ieee_terms = data
            return control_index, non_control_index,author_keywords,ieee_terms
#print(index_term(7303952))

num = 0
for article in data:
    print("%dth article %s is being processed...."%(num,article))
    data[article]['keywords']=index_term(article)
    print(data[article])
    num += 1

pickle.dump( data, open( "data_2000_withkeywords.p", "wb" ) )



