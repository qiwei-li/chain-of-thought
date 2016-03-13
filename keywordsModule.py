import urllib
from bs4 import BeautifulSoup as bs
import pickle

def index_term(ID):
    pre_url = 'http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber='
    url = pre_url+str(ID)
    url_html = urllib.urlopen(url).read()
    soup = bs(url_html,"html.parser")
    control_index = []
    non_control_index = []
    author_keywords = []
    ieee_terms = []
    for link in soup.find_all('h2'):
        if (link.get_text() == 'IEEE TERMS'):
            ul = link.next_sibling.next_sibling
            data = str(ul.get_text()).strip().split("\n")
            ieee_terms = data
    return ieee_terms
