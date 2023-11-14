# This file was created by Bradley Kemp:
# Content from Chris Bradfield tutorials content from kids can code: http://kidscancode.org/blog/
# Lines of coded assisted by Group 1 (ex. Alan)
# Huge help from Isaiah Garcia '25 and Will Goodman '26
# Help from tutorial videos by ShawCode: https://www.youtube.com/@ShawCode
# Sound effects from pixabay.com

# Game Design:
# Avoid being touched by mobs --> Death
# Collect coins
# Once coins are collected, add more
# Have coin count, include high score
# Have a gameover screen
# Be able to reset the game

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math


vec = pg.math.Vector2

# Setup asset folders here - images, sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # Init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.coin_collect = pg.mixer.Sound(os.path.join(snd_folder, 'coin_collect.wav'))
        self.death_sound = pg.mixer.Sound(os.path.join(snd_folder, 'death_sound.mp3'))
        # Image used for my gameover screen
        # gameover_bg = pg.image.load(os.path.join(img_folder, 'gameover_bg.png')).convert()
        pg.display.set_caption("Bradley's Game")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self): 
        # Sets score to 0, but will be updated later
        self.score = 0
        self.level = 0
        self.bgimage = pg.image.load(os.path.join(img_folder, "sky_bg.png")).convert()
        # Puts groups into category, sprite
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # Instantiate classes
        self.playerOne = Player(self)
        # self.playerTwo = PlayerTwo(self)
        # Add instances to groups
        self.all_sprites.add(self.playerOne)
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)
        # self.all_sprites.add(self.playerTwo)

        for p in PLATFORM_LIST:
            # Instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        # Generates mobs in a random range, one to eight
        for m in range(0,7):
            # Each mob has a separate position, randomly determined
            m = Mob(self, randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        
        self.run()
    
    def run(self):
        self.playing = True
        self.coin_spawn()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    # I tried to add a gameover screen and reset button; it didn't work --> I'll solve it later

    # def game_over(self):
    #     text = self.draw_text("Game Over", 30, WHITE, WIDTH/2, HEIGHT/10)
    #     restart_button = Button(10, WIDTH/2, HEIGHT/10, 120, 50, WHITE, BLACK, 'Restart', 32)

    #     for Sprite in self.all_sprites:
    #         Sprite.kill()

    #     while self.running:
    #         for event in pg.event.get():
    #             if event.type == pg.QUIT:
    #                 self.running = False

    #         mouse_pos = pg.mouse.get_pos()
    #         mouse_pressed = pg.mouse.get_pressed()

    #         if restart_button.is_pressed(mouse_pos, mouse_pressed):
    #             self.new()
    #             self.main()

    #         self.screen.blit(self.gameover_bg (0,0))
    #         self.screen.blit(text, self.text_rect)
    #         self.screen.blit(restart_button.image, restart_button.rect)
    #         self.clock.tick(FPS)
    #         pg.display.update()

        # This is what prevents the player from falling through the platform when falling down.
        hits = pg.sprite.spritecollide(self.playerOne, self.all_platforms, False)
        if hits:
            if self.playerOne.vel.y > 0:
                self.playerOne.pos.y = hits[0].rect.top
                self.playerOne.vel.y = 0
                print(self.playerOne.vel.y)
                print(self.playerOne.acc.y)
            elif self.playerOne.vel.y < 0:
                self.playerOne.vel.y = -self.playerOne.vel.y
            
        # Checks to see if player collides specifically with the ground and sets him on top of it
        ghits = pg.sprite.collide_rect(self.playerOne, self.ground)
        if ghits:
            self.playerOne.pos.y = self.ground.rect.top
            self.playerOne.vel.y = 0
        
        if len(self.all_coins) == 0:
            self.coin_spawn()
            self.level += 2
        # Sets coin collision
        coinhits = pg.sprite.spritecollide(self.playerOne, self.all_coins, True)
        if coinhits:
            self.score += 10
            self.coin_collect.play()

        # Sets mob collision
        mobhits = pg.sprite.spritecollide(self.playerOne, self.all_mobs, True)
        if mobhits:
            # Colliding with a mob results in a life lost
            self.playerOne.health -= 1
            self.death_sound.play()
            # If you have 0 lives, reset the game.
            if self.playerOne.health == 0:
                self.playing = False
                # pg.quit()

        # More code for a second player:
         
        # if self.playerTwo.vel.y >= 0:
        #     hits = pg.sprite.spritecollide(self.playerTwo, self.all_platforms, False)
        #     if hits:
        #         self.playerTwo.pos.y = hits[0].rect.top
        #         self.playerTwo.vel.y = 0
        #         self.playerTwo.vel.x = hits[0].speed*1.5
        #  # this prevents the player from jumping up through a platform
        # elif self.playerTwo.vel.y <= 0:
        #     hits = pg.sprite.spritecollide(self.playerTwo, self.all_platforms, False)
        #     if hits:
        #         self.playerTwo.acc.y = 5
        #         self.playerTwo.vel.y = 0
        #         print("ouch")
        #         self.score -= 1
        #         if self.playerTwo.rect.bottom >= hits[0].rect.top - 1:
        #             self.playerTwo.rect.top = hits[0].rect.bottom
                    
    # Sets coin spawns, random locations and random amount
    def coin_spawn(self):
        for c in range(0,10 + self.level):
            c = Coin(self, randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            self.all_sprites.add(c)
            self.all_coins.add(c)

    def events(self):
        for event in pg.event.get():
        # Check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bgimage, (0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Health: " + str(self.playerOne.health), 35, BLACK, WIDTH/2 + 100, 370)
        self.draw_text("Score: " + str(self.score), 35, BLACK, WIDTH/2 - 100, 370)
        # self.draw_text("Hitpoints: " + str(self.playerTwo.hitpoints), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    # Creates a parameter for draw_text
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial bold')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()
