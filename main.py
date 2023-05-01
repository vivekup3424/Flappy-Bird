import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

# Load images of the bird
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))]

GROUND_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))]
BACKGROUND_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))]

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # How much the bird is going to tilt
    ROT_VEL = 20 # How much we are going to rotate on each frame
    ANIMATION_TIME = 5 # How long we are going to show each bird animation

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0 # How much the image is tilted
        self.tick_count = 0 # Physics of the bird
        self.vel = 0 # initial velocity
        self.height = self.y # Where the bird is starting
        self.img_count = 0
        self.img = self.IMGS[0] # Which image of the bird we are starting with

    #function for jumping of the bird
    def jump(self):
        self.vel = -10.5 # Negative velocity because the top left corner is (0,0)
        #negative velocity means going up
        self.tick_count = 0 # When we last jumped, resetting this at each jump
        self.height = self.y # Where the bird is starting
    
    #move is called every single frame, as bird keeps moving
    def move(self): 
        self.tick_count += 1 # How many times we moved since the last jump
        #below equation is most important, understand it carefully
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 # How many pixels we are moving up or down this frame

        #checking terminal velocity
        if d >=16:
            d = 16
        if d < 0: # If we are moving upwards, move a little more, fine tuning our upwards movement
            d -= 2
        self.y += d # Moving the bird up or down

        #tilting the bird
        if d < 0 or self.y < self.height + 50: # If we are moving upwards or we are above the position where we started tilting
            if self.tilt < self.MAX_ROTATION: # If we are not tilted too much
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    def draw(self,win):
        #win = window
        self.img_count += 1 # How many times we showed the same image
        #changing the image of the bird
        if self.img_count < self.ANIMATION_TIME: # If we didn't show the same image for too long
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2: 
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3: 
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4: 
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1: 
            self.img = self.IMGS[0]
            self.img_count = 0
        #if our bird is nosediving, then it can't flap its wing
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    
    #used for collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
def draw_window(win,bird):
    #blit is used to draw something on the screen
    win.blit(BACKGROUND_IMG,(0,0))
    bird.draw(win) # Drawing the bird on the window
    pygame.display.update()
def main():
    bird = Bird(200,200)
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    while True:
        #keep track on events, if we quit the game,we exit the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        bird.move()
        draw_window(WIN,bird)

if __name__ == "__main__":
    main()