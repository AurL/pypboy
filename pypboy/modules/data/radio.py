import pypboy
import config

from pypboy.modules.data import entities


#Radio
import pygame
import numpy
from math import log10
import math
from random import randint
from entities import Oscilloscope
import copy
import game
import os
from random import choice
from radioui import Oscilloscope
#temp
p=[245, 245, 430, 60]  # botom left,  bottom right + top level
nbGrad = 40
color = (20, 155, 40)

gradHeight = 7
bigGrandHeight = 13

class Module(pypboy.SubModule):

	label = "Radio"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		self.oscillo = Oscilloscope()
		self.oscillo.rect[0] = 245
		self.oscillo.rect[1] = 85
		self.add(self.oscillo)
		self.menu = pypboy.ui.SelectableMenu(200, config.RADIOSTATION, [self.play_station, self.stop_station], 0)
		self.menu.rect[0] = 15
		self.menu.rect[1] = 40
		self.add(self.menu)
		self.radio = Radio(self.oscillo)
		# self.ocilloscope = Oscilloscope()

	def play_station(self, index):
		self.radio.set_directory(config.RADIODIR[index])
		self.radio.load_files()
		self.radio.play_random()
		self.oscillo.load_music(self.radio.filename)
		pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])

	def stop_station(self, index):
		self.radio.stop()

	# def render(self, interval=0, *args, **kwargs):


class Radio(game.Entity):

	STATES = {
		'stopped': 0,
		'playing': 1,
		'paused': 2
	}

	def __init__(self, oscillo, *args, **kwargs):
		super(Radio, self).__init__((10, 10), *args, **kwargs)

		self.state = self.STATES['stopped']
		self.directory = '';
		self.files = []
		self.oscillo = oscillo
		pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])

	def set_directory(self, directory):
		self.directory = directory

	def play_random(self):
		f = choice(self.files)
		self.filename = f
		pygame.mixer.music.load(f)
		pygame.mixer.music.play()
		self.state = self.STATES['playing']
		self.oscillo.running = True

	def play(self):
		if self.state == self.STATES['paused']:
			pygame.mixer.music.unpause()
			self.state = self.STATES['playing']
		else:
			self.play_random()
		self.oscillo.running = True

	def pause(self):
		self.state = self.STATES['paused']
		pygame.mixer.music.pause()

	def stop(self):
		self.state = self.STATES['stopped']
		pygame.mixer.music.stop()

	def load_files(self):
		files = []
		for f in os.listdir(self.directory):
			if f.endswith(".mp3") or f.endswith(".ogg") or f.endswith(".wav"):
				files.append(self.directory + f)
		self.files = files