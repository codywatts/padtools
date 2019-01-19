import os
import json
import collections

from .region import Region

class RegionsMetaClass(type, collections.Set):
	_regions = []
	def __iter__(cls):
		return iter(cls._regions)
	def __contains__(cls, value):
		return value in cls._regions
	def __len__(cls):
		return len(cls._regions)
	def load(cls, file_name):
		with open(file_name, "r") as regions_data_file:
			regions_data_as_json = json.load(regions_data_file)
		for region_identifier in regions_data_as_json:
			region_data = regions_data_as_json[region_identifier]
			new_region = Region(region_data["name"])
			cls._regions.append(new_region)
			setattr(cls, region_identifier, new_region)

class Regions(object, metaclass=RegionsMetaClass):
	pass

Regions.load(os.path.join(os.path.dirname(__file__), "data", "regions.json"))
