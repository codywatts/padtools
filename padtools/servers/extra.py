class Extra(object):
	def __init__(self, url=None, file_name=None):
		self._url = url
		self._file_name = file_name
	@property
	def url(self):
		return self._url
	@property
	def file_name(self):
		return self._file_name
