import game
import config
import pygame
import datetime
import os

class Header(game.Entity):

	def __init__(self, headline="", title=""):
		self.headline = headline
		self.title = title
		super(Header, self).__init__((config.WIDTH, config.HEIGHT))
		self.rect[0] = 4
		self._date = None

	def update(self, *args, **kwargs):
		super(Header, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		new_date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
		if new_date != self._date:
			self.image.fill((0, 0, 0))
			pygame.draw.line(self.image, (95, 255, 177), (5, 15), (5, 35), 2)
			pygame.draw.line(self.image, (95, 255, 177), (5, 15), (config.WIDTH - 154, 15), 2)
			pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 154, 15), (config.WIDTH - 154, 35), 2)
			pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 148, 15), (config.WIDTH - 13, 15), 2)
			pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 13, 15), (config.WIDTH - 13, 35), 2)

			text = config.FONTS[14].render("  %s  " % self.headline, True, (105, 251, 187), (0, 0, 0))
			self.image.blit(text, (26, 8))
			text = config.FONTS[14].render(self.title, True, (95, 255, 177), (0, 0, 0))
			self.image.blit(text, ((config.WIDTH - 154) - text.get_width() - 10, 19))
			text = config.FONTS[14].render(self._date, True, (95, 255, 177), (0, 0, 0))
			self.image.blit(text, ((config.WIDTH - 141), 19))
			self._date = new_date

		super(Header, self).update(*args, **kwargs)

class Footer(game.Entity):

	def __init__(self):
		self.menu = []
		super(Footer, self).__init__((config.WIDTH, config.HEIGHT))
		self.rect[0] = 4
		self.rect[1] = config.HEIGHT - 40

	def update(self, *args, **kwargs):
		super(Footer, self).update(*args, **kwargs)

	def select(self, module):
		#self.dirty = 1
		self.selected = module
		self.image.fill((0, 0, 0))
		pygame.draw.line(self.image, (95, 255, 177), (5, 2), (5, 20), 2)
		pygame.draw.line(self.image, (95, 255, 177), (5, 20), (config.WIDTH - 13, 20), 2)
		pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 13, 2), (config.WIDTH - 13, 20), 2)

		offset = 20
		for m in self.menu:
			padding = 1
			text_width = 0
			while text_width < 54:
				spaces = " ".join([" " for x in range(padding)])
				text = config.FONTS[12].render("%s%s%s" % (spaces, m, spaces), True, (105, 255, 187), (0, 0, 0))
				text_width = text.get_size()[0]
				padding += 1
			if m == self.selected:
				pygame.draw.rect(self.image, (95, 255, 177), (offset - 2, 6, (text_width + 3), 26), 2)
			self.image.blit(text, (offset, 12))

			offset = offset + 120 + (text_width - 100)
types = ['WG', 'VAL']
data_string_size = 11

# Main itemview params
poses=[0, 97]
posey = 180
size = [97, 20]

