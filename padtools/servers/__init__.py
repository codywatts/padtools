import os
import json

from .server import Server
from .. import regions

class ServersMetaClass(type):
	def __getitem__(cls, region):
		return region.server
	def load(cls, file_name):
		with open(file_name, "r") as servers_data_file:
			servers_data_as_json = json.loads(servers_data_file.read())
			for server in servers_data_as_json:
				# For now I'm arbitrarily choosing the use the iOS url over the Android url.
				new_server = Server(server["ios_url"])
				for region_identifier in server["regions"]:
					region = getattr(regions, region_identifier)
					region.server = new_server

class Servers(object, metaclass=ServersMetaClass):
	pass

Servers.load(os.path.join(__file__, "..", "data", "servers.json"))
