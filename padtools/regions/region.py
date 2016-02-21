class Region(object):
	def __init__(self, name):
		self._name = name
		self._server = None
	@property
	def name(self):
		return self._name
	@property
	def server(self):
		return self._server
	@server.setter
	def server(self, value):
		self._server = value
	def __str__(self):
		return self.name
