import json
from sys import getsizeof

example_dict = {'id': 1, 'session_id': 2, 'unit': 'army', 'coord_from': [1, 1], 'coord_to': [10, 10]}

class MyProtocol:
	__size: int = 0
	__data: dict

	__coding: str = 'utf-8'

	__bytes_start: bytes = b'START'
	__bytes_end: bytes = b'END'
	__bytes_sep: bytes = b':'

	def __init__(self, data: dict):
		self.__data = data
		self.__size = getsizeof(data)

	def __str__(self):
		return 'Object of class MYProtocol \n' + \
			   'data = ' + str(self.__data) + '\n'

	def getSize(self):
		return self.__size

	def getData(self):
		return self.__data

	@staticmethod
	def getByteStrFromData(data: dict) -> bytes:
		res_str = MyProtocol.__bytes_start + \
				  MyProtocol.__bytes_sep + \
				  json.dumps(data).encode(MyProtocol.__coding) + \
				  MyProtocol.__bytes_sep + \
				  MyProtocol.__bytes_end
		return res_str

	@staticmethod
	def getDataFromByteStr(byte_str: bytes) -> dict:
		if MyProtocol.__bytes_start == byte_str[:len(MyProtocol.__bytes_start)] and \
				MyProtocol.__bytes_end == byte_str[-len(MyProtocol.__bytes_end):]:

			byte_dict = byte_str[len(MyProtocol.__bytes_start) + 1:len(byte_str) - len(MyProtocol.__bytes_end) - 1]
			res = json.loads(byte_dict)

			#print('Получено: ', res)

			return res

		else:
			is_MyProtocol = False

		if not is_MyProtocol:
			print('Unknown protocol')
			return {}
