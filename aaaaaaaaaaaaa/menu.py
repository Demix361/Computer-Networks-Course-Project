from pyglet.gl import *
from cocos.menu import *
from cocos.layer import *
from cocos.sprite import Sprite


class BGLayer(Layer):
	def __init__(self):
		super(BGLayer, self).__init__()

		bg = Sprite('images/menu/background.png')
		bg.position = (400, 300)
		self.add(bg)


class WaitLayer(Layer):
	def __init__(self, game_controller):
		super(WaitLayer, self).__init__()
		self.game_controller = game_controller

		bg = Sprite('images/menu/wait_screen.png')
		bg.position = (400, 300)

		#player = Sprite(f"images/king_right/1/Fall.png")
		#player.position = (400, 300)

		self.add(bg)
		#self.add(player)

		self.schedule(self.update)

	def update(self, dt):
		self.game_controller.wait_server()


class MainMenu(Menu):
	def __init__(self, game_controller):
		super(MainMenu, self).__init__()
		pyglet.font.add_directory('.')

		self.font_title['font_size'] = 50
		self.font_item['font_size'] = 30
		self.font_item_selected['font_size'] = 30

		self.menu_valign = CENTER
		self.menu_halign = CENTER

		items = []
		items.append(MenuItem('Новая игра', self.on_new_game))
		items.append(MenuItem('Управление', self.on_scores))
		items.append(MenuItem('Настройки', self.on_options))
		items.append(MenuItem('Выход', self.on_quit))

		self.create_menu(items, zoom_in(), zoom_out())
		self.game_controller = game_controller

	# TODO: fix freeze on pressing
	def on_new_game(self):
		self.game_controller.connect_to_server()
		self.parent.switch_to(2)
		#self.game_controller.wait_server()
		#self.game_controller.sig_wait_server.sig.emit()

	def on_scores(self):
		print("on_old_game()")

	def on_options(self):
		self.parent.switch_to(1)

	def on_quit(self):
		director.pop()


class OptionMenu(Menu):
	def __init__(self):
		super(OptionMenu, self).__init__("A Heart of Tar'Karas")

		self.font_title['font_size'] = 40

		self.menu_valign = BOTTOM
		self.menu_halign = RIGHT

		items = []
		items.append(MenuItem('Fullscreen', self.on_fullscreen))
		items.append(ToggleMenuItem('Show FPS: ', self.on_show_fps, False))
		items.append(MenuItem('OK', self.on_quit))
		self.create_menu(items, shake(), shake_back())

	def on_fullscreen(self):
		director.window.set_fullscreen(not director.window.fullscreen)

	def on_quit(self):
		self.parent.switch_to(0)

	def on_show_fps(self, value):
		director.show_FPS = value
