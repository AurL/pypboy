import pygame
import numpy
import math
import copy
import traceback
from math import log10
from numpy.fft import fft
import game

class SoundSpectrum:
	"""
	Obtain the spectrum in a time interval from a sound file.
	"""

	left = None
	right = None

	def __init__(self, filename, force_mono=False):
		"""
		Create a new SoundSpectrum instance given the filename of
		a sound file pygame can read. If the sound is stereo, two
		spectra are available. Optionally mono can be forced.
		"""
		# Get playback frequency
		nu_play, format, stereo = pygame.mixer.get_init()
		self.nu_play = 1./nu_play
		self.format = format
		self.stereo = stereo

		# Load sound and convert to array(s)
		sound = pygame.mixer.Sound(filename)
		a = pygame.sndarray.array(sound)
		a = numpy.array(a)
		if stereo:
			if force_mono:
				self.stereo = 0
				self.left = (a[:,0] + a[:,1])*0.5
			else:
				self.left = a[:,0]
				self.right = a[:,1]
		else:
			self.left = a

	def get(self, data, start, stop):
		"""
		Return spectrum of given data, between start and stop
		time in seconds.
		"""
		duration = stop-start
		# Filter data
		start = int(start/self.nu_play)
		stop = int(stop/self.nu_play)
		N = stop - start
		data = data[start:stop]

		# Get frequencies
		frequency = numpy.arange(N/2)/duration

		# Calculate spectrum
		spectrum = fft(data)[1:1+N/2]
		power = (spectrum).real

		return frequency, power

	def get_left(self, start, stop):
		"""
		Return spectrum of the left stereo channel between
		start and stop times in seconds.
		"""
		return self.get(self.left, start, stop)

	def get_right(self, start, stop):
		"""
		Return spectrum of the left stereo channel between
		start and stop times in seconds.
		"""
		return self.get(self.right, start, stop)

	def get_mono(self, start, stop):
		"""
		Return mono spectrum between start and stop times in seconds.
		Note: this only works if sound was loaded as mono or mono
		was forced.
		"""
		return self.get(self.left, start, stop)

class LogSpectrum(SoundSpectrum):
	"""
	A SoundSpectrum where the spectrum is divided into
	logarithmic bins and the logarithm of the power is
	returned.
	"""

	def __init__(self, filename, force_mono=False, bins=20, start=1e2, stop=1e4):
		"""
		Create a new LogSpectrum instance given the filename of
		a sound file pygame can read. If the sound is stereo, two
		spectra are available. Optionally mono can be forced.
		The number of spectral bins as well as the frequency range
		can be specified.
		"""
		SoundSpectrum.__init__(self, filename, force_mono=force_mono)
		start = log10(start)
		stop = log10(stop)
		step = (stop - start)/bins
		self.bins = 10**numpy.arange(start, stop+step, step)

	def get(self, data, start, stop):
		"""
		Return spectrum of given data, between start and stop
		time in seconds. Spectrum is given as the log of the
		power in logatithmically equally sized bins.
		"""
		f, p = SoundSpectrum.get(self, data, start, stop)
		bins = self.bins
		length = len(bins)
		result = numpy.zeros(length)
		ind = numpy.searchsorted(bins, f)
		for i,j in zip(ind, p):
			if i<length:
				result[i] += j
		return bins, result

p=[0, 185, 185, 0]  # botom left,  bottom right + top level
nbGrad = 40
color = (20, 155, 40)

gradHeight = 7
bigGrandHeight = 13
pos = [200, 200]

TRACE, AFTER, GREY = (80, 255, 100),(20, 155, 40),(20, 110, 30)

