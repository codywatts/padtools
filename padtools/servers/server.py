import json

from . import extlist
from . import extdllist
from . import http_interface
from .asset import Asset
from .extra import Extra

class Server(object):
	def __init__(self, url):
		self._assets = []
		self._extras = []
		self._url = url
		self._base = None
		self._extlist_data = None
		self._extdllist_data = None
	
	def _fetch_base(self):
		base_binary_data = http_interface.request(self.url)
		self._base = json.loads(base_binary_data.decode(encoding="utf-8"))
		assert self._base["res"] == 0
	
	def _fetch_extlist(self):
		self._extlist_data = self.request_file("extlist.bin")
		self._assets = []
		mons_data, cards_data = extlist.parse(self._extlist_data)
		# Convert to assets:
		for mons in mons_data:
			file_name = "mons_{id_number:0>3}.bc".format(id_number=mons.id_number)
			url = self.extlist_url + "/" + file_name
			mons_asset = Asset(file_name=file_name, url=url, **(mons._asdict()))
			self._assets.append(mons_asset)
		for card in cards_data:
			file_name = "cards_{id_number:0>3}.bc".format(id_number=card.id_number)
			url = self.extlist_url + "/" + file_name
			cards_asset = Asset(file_name=file_name, url=url, **(card._asdict()))
			self._assets.append(cards_asset)
	
	def request_file(self, file_name):
		request_url = self.extlist_url + "/" + file_name
		return bytes(http_interface.request(request_url))

	def _fetch_extdllist(self):
		self._extdllist_data = self.request_extra_file("extdllist.bin")
		self._extras = []
		extra_files = extdllist.parse(self._extdllist_data)
		for file_name in extra_files:
			url = self.efl_url + "/" + file_name
			self._extras.append(Extra(url=url, file_name=file_name))

	def request_extra_file(self, file_name):
		request_url = self.efl_url + "/" + file_name
		return bytes(http_interface.request(request_url))
	
	@property
	def url(self):
		return self._url
	
	@property
	def assets(self):
		if not self._extlist_data:
			self._fetch_extlist()
		return list(self._assets)
	
	@property
	def version(self):
		return self.base["rver"]
	
	@property
	def extlist_url(self):
		return self.base["extlist"]
	
	@property
	def efl_url(self):
		return self.base["efl"]

	@property
	def base(self):
		if not self._base:
			self._fetch_base()
		return self._base

	@property
	def extras(self):
		if not self._extdllist_data:
			self._fetch_extdllist()
		return list(self._extras)
