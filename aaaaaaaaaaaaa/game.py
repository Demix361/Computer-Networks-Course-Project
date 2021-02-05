from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.mapcolliders import RectMapCollider
from cocos.layer import ScrollingManager, ScrollableLayer, ColorLayer, Layer
from cocos.director import director
from cocos.scene import Scene
from cocos.actions import Action, MoveBy, Move, Repeat, Reverse
from pyglet.window import key
import pyglet
from time import time
import cocos.collision_model as cm
import cocos.euclid as eu
import cocos
from cocos.text import Label

from protocol import MyProtocol


class Swin(Sprite):
	def __init__(self, enemy_id, position):
		super().__init__("images/swin_right/Fall.png")
		self.position = position
		self.enemy_id = enemy_id
		self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 2, self.height / 2)
		self.alive = True
		self.state = 'passive'
		self.right = True
		self.activity = 'idle'

	def idle_right_animation(self):
		img = pyglet.image.load('images/swin_right/Idle.png')
		img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=80, item_height=56)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
		self.image = anim

	def idle_left_animation(self):
		img = pyglet.image.load('images/swin_left/Run.png')
		img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=80, item_height=56)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
		self.image = anim

	def run_right_animation(self):
		img = pyglet.image.load('images/swin_right/Run.png')
		img_grid = pyglet.image.ImageGrid(img, 1, 7, item_width=80, item_height=56)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
		self.image = anim

	def run_left_animation(self):
		img = pyglet.image.load('images/swin_left/Idle.png')
		img_grid = pyglet.image.ImageGrid(img, 1, 7, item_width=80, item_height=56)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
		self.image = anim

	def attack_right_animation(self):
		img = pyglet.image.load('images/swin_right/Attack.png')
		img_grid = pyglet.image.ImageGrid(img, 1, 5, item_width=80, item_height=56)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
		self.image = anim

	def attack_left_animation(self):
		img = pyglet.image.load('images/swin_left/Attack.png')
		img_grid = pyglet.image.ImageGrid(img, 1, 5, item_width=80, item_height=56)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
		self.image = anim


class SwinAction(Action, RectMapCollider):
	def start(self):
		self.target.velocity = 0, 0
		self.not_moving = False
		self.speed = 0
		self.stop = True
		self.stop_time = 0
		self.is_jump = False
		self.allow_jump = True

		self.gravity_speed = 18000

	def on_bump_handler(self, vx, vy):
		return (vx, vy)

	def step(self, dt):
		dx = self.target.velocity[0]
		dy = self.target.velocity[1]
		dx = self.speed * dt

		# ИИ






		# "Гравитация"
		dy -= self.gravity_speed * dt

		# Столкновение с картой
		last_rect = self.target.get_rect()
		last_rect.size = (32, 38)
		last_rect.position = (last_rect.position[0] + 24, last_rect.position[1])
		new_rect = last_rect.copy()
		new_rect.x += dx
		new_rect.y += dy * dt

		self.target.velocity = self.collide_map(map_layer, last_rect, new_rect, dy, dx)
		self.on_ground = bool(new_rect.y == last_rect.y)
		# center of sprite (80x56) -> bottom left of rect (32x38) with offset: 24 to right, 0 to up
		self.target.position = (new_rect.position[0] + 16, new_rect.position[1] + 28)


