import urllib.request

def request(url):
	response_object = urllib.request.urlopen(url)
	with response_object as response:
		return response.read()
	return None
