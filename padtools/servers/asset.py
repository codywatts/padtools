class Asset(object):
	def __init__(self, url=None, file_name=None, id_number=None, uncompressed_size=None, compressed_size=None):
		self._url = url
		self._file_name = file_name
		self._id_number = id_number
		self._uncompressed_size = uncompressed_size
		self._compressed_size = compressed_size
	@property
	def url(self):
		return self._url
	@url.setter
	def url(self, value):
		self._url = value
	@property
	def id_number(self):
		return self._id_number
	@property
	def file_name(self):
		return self._file_name
	@property
	def compressed_size(self):
		return self._compressed_size
	@property
	def uncompressed_size(self):
		return self._uncompressed_size
