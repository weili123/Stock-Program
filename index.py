from paste import request
import re
def application(environ, start_response):
	status = '200 OK'
	path = re.sub("[^a-z]","",environ.get('PATH_INFO'))
	query = dict(request.parse_querystring(environ))
	output = path
	
	response_headers = [('Content-Type', 'application/json')]
	start_response(status, response_headers)
	return [output]
