import pygame

WIDTH = 480
HEIGHT = 360

# OUTPUT_WIDTH = 320
# OUTPUT_HEIGHT = 240

#MAP_FOCUS = (-5.9347681, 54.5889076)
MAP_FOCUS = (48.856255, 2.351277)

EVENTS = {
	'SONG_END': pygame.USEREVENT + 1
}

ACTIONS = {
	pygame.K_F1: "module_stats",
	pygame.K_F2: "module_items",
	pygame.K_F3: "module_data",
	pygame.K_1:	"knob_1",
	pygame.K_2: "knob_2",
	pygame.K_3: "knob_3",
	pygame.K_4: "knob_4",
	pygame.K_5: "knob_5",
	pygame.K_UP: "dial_up",
	pygame.K_DOWN: "dial_down",
	pygame.K_p: "play",
	pygame.K_s: "stop",
	pygame.K_SPACE : "dial_select"
}

# Using GPIO.BCM as mode
GPIO_ACTIONS = {
#     4: "module_stats", #GPIO 4
# 	14: "module_items", #GPIO 14
# 	15: "module_data", #GPIO 15
# 	17:	"knob_1", #GPIO 17
# 	18: "knob_2", #GPIO 18
# 	7: "knob_3", #GPIO 7
# 	22: "knob_4", #GPIO 22
# 	23: "knob_5", #GPIO 27
# #	31: "dial_up", #GPIO 23
# 	27: "dial_down" #GPIO 7
}


MAP_ICONS = {
	"camp": 		pygame.image.load('images/map_icons/camp.png'),
	"factory": 		pygame.image.load('images/map_icons/factory.png'),
	"metro": 		pygame.image.load('images/map_icons/metro.png'),
	"misc": 		pygame.image.load('images/map_icons/misc.png'),
	"monument": 	pygame.image.load('images/map_icons/monument.png'),
	"vault": 		pygame.image.load('images/map_icons/vault.png'),
	"settlement": 	pygame.image.load('images/map_icons/settlement.png'),
	"ruin": 		pygame.image.load('images/map_icons/ruin.png'),
	"cave": 		pygame.image.load('images/map_icons/cave.png'),
	"landmark": 	pygame.image.load('images/map_icons/landmark.png'),
	"city": 		pygame.image.load('images/map_icons/city.png'),
	"office": 		pygame.image.load('images/map_icons/office.png'),
	"sewer": 		pygame.image.load('images/map_icons/sewer.png'),
}

AMENITIES = {
	'pub': 				MAP_ICONS['vault'],
	'nightclub': 		MAP_ICONS['vault'],
	'bar': 				MAP_ICONS['vault'],
	'fast_food': 		MAP_ICONS['sewer'],
	'cafe': 			MAP_ICONS['sewer'],
	'drinking_water': 	MAP_ICONS['sewer'],
	'restaurant': 		MAP_ICONS['settlement'],
	'cinema': 			MAP_ICONS['office'],
	'pharmacy': 		MAP_ICONS['office'],
	'school': 			MAP_ICONS['office'],
	'bank': 			MAP_ICONS['monument'],
	'townhall': 		MAP_ICONS['monument'],
	'bicycle_parking': 	MAP_ICONS['misc'],
	'place_of_worship': MAP_ICONS['misc'],
	'theatre': 			MAP_ICONS['misc'],
	'bus_station': 		MAP_ICONS['misc'],
	'parking': 			MAP_ICONS['misc'],
	'fountain': 		MAP_ICONS['misc'],
	'marketplace': 		MAP_ICONS['misc'],
	'atm': 				MAP_ICONS['misc'],
}

pygame.font.init()
FONTS = {}
for x in range(10, 28):
	FONTS[x] = pygame.font.Font('monofonto.ttf', x)


SPECIAL = [
	'Strengh          5',
	'Perception       8',
	'Endurance        3',
	'Charisme         2',
	'Intelligence     6',
	'Agility          12',
	'Luck             8'
]

# Items [Name, weight, value, icon_path_in_prop_dir]
WEAPON = [
	['Big fucking rifle', 1158, 20, 'rifle.png'],
	['Baseball bat', 18, 20, 'bat.png'],
	['Tazer', 18, 20, 'tazer.png']
]

APPAREL = [
	['Vault 101 suit', 2, 150, 'vault.png'],
	['Steampunk glasses', 2, 150, 'vault.png'],
	['Steampunk hat', 2, 150, 'vault.png'],
	['Moon boots', 2, 150, 'vault.png']
]

AIDS = [
	['Stimpack', 3, 10, 'stimpak.png'],
	['Rad-Away', 3, 10, 'stimpak.png'],
	['Stealth boy', 3, 10, 'stimpak.png'],
	['Popcorn', 3, 500, 'stimpak.png'],
	['Rat meat', 3, 10, 'stimpak.png'],
	['Cereal bar', 3, 10, 'stimpak.png']
]

MISC = [
	['OnePlus One', 3, 300, 'stimpak.png'],
	['House keys', 3, 10, 'stimpak.png'],
	['Bus card', 3, 10, 'stimpak.png']
]

AMMO = [
	'9mm ammo         750',
	'357 magnum       120'
]

RADIOSTATION = [
	'Galaxy News Radio',
	'Radio New Vegas',
	'Mojave Music'
]

RADIODIR = [
	'sounds\\radio\\gnr\\',
	'sounds\\radio\\rnv\\',
	'sounds\\radio\\mm\\'
]

PERK = [
	['Computer Whiz', 'Can make one extra attempt to hack a locked-down terminal', 'computerwiz.png']
]
# OBJECTS