import MySQLdb as mysqldb
import json

#handles adding stocks to the database
def add_stock(query):
	symbol = query.get('symbol')
	industry = query.get('industry')
	conn = mysqldb.connect(db='stock', user='root', passwd='password', host='localhost')
	c = conn.cursor()
	data = {}
	data['success'] = True
	return json.dumps(data)
