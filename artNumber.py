from googlesearch import GoogleSearch


def Search(paper):

	gs = GoogleSearch(paper + " ieeexplore.ieee.org")
	url = gs.top_urls()[0]
	artNumber = [word for word in url.split("=")][-1]
	
	return artNumber