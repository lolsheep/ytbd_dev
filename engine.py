import sys
import pygame
import character, event, items

EVENT = event.event()
DIR = "resources/"


config = {
	"name" : "Nothing",
	"dimensions" : (800,800),
	"background" : None
}


chara = character.Character()
Item = items.Item()
# Engine Factor class

class Factory:


	# When class is initialized, nothing is set until it calls set_config
	# There is no reason for this other than to save space and not have ugly code


	def __init__(self, config=config):
		# Initialize pygame
		pygame.init()

		self.fps = 60
		self.clock = pygame.time.Clock()
		# Set display as a public variable
		self.display = pygame.display
		# Assign config
		self.props = chara.props()
		self.eng_conf = config
		# Set window width and height to a tuple
		self.width, self.height = self.eng_conf["dimensions"]
		# Screen is not yet initialized, but this is pygame screen
		self.screen = self.display.set_mode((self.width, self.height))
		# Game name
		self.name = self.eng_conf["name"]
		# Background image file reference
		self.background_image = None
		# Game background object
		self.game_bg = None
		# Player Character
		self.character = chara.return_self()
		# Character sprite
		self.character_img = self.character.chara_frames
		self.character_load = None

		self.items = Item.return_self()
		self.items_load = []

		self.display.set_caption(self.name)

		self.set_img()

	def set_img(self):

		if self.eng_conf["background"] is None:

			self.background_image = "resources/background/def_bg.jpg" 

		else:

			self.background_image = self.eng_conf["background"]

		self.items_load = pygame.image.load(self.items.item_frames["sparkle"][0])

		self.game_bg = pygame.image.load(self.background_image)
		self.game_bg = pygame.transform.scale(self.game_bg, (self.width,self.height))

		if self.character.chara_img is not None:

			self.character_load = pygame.image.load(self.character_img[0])

	def return_self(self):

		return self

	

