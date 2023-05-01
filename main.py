import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # Creating the window
pygame.display.set_caption("Fucking Bird")
# Load images of the bird
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
BACKGROUND_IMG = bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 800))

class Bird:
    """
    Bird class representing the flappy bird
    """
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # How much the bird is going to tilt
    ROT_VEL = 20 # How much we are going to rotate on each frame
    ANIMATION_TIME = 5 # How long we are going to show each bird animation

    def __init__(self,x,y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
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
        """make the bird jump
        :return: None"""
        self.vel = -10.5 # Negative velocity because the top left corner is (0,0)
        #negative velocity means going up
        self.tick_count = 0 # When we last jumped, resetting this at each jump
        self.height = self.y # Where the bird is starting
    
    #move is called every single frame, as bird keeps moving
    def move(self): 
        """make the bird move
        :return: None"""
        self.tick_count += 1 # How many times we moved since the last jump
        #below equation is most important, understand it carefully
        #for downward acceleration
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
        """draw the bird
        :param win: pygame window or surface
        :return: None"""
        #win = window
        self.img_count += 1 # How many times we showed the same image
        #changing the image of the bird
        if self.img_count <= self.ANIMATION_TIME: # If we didn't show the same image for too long
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2: 
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3: 
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4: 
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*4 + 1: 
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
        """gets the mask for current image of the bird
        :return: None"""
        return pygame.mask.from_surface(self.img)
class Pipe:
    """represent a pipe object"""
    GAP = 200 # Space between the pipes
    VEL = 5 # How fast the pipes are moving
    #since our bird doesn't move, we move the pipes
    def __init__(self,x):
        """
        initialize pipe object
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        #height of tubes is random
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True) # Flipping the pipe image
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()
    def set_height(self):
        """set the height of the pipe, from the top of the screen
        :return: None"""
        #get a random number for where our pipe should be
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    def move(self):
        self.x -= self.VEL
    def draw(self,win):
        """draw both the top and bottom of the pipe
        :param win: pygame window or surface
        :return: None"""
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    #defining collision
    #mask is used to define the pixels of the image, inplace of using hit-boxes
    def collide(self,bird,win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP) # Mask for the top pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # Mask for the bottom pipe

        #now we need to calculate the offset- how far away the masks are from each other
        #offset is a tuple
        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point:
            return True
        return False
    
class Base:
    VEL = 5 # Same velocity as the pipes
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG
    def __init__(self,y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        #if the first image is off the screen, we move it to the back
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        #if the second image is off the screen, we move it to the back
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self,win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))

def draw_window(win,bird, pipes, base):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    #blit is used to draw something on the screen
    win.blit(BACKGROUND_IMG,(0,0))
    #drawing the pipes
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win) # Drawing the bird on the window
    pygame.display.update()

def main():
    bird = Bird(230,500) #optimal position for the bird
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    base = Base(600)
    pipes = [Pipe(480),Pipe(900),Pipe(1500),Pipe(2000)]
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        #keep track on events, if we quit the game,we exit the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #bird.move()
        base.move()
        for pipe in pipes:
            #check for collision with the bird
            pipe.move()
        draw_window(WIN,bird,pipes,base)

if __name__ == "__main__":
    main()