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

class Header(structured_data("Header", [("mons_count", "I"), ("cards_count", "I"), ("magic_string", "4s"), (None, "4x")])):
	pass

class UncompressedMonsterRecord(structured_data("UncompressedMonsterRecord", [("id_number", "H"), (None, "4x"), (None, "4x"), (None, "4x"), (None, "2x"), ("uncompressed_size", "I"), (None, "4x")])):
	pass

class UncompressedCardRecord(structured_data("UncompressedCardRecord", [("id_number", "B"), (None, "x"), (None, "4x"), (None, "4x"), (None, "4x"), (None, "2x"), ("uncompressed_size", "I"), (None, "4x")])):
	pass

class CompressedAssetRecord(structured_data("CompressedAssetRecord", [("compressed_size", "I"), (None, "4x")])):
	pass

class UnifiedAssetRecord(namedtuple("UnifiedAssetRecord", UncompressedMonsterRecord._fields + CompressedAssetRecord._fields)):
	pass

def parse(extlist_data):
	extlist_data = bytearray(extlist_data)
	def read_structured_data(buffer, structured_data_type, number_of_items=1):
		output = [structured_data_type.unpack_from(buffer, i * structured_data_type.size) for i in range(number_of_items)]
		buffer[:] = buffer[(structured_data_type.size * number_of_items):]
		return output[0] if number_of_items == 1 else output
	
	header = read_structured_data(extlist_data, Header)
	assert header.magic_string == b"EXT1"
	
	uncompressed_mons_data = read_structured_data(extlist_data, UncompressedMonsterRecord, header.mons_count)
	uncompressed_cards_data = read_structured_data(extlist_data, UncompressedCardRecord, header.cards_count)
	compressed_mons_data = read_structured_data(extlist_data, CompressedAssetRecord, header.mons_count)
	compressed_cards_data = read_structured_data(extlist_data, CompressedAssetRecord, header.cards_count)
	
	# Unify the compressed and uncompressed data:
	mons_data = [UnifiedAssetRecord._make(uncompressed + compressed) for uncompressed, compressed in zip(uncompressed_mons_data, compressed_mons_data)]
	cards_data = [UnifiedAssetRecord._make(uncompressed + compressed) for uncompressed, compressed in zip(uncompressed_cards_data, compressed_cards_data)]
	
	# Remove empty entries:
	mons_data = [mons for mons in mons_data if mons.id_number != 0]
	cards_data = [card for card in cards_data if card.id_number != 0]
	
	return mons_data, cards_data
