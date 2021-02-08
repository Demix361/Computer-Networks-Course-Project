from __future__ import division, print_function, unicode_literals
from cocos.director import director
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import Sprite
from cocos.scenes import FadeTransition

import socket
from time import sleep

import menu
from protocol import MyProtocol
from game import Level1Scene


class Game:
	def __init__(self):
		director.init(resizable=False, width=800, height=600)
		director.set_depth_test()

		self.hello = 'Hello'
		self.menu_scene = Scene(menu.BGLayer(),
								MultiplexLayer(menu.MainMenu(self), menu.OptionMenu(), menu.WaitLayer(self)))

		self.player_id = None
		self.ready = False
		self.max_players = 2
		self.sock = None

	def start(self):
		director.run(self.menu_scene)

	def connect_to_server(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(('127.0.0.1', 9090))

		mes = {'type': 'connect'}
		mes_bit = MyProtocol.getByteStrFromData(mes)
		self.sock.send(mes_bit)
		data_bit = self.sock.recv(10000)
		data = MyProtocol.getDataFromByteStr(data_bit)
		self.player_id = data['player_id']
		self.ready = True
		print(self.player_id)

		mes = {'type': 'ask', 'question': 'players_connected'}
		mes_bit = MyProtocol.getByteStrFromData(mes)
		self.sock.send(mes_bit)
		data_bit = self.sock.recv(10000)
		data = MyProtocol.getDataFromByteStr(data_bit)

		#if data['players_connected'] == self.max_players:
		#	mes = {'type': 'start'}
		#	mes_bit = MyProtocol.getByteStrFromData(mes)
		#	self.sock.send(mes_bit)

	def wait_server(self):
		mes = {'type': 'ask', 'question': 'game_ready'}
		mes_bit = MyProtocol.getByteStrFromData(mes)
		self.sock.send(mes_bit)
		data_bit = self.sock.recv(10000)
		data = MyProtocol.getDataFromByteStr(data_bit)

		if data['type'] == 'ask' and data['question'] == 'game_ready' and data['answer'] == 'yes':
			director.replace(FadeTransition(Level1Scene(self)))






if __name__ == '__main__':
	g = Game()
	g.start()
