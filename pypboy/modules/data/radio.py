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
		print(os.path.exists(config.RADIODIR[index]))
		self.radio.set_directory(config.RADIODIR[index])
		self.radio.load_files()
		self.radio.play_random()
		self.oscillo.load_music(self.radio.filename)
		pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])

	def stop_station(self, index):
		self.radio.stop()
		print('stop')

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


# class Oscilloscope(game.Entity):
# 	def __init__(self):
# 		super(Oscilloscope, self).__init__()
# 		self.WIDTH = 480
# 		self.HEIGHT = 350
# 		self.image = pygame.Surface((self.WIDTH, self.HEIGHT), 0)
# 		self.rect = self.image.get_rect()
# 		self.xaxis = self.HEIGHT/2
# 		pygame.draw.line(self.image, color, (p[0], p[1]), (p[2], p[1]), 2)
# 		pygame.draw.line(self.image, color, (p[2], p[1]), (p[2], p[3]), 2)
# 		# Graduations
# 		w = p[2] - p[0]
# 		h = p[1] - p[3]
# 		stepw = float(w) / nbGrad;
# 		steph = float(h) / nbGrad;
# 		print(stepw)
# 		height = gradHeight
# 		for u in range(nbGrad):
# 			if u % 5 ==0:
# 				pygame.draw.line(self.image, color, (p[0] + u * stepw, p[1]), (p[0] + u * stepw, p[1] - bigGrandHeight), 1)
# 				pygame.draw.line(self.image, color, (p[2] - bigGrandHeight, p[3] + u * steph), (p[2], p[3] + u * steph), 1)
# 			else:
# 				pygame.draw.line(self.image, color, (p[0] + u * stepw, p[1]), (p[0] + u * stepw, p[1] - gradHeight), 1)
# 				pygame.draw.line(self.image, color, (p[2] - gradHeight, p[3] + u * steph), (p[2], p[3] + u * steph), 1)
# 			print((p[0] + u * stepw, p[1]))
# 		self.image = self.image.convert()
# 		self.blank = self.image.copy()
# 		self.draw(5.0, 20, 3)
# 		self.blank = numpy.zeros((self.WIDTH, self.HEIGHT, 3))
# 		#pygame.surfarray.blit_array(self.image, self.blank)
# 		# while True:
# 		# 	self.draw(5.0, 20, 3)


# 	def draw(self,time,frequency,power):
# 		# try:
# 			pixels = copy.copy(self.image)
# 			offset = 1
# 			for x in range(self.WIDTH):
# 				offset = offset - 1
# 				if offset < -1:
# 					offset = offset + 1.1
# 				try:
# 					pow = power[int(x/10)]
# 					log = math.log10( pow )
# 					offset = ((pow / math.pow(10, math.floor(log))) + log)*1.8
# 				except:
# 					pass
# 				try:
# 					y = float(self.xaxis) - (math.sin((float(x)+float(time))/5.0)*2.0*offset)
# 					pixels[x][y] = self.TRACE
# 					pixels[x][y-1] = self.AFTER
# 					pixels[x][y+1] = self.AFTER
# 					if abs(y) > 120:
# 						pixels[x][y-2] = self.AFTER
# 						pixels[x][y+2] = self.AFTER
# 				except:
# 					pass
# 			# for w in range(self.WIDTH):
# 			# 	for h in range(self.HEIGHT):
# 			# 		self.blank.set_at((w,h), pixels[w][h])
# 			# if not self.embedded:
# 			# 	pygame.display.flip()
# 		# except Exception as e:
# 		# 	print(e)