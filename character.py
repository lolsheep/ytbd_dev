import sys, pygame

DIR = "resources/"


class Character:


	def __init__(self):

		self.properties = {

			"character_img" : DIR+"character/ghost/frames/1.png",
			"character_frames" : [DIR+"character/ghost/frames/1.png",DIR+"character/ghost/frames/2.png"],
			"character_stats" : {"character_speed" : 10 },
		}
		self.pickups = {
			"coin" : DIR+"coin.png"
		}

		self.chara_img = self.properties["character_img"]
		self.chara_frames = self.properties["character_frames"]
		self.stats = self.properties["character_stats"]
		self.speed = self.stats["character_speed"]

		self.x = 10
		self.y = 400
		self.face = "l"
		
		self.curr_frame = 0
		self.curr_anim = 0



	def props(self):
		return self.properties

	def move(self,coord,face):
		self.x = coord[0]
		self.y = coord[1]
		self.face = face

	def return_xy(self):
		print(self.x)
		return (self.x,self.y)
	
	def animate(self,ch_img,curr_frame):

		new_frame = curr_frame+1
  
		try:

			re = ch_img[new_frame] 

		except IndexError:
      
			new_frame = 0
			re = ch_img[0]
		
		return (pygame.image.load(re),new_frame)



	def return_self(self):

		return self






