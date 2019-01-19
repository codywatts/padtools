from collections import namedtuple
import struct

def structured_data(class_name, data_members):
	attributes = [attribute_name for attribute_name, struct_format in data_members if attribute_name != None]
	format_string = ''.join([struct_format for attribute_name, struct_format in data_members])
	class StructuredData(namedtuple(class_name, attributes)):
		format = format_string
		size = struct.calcsize(format_string)
		@classmethod
		def unpack_from(cls, buffer, offset=0):
			return cls._make(struct.unpack_from(cls.format, buffer, offset))
	return StructuredData

class Header(structured_data("Header", [("magic_string", "4s"), ("entry_count", "I"), (None, "4x"), (None, "4x")])):
	pass

class ExtraFileRecord(structured_data("ExtraFileRecord", [(None, "4x"), ("last_update", "I"), (None, "4x"), ("offset", "I")])):
	pass

def parse(extlist_data):
	extlist_data = bytearray(extlist_data)
	starting_size = len(extlist_data)
	def read_structured_data(buffer, structured_data_type, number_of_items=1):
		output = [structured_data_type.unpack_from(buffer, i * structured_data_type.size) for i in range(number_of_items)]
		buffer[:] = buffer[(structured_data_type.size * number_of_items):]
		return output[0] if number_of_items == 1 else output
	
	header = read_structured_data(extlist_data, Header)
	assert header.magic_string == b"EXF2"

	extra_files_data = read_structured_data(extlist_data, ExtraFileRecord, header.entry_count)
	
	extras = []
	for efd in extra_files_data:
		x = efd.offset - starting_size
		s = ''
		while extlist_data[x] != 0:
			s += chr(extlist_data[x])
			x += 1
		extras.append(s)

	return extras
