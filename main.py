import os
import random 
import math 
import pygame
from os import listdir 
from os.path import isfile, join

from pygame.sprite import Group

#initialize pygame
pygame.init()
# the title display on top of window
pygame.display.set_caption("Jungle Adventure")

BG_COLOR = (255, 255, 255) # background color
WIDTH, HEIGHT = 1000, 800 # window size
FPS = 60 # frame rate
PLAYER_VEL = 5 # player speed
window = pygame.display.set_mode((WIDTH, HEIGHT)) # store window with size defined above

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] # True is flip X, False is not flip Y

def load_sprite_shets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))] # load every files in dir if it is file

    all_sprites = {} 

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() 

        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height) 
            surface.blit(sprite_sheet, (0,0), rect) 
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace('.png', '') + "_right"] = sprites
            all_sprites[image.replace('.png', '') + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace('.png', '')] = sprites

    return all_sprites

class Player(pygame.sprite.Sprite):# sprite class handle pixel perfect collitions
    COLOR = (255, 0, 0) 
    GRAVITY = 1
    SPRITES = load_sprite_shets("MainCharacters", "PinkMan", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0 # how many pixel player move x axis per frame
        self.y_vel = 0 # how many pixel player move y axis per frame
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        

    def move(self, dx, dy): 
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left" 
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right" 
            self.animation_count = 0

    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self): 
        sprite_sheet = "idle" 
        if self.x_vel != 0:
            sprite_sheet = "run" 

        sprite_sheet_name = sprite_sheet + "_" + self.direction 
        sprite = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprite)
        self.sprite = sprite[sprite_index] 
        self.animation_count+=1
        self.update()
    

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


# generate background
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))# could use a f string as well returns f"assets/Background/{name}"
    
    _, _, width, height = image.get_rect() # object destruction, only get width and height, don't get x,y

    tiles = [] # list of all image position 

    # use window with and hight devide by image with and height get how many image need generate to fill window
    # +1 make sure it covers entire window
    for i in range(WIDTH // width + 1): # // floor the result
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height) # position of image depends on where it should be ,(x, y pos is top left of img)
            tiles.append(pos) # no need explain

    return tiles, image # return as a tuple !!!


# draw background 
def draw(window, background, bg_image, player):
    
    for tile in background:
        window.blit(bg_image, tile)# draw img(loaded img), tile is postion(tuple)

    player.draw(window)

    pygame.display.update()


def handle_move(player): 
    keys = pygame.key.get_pressed()

    player.x_vel = 0 # make sure it will stop when lift the finger

    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)


# this is main function when run the script
def main(window): # pass window in to main function
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png") # get loaded image and all neccesary postion , (destruct tuple)

    player = Player(100, 100, 50, 50)

    run = True

    while run:
        clock.tick(FPS) # make sure while loop is gonna run 60 frames per second (no more than 60, it's like delta time)

        for event in pygame.event.get():#constantly check user events
            # check if user quit the game
            if event.type == pygame.QUIT:
                run = False 
                break
        
        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_image, player)

    
    # if out of while loop, quit the game(deferent than QUIT event)
    pygame.quit()
    quit()# quit the python programe


# if run in this file, run main, else need call main function to run this game(useful if in a arcade game chose menu)
if __name__ == "__main__":
    main(window)