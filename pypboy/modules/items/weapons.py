import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

	label = " Weapons "

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		self.menu = pypboy.ui.SelectableMenu(200, [p[0] for p in config.WEAPON], [], self.update_content, 0, True)
		self.menu.rect[0] = 15
		self.menu.rect[1] = 40
		self.add(self.menu)
		self.item_view = pypboy.ui.Itemview(config.WEAPON, 'art\\weapon\\', True)
		self.item_view.rect[0] = 245
		self.item_view.rect[1] = 60
		self.add(self.item_view)
		self.item_view.set_element(self.menu.selected)

	def update_content(self, index):
		self.item_view.set_element(index)