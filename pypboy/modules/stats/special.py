import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

	label = "S.P.E.C.I.A.L."

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		self.menu = pypboy.ui.Menu(200, config.SPECIAL, [], 0)
		self.menu.rect[0] = 15
		self.menu.rect[1] = 40
		self.add(self.menu)