class Oscilloscope(game.Entity):
	def __init__(self):
		super(Oscilloscope, self).__init__((185, 185))

		# Sound
		clock = pygame.time.Clock()
		# set up the mixer
		freq = 44100	 # audio CD quality
		bitsize = 16	# unsigned 16 bit
		channels = 2	 # 1 is mono, 2 is stereo
		buffer = 2048	# number of samples (experiment to get right sound)
		self.mixer = pygame.mixer.init(freq, bitsize, channels, buffer)
		self.running = False
		self.spectrum = None

		# Dimensions
    	# Position
		self.WIDTH = 188
		self.HEIGHT = 188
		self.image = pygame.Surface((self.WIDTH, self.HEIGHT), 0)
		# self.rect[0] =  50
		# self.rect[1] =  50
		self.image.fill((0, 0, 0))
		# pygame.draw.line(self.image, color, (10, 10), (50, 50), 2)
		self.image.blit
		self.rect[2] = self.rect[3] = 185
		self.image = pygame.Surface((self.WIDTH, self.HEIGHT), 0)
		self.xaxis = self.HEIGHT/2
		pygame.draw.line(self.image, color, (p[0], p[1]), (p[2], p[1]), 2)
		pygame.draw.line(self.image, color, (p[2], p[1]), (p[2], p[3]), 2)
		# Graduations
		w = p[2] - p[0]
		h = p[1] - p[3]
		stepw = float(w) / nbGrad;
		steph = float(h) / nbGrad;
		height = gradHeight
		for u in range(nbGrad):
			if u % 5 ==0:
				pygame.draw.line(self.image, color, (p[0] + u * stepw, p[1]), (p[0] + u * stepw, p[1] - bigGrandHeight), 1)
				pygame.draw.line(self.image, color, (p[2] - bigGrandHeight, p[3] + u * steph), (p[2], p[3] + u * steph), 1)
			else:
				pygame.draw.line(self.image, color, (p[0] + u * stepw, p[1]), (p[0] + u * stepw, p[1] - gradHeight), 1)
				pygame.draw.line(self.image, color, (p[2] - gradHeight, p[3] + u * steph), (p[2], p[3] + u * steph), 1)
		self.image = self.image.convert()
		self.blank = self.image.copy()
		#self.draw(5.0, 20, 3)
		#self.blank = numpy.zeros((self.WIDTH, self.HEIGHT, 3))
		#pygame.surfarray.blit_array(self.image, self.blank)
		# while True:
		# 	self.draw(5.0, 20, 3)

	def draw_oscillo(self, blank, time, power):
		try:
			pixels = pygame.surfarray.pixels2d(blank)[0]
			offset = 1
			for x in range(self.WIDTH):
				offset = offset - 1
				if offset < -1:
					offset = offset + 1.1
				try:
					pow = power[int(x/10)]
					log = math.log10( pow )
					offset = ((pow / math.pow(10, math.floor(log))) + log)*3
				except Exception as e:
					pass
				try:
					y = float(self.xaxis) - (math.sin((float(x)+float(time))/5.0)*2.0*offset)
					blank.set_at((x, int(y)), TRACE)
					blank.set_at((x, int(y-1)), AFTER)
					blank.set_at((x, int(y+1)), AFTER)
					if abs(y) > 120:
						blank.set_at((x, int(y -2)), AFTER)
						blank.set_at((x, int(y +2)), AFTER)
					# pixels[x][int(y-1)] = AFTER
					# pixels[x][int(y+1)] = AFTER
					# if abs(y) > 120:
					# 	pixels[x][int(y-2)] = AFTER
					# 	pixels[x][int(y+2)] = AFTER
				except Exception as e:
					pass
			#pygame.surfarray.blit_array(blank, pixels)	 # Blsit the screen buffer
			pygame.display.flip()
		except Exception,e:
			print traceback.format_exc()

	def update(self):
		self.image = copy.copy(self.blank)
		if pygame.mixer.music.get_busy() and self.running and self.spectrum is not None:
			start = pygame.mixer.music.get_pos() / 1000.0
			try:
				f,p = self.spectrum.get_mono(start, start+0.002)
			except:
				pass
			self.draw_oscillo(self.image, start,p)
			pygame.time.wait(50)


	def load_music(self, file):
		self.spectrum = LogSpectrum(file,force_mono=True)

	def draw(self,time,frequency,power):
		# try:
			pixels = copy.copy(self.image)
			offset = 1
			for x in range(self.WIDTH):
				offset = offset - 1
				if offset < -1:
					offset = offset + 1.1
				try:
					pow = power[int(x/10)]
					log = math.log10( pow )
					offset = ((pow / math.pow(10, math.floor(log))) + log)*1.8
				except:
					pass
				try:
					y = float(self.xaxis) - (math.sin((float(x)+float(time))/5.0)*2.0*offset)
					pixels[x][y] = self.TRACE
					pixels[x][y-1] = self.AFTER
					pixels[x][y+1] = self.AFTER
					if abs(y) > 120:
						pixels[x][y-2] = self.AFTER
						pixels[x][y+2] = self.AFTER
				except:
					pass