[ 100, 20 ]
class Itemview(game.Entity):

	def __init__(self, items, art_dir='', is_sellable=False):
		super(Itemview, self).__init__((config.WIDTH, config.HEIGHT))
		self.is_sellable = is_sellable
		self.content = ['', ''] if is_sellable else ['']
		self.items = items
		self.art_dir = art_dir
		self.rect[2] = 185
		self.rect[3] = 185
		self.art = None

	def set_element(self, index):
		self.content = [self.items[index][1], self.items[index][2]] if self.is_sellable else [self.items[index][1]]
		self.art = pygame.image.load(os.path.join(self.art_dir, self.items[index][-1]))
		if self.is_sellable:
			self.art = pygame.transform.scale(self.art, (160, 160))
		else:
			self.art = pygame.transform.scale(self.art, (160, 160))
		self.redraw()

	def split_text(self, text, length):
		textlength = len(text)
		index = 0
		elements = []
		text.rstrip()
		while index < textlength:
			t = text[index * length:(index + 1) * length:]
			elements.append(t)
			index+=1
		return elements

	def build_content(self, index):
		if self.is_sellable:
			toto = '{}{}{}'.format(types[index], ' ' * (data_string_size - (len(types[index]) +len(str(self.content[index])))), self.content[index])
		else:
			toto = self.split_text(self.content[index], 30)
		return toto

	def redraw(self):
		self.image.fill((0, 0, 0))
		offset = 5
		#pygame.draw.line(self.image, (95, 255, 177), (0, 2), (180, 2), 2)
		if self.is_sellable:
			pygame.draw.line(self.image, (95, 255, 177), (poses[0], posey ), (poses[0] + size[0] - 4, posey) , 2)
			pygame.draw.line(self.image, (95, 255, 177), (poses[1], posey ), (poses[1] + size[0] - 4, posey) , 2)
			pygame.draw.line(self.image, (95, 255, 177), (poses[0] + size[0] - 4, posey ), (poses[0] + size[0] - 4, posey + size[1]) , 2)
			pygame.draw.line(self.image, (95, 255, 177), (poses[1] + size[0] - 4, posey ), (poses[1] + size[0] - 4, posey + size[1]) , 2)
			text = config.FONTS[16].render(self.build_content(0), True, (105, 255, 187), (0, 0, 0))
			self.image.blit(text, (0, posey + 2))
			text = config.FONTS[16].render(self.build_content(1), True, (105, 255, 187), (0, 0, 0))
			self.image.blit(text, (poses[1], posey + 2))
			self.image.blit(self.art, (0, 0))
		else:
			pygame.draw.line(self.image, (95, 255, 177), (poses[0], posey ), (poses[0] + size[0] * 2 + 18 , posey) , 2)
			pygame.draw.line(self.image, (95, 255, 177), (poses[1] + size[0] + 18, posey ), (poses[1] + size[0] +18, posey + size[1]) , 2)
			index = 0
			toto = self.build_content(0)
			for el in toto:
				text = config.FONTS[14].render(el, True, (105, 255, 187), (0, 0, 0))
				self.image.blit(text, (0, posey + 3 + index * (text.get_size()[1] + 6)))
				index += 1
			self.image.blit(self.art, (0, 0))
		# for i in range(len(self.items)):
		# 	text = config.FONTS[14].render(" %s " % self.items[i], True, (105, 255, 187), (0, 0, 0))
		# 	self.image.blit(text, (10, offset))
		# 	offset += text.get_size()[1] + 6

