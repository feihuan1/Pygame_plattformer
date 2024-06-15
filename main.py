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

class Player(pygame.sprite.Sprite):# sprite class handle pixel perfect collitions
    COLOR = (255, 0, 0) 

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0 # how many pixel player move x axis per frame
        self.y_vel = 0 # how many pixel player move y axis per frame
        self.mask = None
        self.direction = "left"
        self.animation_count = 0

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
        self.move(self.x_vel, self.y_vel)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)


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