import pygame
import sys
import pygame.freetype
import character
import items
import event
import moviepy
from moviepy.editor import *
EVENT = event.event()
chara = character.Character()
item = items.Item()

config = {
    "name": "Nothing",
    "dimensions": (800, 800),
    "background": None
}


class Scenes:

    def __init__(self):

        pygame.init()        
        
        self.title = "YET TO BE DETERMINED"
        
        # Window name configuration 
        self.eng_conf = config
        self.name = self.eng_conf["name"]
        self.width, self.height = self.eng_conf["dimensions"]# Window height,width
        
        #-----FPS/Clock
        self.fps = 60
        self.clock = pygame.time.Clock()
        
        #-----Scene selection
        self.scene = 0
        self.scene_started = False

        #-----Pygame surface stuff
        self.screen = pygame.display.set_mode((self.height,self.width))
        self.display = pygame.display
        self.display.set_caption(self.name)

        

        #________ Menu configuration _________#
        
        #-----Font options for title
        self.title_text = pygame.freetype.Font(
            'resources/fonts/256BYTES.ttf', 80)
        self.options = pygame.freetype.Font('resources/fonts/256BYTES.ttf', 60)
        #----- Menu select colors in RGB
        
        self.menu_current_select = 0
        self.menu_selected = (255, 255, 255)
        self.menu_unselected = (255, 0, 0)
        
        
        #_______ First scene / Character init _______#
        
        
        #-----Background image reference and pygame image load reference 
        # (not set until first scene)
        self.background_image = None
        self.game_bg = None
        
        
        #-----Player Character
        # Main character image always 1 of 2 frames
        # self.chara is a direct reference to Character class' self 
        # Like above image is directly referenced (1 of 2) and then loaded later
        
        self.chara = chara.return_self()
        self.character_img = self.chara.chara_frames
        self.character_load = None
        
        #-----Character frames for animation later
        self.ch_frame = 0
        self.ch_anim = 0
        
        #-----Item class reference, load is an array since -
        # - item frames are not always predictable, and cannot be hardcoded 
        self.items = item.return_self()
        self.items_load = []
        
        #-----Item frames for animation later 
        self.item_frame = 0 
        self.item_anim = 0
        self.menu_play = True
        self.scene_done = False
        self.level_music = True
    # ______ Scene starter _____#
    
    # - This is a simple scene selector
    # - Later, in the start function, once self.scene is greater than current scene -
    # - The game loop will stop, then pass self.scene to this function
    # - This function will pick the scene based on what's passed to it. 
    # - This is good for later, since we can easily save certain parts of the game state
    # - based on what is being passed to this function
    # - later, items, xp, and other values can be saved to a file 
    
    def start_scene(self, scene):
        
        # self.scene will always be set to the scene that is passed here
        
        self.scene = scene

        # Simple control, which will pick the scene based on the number passed to the function
        
        if self.scene == 0:
            
            
            if self.menu_play:
              
                pygame.mixer.music.load("resources/sound/menu/menu_mu.wav")
                pygame.mixer.music.play(-1)
                self.menu_play = False
                
            self.scene_title()
            
        # This is here so that the character image will load after the title,
        # but set_img() won't run every iteration of the game loop
        # scene_started is set to False here so that it won't run every iteration
        
        if self.scene > 1 and self.scene_started:
            
            self.set_img()
            self.scene_started = False

        if self.scene == 2:
            if self.level_music:
                pygame.mixer.music.load("resources/sound/scn_2_music/sc_2.wav")
                pygame.mixer.music.play(-1)
                self.level_music = False

            self.scene_two()
            
    # _____ Title Scene _____#
    
    
    # - Kind of a pain in the ass but it works 
    # - This is the first scene rendered by the scene function above
    # - Later on I'll add some music once I get around to actually working on some 
    
    def scene_title(self):

        # We want the screen to be black, despite the default bg being black
        self.screen.fill((0, 0, 0))

        # Rendering all the menu text. Obviouly the title would be bigger
        title = self.title_text.render(
            self.title, (255, 0, 0))[0]
        
        start = self.options.render("START", self.menu_selected)[0]
        quitq = self.options.render("QUIT", self.menu_unselected)[0]

        # Hard coded positioning because I'm a lazy person and don't care 
        self.screen.blit(title, (55, 250))
        self.screen.blit(start, (330, 350))
        self.screen.blit(quitq, (350, 420))

        # Key event handler to either start or close the game
        # - This also highlights the text you're selecting currently by changing the color to white
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                ef = pygame.mixer.Sound('resources/sound/menu/menu.wav')
                ef.play()
                if event.key == pygame.K_DOWN:
                    if self.menu_current_select == 0:
                        self.handle_menu_key_event(1, 255, 0)
                    else:
                        self.handle_menu_key_event(0, 0, 255)
                if event.key == pygame.K_UP:
                    if self.menu_current_select == 1:
                        self.handle_menu_key_event(0, 0, 255)
                    else:
                        self.handle_menu_key_event(1, 255, 0)
                if event.key == pygame.K_RETURN:
                    if self.menu_current_select == 1:
                        sys.exit()
                    else:
                        self.scene_started = True
                        self.scene = 1
                        self.screen.fill((0, 0, 0))
                        self.display.update()

    # Function for handling key events in the menu 
    def handle_menu_key_event(self, arg0, arg1, arg2):
        self.menu_current_select = arg0
        self.menu_unselected = 255, arg1, arg1
        self.menu_selected = 255, arg2, arg2
        
    def scene_one(self):
        
        clip = VideoFileClip('resources/video/sc_1/sc_1.mp4')
        clip.preview()
        clip.close()
        self.scene_done = True
        return print("done")
      
        
    def scene_two(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        if self.item_frame % 4 == 0:
            
            self.items_load, self.item_frame = chara.animate(
                self.items.item_frames["sparkle"], self.item_anim)
            self.item_anim = self.item_frame

        if self.ch_frame % 60 == 0:
            
            self.character_load, self.ch_frame = chara.animate(
                self.character_img, self.ch_anim)
            self.ch_anim = self.ch_frame

        self.screen.blit(self.game_bg, (0, 0))
        self.screen.blit(self.items_load, (0, 0))

        EVENT.key_event(self.chara, self.fps,pygame.key.get_pressed())
        
        if chara.face == "r":
            self.screen.blit(
                pygame.transform.flip(self.character_load, True, False),
                self.chara.return_xy())
        else:
            self.screen.blit(self.character_load, self.chara.return_xy())

        
        # self.tbox = EVENT.text_box()
        # self.tbox = pygame.transform.scale(self.tbox, (700,700))
        # self.screen.blit(self.tbox,(50,100))

        self.ch_frame += 1
        self.item_frame += 1






    def set_img(self):

        if self.eng_conf["background"] is None:
            self.background_image = "resources/background/def_bg.jpg"
        else:
            self.background_image = self.eng_conf["background"]

        self.items_load = pygame.image.load(self.items.item_frames["sparkle"][0])
        self.game_bg = pygame.image.load(self.background_image)


        self.game_bg = pygame.transform.scale(
            self.game_bg, (self.width, self.height))
        
        self.character_load = pygame.image.load(
            self.character_img[0])










    def Start(self):

        current_scene = self.scene
        if self.scene == 1:
            self.scene_one()
            if self.scene_done:
                self.scene = 2
                return self.Start()
            
        while 1:

            self.start_scene(self.scene)

            if self.scene > current_scene:
                
                return self.Start()
            
            self.display.update()
            self.clock.tick(self.fps)