#square types [small, large, perks]
SMALL = [ 80, 20 , 9]
MID = [ 160, 20 , 19]
LARGE = [ 236, 20 , 29]
PERK =  [ 200, 100, 90]
offset_x = 6
class AidsView(game.Entity):
	# item_data: list of data elements to be added
	# item_layout: one dimension list with indexes for ui type (SMALL=1, LARGE=2, PERK=3  adding - to keep space of element)
	def __init__(self, item_data, item_layout, data_caption, art_dir=''):
		super(AidsView, self).__init__((config.WIDTH, config.HEIGHT))
		self.content = []
		self.item_data = item_data
		self.item_layout = item_layout
		self.data_caption = data_caption
		self.rect[2] = 185
		self.rect[3] = 185
		self.art_dir = art_dir
		self.art = None

	def set_element(self, index):
		self.content = self.item_data[index][1:len(self.data_caption) + 1:]
		self.art = pygame.image.load(os.path.join(self.art_dir, self.item_data[index][-1]))
		self.art = pygame.transform.scale(self.art, (155, 155))
		self.redraw()

	def split_text(self, text, length):
		textlength = len(text)
		index = 0
		elements = []
		text.rstrip()
		while index < textlength:
			t = text[index * length:(index + 1) * length:]
			elements.append(t)
			index+=1
		return elements

	def build_content(self, index, string_size):
		if(len(self.data_caption) == 0):
				caption = self.content[index]
		else:
				caption = '{}{}{}'.format(self.data_caption[index], ' ' * (string_size - (len(self.data_caption[index]) + len(str(self.content[index])))), self.content[index])
		return caption

	# def draw_small(self, index, pos_x, pos_y):
	# 	pygame.draw.line(self.image,
	# 		(95, 255, 177),
	# 		(pos_x, pos_y ), (pos_x + SMALL[0] - 4, pos_y),
	# 		 2)
	# 	pygame.draw.line(self.image,
	# 		(95, 255, 177),
	# 		(pos_x + SMALL[0] - 4, pos_y ), (pos_x + SMALL[0] - 4, pos_y + SMALL[1]),
	# 		 2)

	# 	return pos_x + SMALL[0]

	def draw_small(self, index, pos_x, pos_y):
		pygame.draw.line(self.image,
			(95, 255, 177),
			(pos_x, pos_y ), (pos_x + SMALL[0] - 4, pos_y),
			 2)
		pygame.draw.line(self.image,
			(95, 255, 177),
			(pos_x + SMALL[0] - 4, pos_y ), (pos_x + SMALL[0] - 4, pos_y + SMALL[1]),
			 2)

	def draw_mid(self, index, pos_x, pos_y):
		pygame.draw.line(self.image,
			(95, 255, 177),
			(pos_x, pos_y ), (pos_x + MID[0] - 4, pos_y),
			 2)
		pygame.draw.line(self.image,
			(95, 255, 177),
			(pos_x + MID[0] - 4, pos_y ), (pos_x + MID[0] - 4, pos_y + MID[1]),
			 2)
		return pos_x + MID[0]

	def draw_large(self, index, pos_y):
		pygame.draw.line(self.image,
			(95, 255, 177),
			(0, pos_y ), (LARGE[0], pos_y),
			 2)
		pygame.draw.line(self.image,
			(95, 255, 177),
			(LARGE[0], pos_y ), (LARGE[0], pos_y + LARGE[1]),
			 2)

	def redraw(self):
		self.image.fill((0, 0, 0))
		offset = 5
		offset_x = 0
		offset_y = 175
		current_line_score = 0
		for e, t in enumerate(self.item_layout):
			if t == 1:
				text = config.FONTS[16].render(self.build_content(e, SMALL[2]), True, (105, 255, 187), (0, 0, 0))
				self.image.blit(text, (offset_x, offset_y))
				self.draw_small(e, offset_x, offset_y)
				offset_x += SMALL[0]
				current_line_score += 1
			if t == 2:
				text = config.FONTS[16].render(self.build_content(e, MID[2]), True, (105, 255, 187), (0, 0, 0))
				self.image.blit(text, (offset_x, offset_y))
				self.draw_mid(e, offset_x, offset_y)
				offset_y += 20 + offset_y
			if t == 3:
				offset_y += 20 + offset
				text = config.FONTS[16].render(self.build_content(e, LARGE[2]), True, (105, 255, 187), (0, 0, 0))
				self.image.blit(text, (0, offset_y))
				self.draw_large(e, offset_y)
			if t == 4:
				caption = self.split_text(self.content[e], 32)
				for i, el in enumerate(caption):
					text = config.FONTS[14].render(el, True, (105, 255, 187), (0, 0, 0))
					self.image.blit(text, (0, posey + i * (text.get_size()[1])))
				self.draw_large(e, offset_y)
			if current_line_score == 3 and e < len(self.item_layout) - 2 and self.item_layout[e + 1] != 3 :
				offset_y += 20 + offset
				current_line_score = 0
				offset_x = 0

		self.image.blit(self.art, (40, 0))

class Menu(game.Entity):

	def __init__(self, width, items=[], callbacks=[], selected=0):
		super(Menu, self).__init__((width, config.HEIGHT - 80))
		self.items = items
		self.callbacks = callbacks
		self.selected = 0
		self.select(selected)

		if config.SOUND_ENABLED:
			self.dial_move_sfx = pygame.mixer.Sound('sounds/dial_move.ogg')

	def select(self, item):
		self.selected = item
		self.redraw()
		if len(self.callbacks) > item and self.callbacks[item]:
			self.callbacks[item]()

	def handle_action(self, action):
		if action == "dial_up":
			if self.selected > 0:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.select(self.selected - 1)
		if action == "dial_down":
			if self.selected < len(self.items) - 1:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.select(self.selected + 1)

	def redraw(self):
		self.image.fill((0, 0, 0))
		offset = 5
		for i in range(len(self.items)):
			text = config.FONTS[14].render(" %s " % self.items[i], True, (105, 255, 187), (0, 0, 0))
			if i == self.selected:
				selected_rect = (5, offset - 2, text.get_size()[0] + 6, text.get_size()[1] + 3)
				pygame.draw.rect(self.image, (95, 255, 177), selected_rect, 2)
			self.image.blit(text, (10, offset))
			offset += text.get_size()[1] + 6

