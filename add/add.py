import MySQLdb as mysqldb
import json, urllib2, re
from bs4 import BeautifulSoup

#handles adding stocks to the database
def add_stock(query):
	#get symbol and industry from query
	symbol = query.get('symbol')
	industry = query.get('industry')
	
	#crawl to find company from symbol using beautifulsoup
	soup = get_soup("q", symbol)

	#return 404 if soup == none
	if soup == None:
		return create_json_error('404 NOT FOUND', 'cannot find symbol: ' + symbol)
	name = get_name(soup)
	if name == None:
		return create_json_error('404 NOT FOUND', 'cannot find symbol: ' + symbol)
	
	#get website
	profile_soup = get_soup("q/pr",symbol)
	website = get_website(profile_soup)
	
	conn = mysqldb.connect(db='stock', user='root', passwd='password', host='localhost')
	c = conn.cursor()
	data = {}
	data['status'] = True
	data['name'] = str(name)
	data['website'] = str(website)
	return json.dumps(data)

def get_soup(page, symbol):
	#crawl yahoo finance for symbol
	url = "http://finance.yahoo.com/" + page + "?s=" + symbol
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html,'html.parser')
	return soup

def get_name(soup):
	#get company name, if none then cannot find company
	name = soup.find("div", {"class":"title"})
	if name == None:
		return None
	#get to correct descendent
	name = name.find("h2").get_text()

	#remove symbol from name
	name = re.sub('\(\w*\)', '', name)[:-1]
	return name

def get_website(soup):
	#get company website, cannot fail as all public companies have websites
	website = soup.find("td", {"class":"yfnc_modtitlew1"}).findAll("a", href=True)[1]
	return website.get_text()


def create_json_error(status,reason):
	data = {}
	data['status'] = status
	data['reason'] = reason
	return json.dumps(data)
