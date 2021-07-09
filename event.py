import pygame, character

DIR = "resources/"


class event:

    def __init__(self):

        self.width = 800
        self.height = 800

        self.textbox = "resources/screen/textbox.png"
    
    def key_event(self,chara,fps,keys):

        pos = [chara.x,chara.y]

        speed = chara.speed / fps * fps
        if  keys[pygame.K_LEFT]:

            if pos[0] <= 1:

                pos[0] = pos[0]
            else:
                pos[0] -= 1 * speed
                
            chara.move(pos,"l")

        if  keys[pygame.K_RIGHT]:

            if pos[0] >= self.width:
                
                pos[0] = self.width 
                
            else:
                pos[0] += 1 * speed
                
            chara.move(pos,"r")

        if  keys[pygame.K_UP]:

            if pos[1] <= 1:

                pos[1] = 3
            else:
                pos[1] -= 1 * speed
                
            chara.move(pos,chara.face)

        if  keys[pygame.K_DOWN]:

            if pos[1] >= self.height:

                pos[1] = self.height - 3
            else:
                pos[1] += 1 * speed

            chara.move(pos,chara.face)
    
    def text_box(self):

            return pygame.image.load(self.textbox)