class SelectableMenu(game.Entity):
	def __init__(self, width, items=[], callbacks=[], select_callback = None, selected=0, multi=False):
		super(SelectableMenu, self).__init__((width, config.HEIGHT - 80))
		self.items = items
		self.callbacks = callbacks
		self.select_callback = select_callback
		self.selected = 0
		self.enabled = []
		self.select(selected)
		self.multi = multi;

		if config.SOUND_ENABLED:
			self.dial_move_sfx = pygame.mixer.Sound('sounds/dial_move.ogg')

	def select(self, item):
		self.selected = item
		self.redraw()

	def getEnabled(self):
		if self.enabled:
			return self.enabled[0]

	def enableItem(self, index):
		if index in self.enabled:
			self.enabled.remove(index)
			if len(self.callbacks) == 2:
				self.callbacks[1](index)
		else:
			if self.multi is False:
				self.enabled = []

			self.enabled.append(index)
			if len(self.callbacks) > 0:
				self.callbacks[0](index)

		self.redraw()

	def handle_action(self, action):
		if action == "dial_up":
			if self.selected > 0:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.select(self.selected - 1)
				if self.select_callback:
					self.select_callback(self.selected)
		if action == "dial_down":
			if self.selected < len(self.items) - 1:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.select(self.selected + 1)
				if self.select_callback:
					self.select_callback(self.selected)
		if action == "dial_select":
			if self.selected is not None:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.enableItem(self.selected)

	def redraw(self):
		self.image.fill((0, 0, 0))
		offset = 5
		for i in range(len(self.items)):
			text = config.FONTS[14].render(" %s " % self.items[i], True, (105, 255, 187), (0, 0, 0))
			if i == self.selected:
				selected_rect = (0, offset - 2, 180, text.get_size()[1] + 3)
				pygame.draw.rect(self.image, (95, 255, 177), selected_rect, 2)
			if i in self.enabled:
				pygame.draw.rect(self.image, (95, 255, 177), [9, text.get_size()[1]/2.0 + offset - 2, 6, 6] , 0)
			self.image.blit(text, (15, offset))
			offset += text.get_size()[1] + 6

class Scanlines(game.Entity):

	def __init__(self, width, height, gap, speed, colours, full_push=False):
		super(Scanlines, self).__init__((width, height))
		self.width = width
		self.height = height
		self.move = gap * len(colours)
		self.gap = gap
		self.colours = colours
		self.rect[1] = 0
		self.top = 0.0
		self.speed = speed
		self.full_push =full_push
		colour = 0
		area = pygame.Rect(0, self.rect[1] * self.speed, self.width, self.gap)
		while area.top <= self.height - self.gap:
			self.image.fill(self.colours[colour], area)
			area.move_ip(0, (self.gap))
			colour += 1
			if colour >= len(self.colours):
				colour = 0

	def render(self, interval, *args, **kwargs):
		self.top += self.speed * interval
		self.rect[1] = self.top
		self.dirty = 1
		if self.full_push:
			if self.top >= self.height:
				self.top = 0
		else:
			if (self.top * self.speed) >= self.move:
				self.top = 0
		super(Scanlines, self).render(self, *args, **kwargs)


class Overlay(game.Entity):
	def __init__(self):
		self.image = pygame.image.load('images/overlay.png')
		super(Overlay, self).__init__((config.WIDTH, config.HEIGHT))
		self.blit_alpha(self, self.image, (0, 0), 128)

	def blit_alpha(self, target, source, location, opacity):
		x = location[0]
		y = location[1]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(target, (-x, -y))
		temp.blit(source, (0, 0))
		temp.set_alpha(opacity)
		target.blit(temp, location)


class Border(game.Entity):
	def __init__(self):
		super(Border, self).__init__()
		self.image = pygame.image.load('images/border.png')
		self.rect = self.image.get_rect()