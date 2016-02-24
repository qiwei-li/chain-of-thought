import requests
import re
import lxml
from lxml import html
from lxml import etree


def getArnumber(href):
        pattern = r"arnumber=\d*"
        match = re.search(pattern, href)
        if match:
                arnumber = match.group()[len("arnumber="):]
                arnumber = int(arnumber)
                return arnumber
        return None


def extractLine(line):
        links = line.find("div")
        if links != None:
                abstract = links.find("a")
                if abstract != None and abstract.text == "Abstract":
                        href = abstract.get("href")
                        return getArnumber(href)
        return None


""" References """
def getRefs(arnumber):
	site = "http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber={0}".format(arnumber)
	page = requests.get(site)
	#print page.content
	try:
		tree = html.fromstring(page.content)
	except lxml.etree.ParseError:
		print "error: lxml.etree.ParseError"
		return []

	count = 0
	result = []
	refs = tree.xpath('//ol[@class = "docs"]')
	if len(refs) > 0:
		for ref in refs[0]:
			count += 1
			refNum = extractLine(ref)
			if refNum != None:
				result.append(refNum)	
	print "Number of references: ", count
	return result


""" Extended Version of Cited By """
def getCites(arnumber):
	site = "http://ieeexplore.ieee.org/xpl/abstractCitationsIeee.ajax?arnumber={0}".format(arnumber) 
	page = requests.get(site)
	#print page.content
	try:
		tree = html.fromstring(page.content)
	except lxml.etree.ParserError:
		print "error: lxml.etree.ParseError" 
		return []

	count = 0
	result = []
	for cite in tree.findall('li'):
		count += 1
		citeNum = extractLine(cite)
		if citeNum != None:
			result.append(citeNum)
	print "Number of cites: ", count
 	return result


""" Similar Articles """
def getSimls(arnumber):
	site = "http://ieeexplore.ieee.org/xpl/abstractSimilar.jsp?arnumber={0}".format(arnumber) 
	page = requests.get(site)
	try:
		tree = html.fromstring(page.content)
	except lxml.etree.ParserError:
		print "error: lxml.etree.ParseError"
		return []
	
	count = 0
	result = []
	pattern = r"arnumber=\d*"
	similars = tree.xpath('//ul[@class = "docs"]')
	if len(similars) > 0:
		for line in similars[0]:
			paper = line.find('h3/a')
			if paper != None and ('href' in paper.keys()):
				href = paper.get('href')
				simlNum = getArnumber(href)
				if simlNum != None:
					result.append(simlNum)
				count += 1
	print "Number of similars: ", count
	return result

		
def main():
	#arnumber = 4492369
	arnumber = 6995590
	getRefs(arnumber)
	getCites(arnumber)
	getSimls(arnumber)


if __name__ == "__main__":
	main()
