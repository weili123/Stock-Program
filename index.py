from paste import request
import re, sys
sys.path.append('/var/www/stock_program')
import add.add as add

def application(environ, start_response):
	status = '200 OK'
	output = ''
	#get query
	query = re.sub("[^a-z]","",environ.get('PATH_INFO'))
	#get arguments
	arguments = dict(request.parse_querystring(environ))

	#add stock to database
	if query == 'add':
		#file that handles adding stock to database
		output = add.add_stock(arguments)
	
	response_headers = [('Content-Type', 'application/json')]
	start_response(status, response_headers)
	return [output]
