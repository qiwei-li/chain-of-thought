from lxml import html, etree
import requests
import os
import re



def ieee(artNum):
	usage = {}
	for i in artNum:
		usageI = {}
		site = "http://ieeexplore.ieee.org/xpl/abstractMetrics.jsp?arnumber=" + str(i)

		page = requests.get(site)
		tree = html.fromstring(page.content)

		metrics = tree.xpath('//div[@class = "year-selector"]')[0]
		table = [p.text_content() for p in metrics]
		temp = str(table[0]).translate(None, '\t\n')
		years = [ temp[k:k+4] for k in range(0, len(temp), 4) ]

		for elt in years:
			usageValue =[]
			site = "http://ieeexplore.ieee.org/xpl/biblMetrics.ajax?arnumber=" + str(i) + "&bbyear=" + elt
			page = requests.get(site)
			tree = html.fromstring(page.content)
			metrics = tree.xpath('//div[@class = "metrics-container"]')[0]
			for j in range(0,6):
					usageValue.append(metrics[3][0][1][j].text)
			for j in range(0,6):
					usageValue.append(metrics[3][1][1][j].text)
			usageI[elt] = usageValue
		usage[i] = usageI

	return usage
	
def main():
	artNum = [6740843, 6740844]  # list of article numbers we want to scrape
	Y= ieee(artNum)  			# Y is the dictionary in the 
								#format of {article number:{year:{list of 12 month values in order from Jan to Dec}}}
	
	return

	
	
			
if __name__ == "__main__":
	main()		