class OnlinePlayer(Sprite):
	def __init__(self, player_id):
		super().__init__(f"images/king_right/{(player_id - 1) % 2 + 1}/Fall.png")
		self.player_id = player_id
		self.image_id = (self.player_id - 1) % 2 + 1
		self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 2, self.height / 2)

	def idle_right_animation(self):
		img = pyglet.image.load(f"images/king_right/{self.image_id}/Idle.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim

	def idle_left_animation(self):
		img = pyglet.image.load(f"images/king_left/{self.image_id}/Idle.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim

	def run_right_animation(self):
		img = pyglet.image.load(f"images/king_right/{self.image_id}/Run.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim

	def run_left_animation(self):
		img = pyglet.image.load(f"images/king_left/{self.image_id}/Run.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim

	def attack_right_animation(self):
		img = pyglet.image.load(f"images/king_right/{self.image_id}/Attack.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
		self.image = anim

	def attack_left_animation(self):
		img = pyglet.image.load(f"images/king_left/{self.image_id}/Attack.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
		self.image = anim


class OnlinePlayerAction(Action):
	def step(self, dt):
		self.target.position = 1


class Player(Sprite):
	def __init__(self, player_id):
		super().__init__(f"images/king_right/{(player_id - 1) % 2 + 1}/Fall.png")
		self.position = 500, 500
		self.player_id = player_id
		self.image_id = (self.player_id - 1) % 2 + 1
		self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 2, self.height / 2) # / (2*3.35417)

		self.anim_list = []
		self.idle_right_animation()

		self.damage = 20
		self.hp = 200
		self.hit_count = 0
		self.right = True
		self.velocity = (0, 0)
		self.on_ground = True

		self.do(PlayerAction())

	def idle_right_animation(self):
		img = pyglet.image.load(f"images/king_right/{self.image_id}/Idle.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim
		self.anim_list.append('idle_r')

	def idle_left_animation(self):
		img = pyglet.image.load(f"images/king_left/{self.image_id}/Idle.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim
		self.anim_list.append('idle_l')

	def run_right_animation(self):
		img = pyglet.image.load(f"images/king_right/{self.image_id}/Run.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim
		self.anim_list.append('run_r')

	def run_left_animation(self):
		img = pyglet.image.load(f"images/king_left/{self.image_id}/Run.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
		self.image = anim
		self.anim_list.append('run_l')

	def attack_right_animation(self):
		img = pyglet.image.load(f"images/king_right/{self.image_id}/Attack.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
		self.image = anim
		self.anim_list.append('attack_r')

	def attack_left_animation(self):
		img = pyglet.image.load(f"images/king_left/{self.image_id}/Attack.png")
		img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
		anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
		self.image = anim
		self.anim_list.append('attack_l')


class PlayerAction(Action, RectMapCollider):
	def start(self):
		self.target.velocity = 0, 0

		self.turn_left = 0
		self.turn_right = 0
		self.right = True

		self.idle_right = 0
		self.idle_left = 0

		self.on_ground = True
		self.is_jump = False
		self.allow_jump = True
		self.space_key = 0
		self.jump_frames = 60
		self.cur_jump_frame = 0
		self.jump_speed = 50000
		self.frame_delta_jump = self.jump_speed / self.jump_frames
		self.jump_animation = 0
		self.fall_animation = 0

		self.alt_key = 0
		self.attack_cd = 0.5
		self.last_attack_time = 0
		self.attack_duration = 0.25
		self.attack_in_progress = False

		self.gravity_speed = 18000

	def on_bump_handler(self, vx, vy):
		return (vx, vy)

	def step(self, dt):
		dx = self.target.velocity[0]
		dy = self.target.velocity[1]

		if self.target.position[0] < -1000 or self.target.position[1] < -1000:
			self.target.position = 500, 500

		# Анимация покоя
		if self.right and self.turn_right == 0:
			self.idle_right += 1
		elif not self.right and self.turn_left == 0:
			self.idle_left += 1
		if self.idle_right == 1:
			self.target.idle_right_animation()
		elif self.idle_left == 1:
			self.target.idle_left_animation()

		# Движение влево/впарво
		dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 300 * dt
		if keyboard[key.RIGHT]:
			self.turn_right += 1
			self.turn_left = 0
			self.idle_right = 0
			self.idle_left = 0
		else:
			self.turn_right = 0
		if self.turn_right == 1:
			self.right = True
			self.target.run_right_animation()

		# Анимация бега
		if keyboard[key.LEFT]:
			self.turn_left += 1
			self.turn_right = 0
			self.idle_right = 0
			self.idle_left = 0
		else:
			self.turn_left = 0
		if self.turn_left == 1:
			self.right = False
			self.target.run_left_animation()

		# Прыжок
		if keyboard[key.SPACE]:
			self.space_key += 1
		else:
			self.space_key = 0
		if self.on_ground:
			self.is_jump = False
			self.allow_jump = True
			self.cur_jump_frame = 0
		if self.on_ground and self.space_key == 1 and self.allow_jump:
			self.is_jump = True
			self.allow_jump = False
		if self.is_jump and self.cur_jump_frame < self.jump_frames:
			dy += (self.jump_speed - self.cur_jump_frame * self.frame_delta_jump) * dt
			self.cur_jump_frame += 1

		# Анимация атаки
		if keyboard[key.LALT]:
			self.alt_key += 1
			if self.alt_key == 1 and time() - self.last_attack_time > self.attack_cd:
				if self.right:
					self.target.attack_right_animation()
				else:
					self.target.attack_left_animation()
				self.last_attack_time = time()
				self.attack_in_progress = True
		else:
			self.alt_key = 0
		if self.attack_in_progress and time() - self.last_attack_time > self.attack_duration:
			if self.right:
				self.target.idle_right_animation()
			else:
				self.target.idle_left_animation()
			self.attack_in_progress = False

		# "Гравитация"
		dy -= self.gravity_speed * dt

		# Столкновение с картой
		last_rect = self.target.get_rect()
		last_rect.size = (34, 54)
		last_rect.position = (last_rect.position[0] + 76, last_rect.position[1] + 28)
		new_rect = last_rect.copy()
		new_rect.x += dx
		new_rect.y += dy * dt

		self.target.velocity = self.collide_map(map_layer, last_rect, new_rect, dy, dx)
		self.on_ground = bool(new_rect.y == last_rect.y)
		# center of sprite (186x116) -> bottom left of rect (34x54) with offset: 76 to right, 28 to up
		self.target.position = (new_rect.position[0] + 17, new_rect.position[1] + 30)

		scroller.set_focus(self.target.x, self.target.y)


class MainLayer(ScrollableLayer):
	def __init__(self):
		super(MainLayer, self).__init__()
		self.collision_manager = cm.CollisionManagerBruteForce()

		# Игрок
		self.player = Player(game_controller.player_id)
		self.add(self.player, z=2)
		self.collision_manager.add(self.player)

		# Другие игроки
		self.other_players = []
		for i in range(game_controller.max_players):
			if i != self.player.player_id - 1:
				online_player = OnlinePlayer(i + 1)
				self.other_players.append(online_player)
				self.add(online_player)
				self.collision_manager.add(online_player)

		# Свины
		self.enemies = [Swin(0, (400, 600))]
		for e in self.enemies:
			#if self.player.player_id == 1:
			e.do(SwinAction())
			self.add(e)
			self.collision_manager.add(e)

		self.schedule(self.update)

	def update(self, dt):
		mes = {'type': 'position', 'player_id': game_controller.player_id, 'pos': self.player.position}

		if len(self.player.anim_list) > 0:
			mes['anim'] = self.player.anim_list.pop(0)
		else:
			mes['anim'] = 'none'

		#enemy_info = []
		#for e in self.enemies:
		#	enemy_info.append({'id': e.enemy_id,
		#					   'pos': e.position,
		#					   'alive': e.alive,
		#					   'state': e.state,
		#					   'right': e.right,
		#					   'activity': e.activity})
		#mes['enemy_info'] = enemy_info

		mes_bit = MyProtocol.getByteStrFromData(mes)
		game_controller.sock.send(mes_bit)
		data_bit = game_controller.sock.recv(10000)
		data = MyProtocol.getDataFromByteStr(data_bit)

		for p in self.other_players:
			p.position = data[f'pos_{p.player_id}']
			anim = data[f'anim_{p.player_id}']

			if anim == 'idle_r':
				p.idle_right_animation()
			elif anim == 'idle_l':
				p.idle_left_animation()
			elif anim == 'run_r':
				p.run_right_animation()
			elif anim == 'run_l':
				p.run_left_animation()
			elif anim == 'attack_r':
				p.attack_right_animation()
			elif anim == 'attack_l':
				p.attack_left_animation()

		if self.player.player_id == 1:
			self.player.cshape.center = self.player.position

			for e in self.enemies:
				e.cshape.center = e.position

			for p in self.other_players:
				p.cshape.center = p.position

			collisions = self.collision_manager.objs_colliding(self.player)
			print(collisions)




class Level1Scene(Scene):
	def __init__(self, g_c):
		super(Level1Scene, self).__init__()

		global keyboard, scroller, game_controller, map_layer
		game_controller = g_c
		scroller = ScrollingManager()
		keyboard = key.KeyStateHandler()
		director.window.push_handlers(keyboard)

		map_layer = load("tiles/map1/map_3.tmx")['base']
		map_h = (map_layer.cells[-1][-1].y // map_layer.tw + 1)
		map_layer_bg_0 = load("tiles/map1/map_3.tmx")['background']
		map_layer_bg_1 = load("tiles/map1/map_3.tmx")['decorations']

		main_layer = MainLayer()

		scroller.add(map_layer_bg_0, z=-2)
		scroller.add(map_layer_bg_1, z=-1)
		scroller.add(map_layer, z=0)
		scroller.add(main_layer, z=1)

		self.add(scroller)
		self.schedule_interval(main_layer.update, 1 / 30)  # 60 times per second
