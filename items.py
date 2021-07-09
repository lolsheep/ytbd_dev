import pygame,os

DIR = "resources/"


class Item:

    def __init__(self,x=400,y=400):

        self.item_dir = {
            "sparkle" : DIR+"pickup/spark/"
        }
        self.item_frames = {}

        self.x = x
        self.y = y

        self.curr_frame = 0
        self.curr_anim = 0

        self.populate_items()

    def populate_items(self):

        for key in self.item_dir:

            self.get_frames(key,self.item_dir[key])
    
    def get_frames(self,key,dir):

        frames = os.listdir(dir)

        self.item_frames[key] = []

        for i in frames:
            
            self.item_frames[key].append(dir+i)


        

    def move(self,coord,face):
        
        self.x = coord[0]
        self.y = coord[1]
        self.face = face

    def return_xy(self):
        print(self.x)
        return (self.x,self.y)

    def animate(self,item_img,curr_frame):
        
        new_frame = curr_frame+1
        
        try:
            re = item_img[new_frame] 

        except IndexError:

            new_frame = 0
            re = item_img[0]

        return (pygame.image.load(re),new_frame)

    def return_frames(self):
        return self.item_frames

    def return_self(self):

        return self






