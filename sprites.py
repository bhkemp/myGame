# This file was created by Bradley Kemp:

import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *

# Setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # Makes self.game into game for convenience purposes
        self.game = game
        # An image for player
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # Sets attributes, like health and score, but also velocity and acceleration
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 3
        self.score = 0
    # Defines the controls, setting different movements to keys
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        ghits = pg.sprite.collide_rect(self, self.game.ground)
        # Code also featured in main.py
        if hits or ghits:
            print("I can jump!")
            self.vel.y = -PLAYER_JUMP
        # Same code, but self must be added before "game.all_coins" to connect main.py and sprites.py
        coinhits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if coinhits:
            self.score += 10
        mobhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if mobhits:
            self.health -= 1
            if self.health == 0:
                self.game.playing = False
                # pg.quit()
        
    def update(self):
        # CHECKING FOR COLLISION WITH MOBS HERE>>>>>
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # If friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # Allows player to never go off screen: If he leaves on one side, appear on the other
        if self.rect.x > WIDTH:
            self.pos.x = 0
        if self.rect.right < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

# Add back in if you want a second player; adjust code if necessary:
# class PlayerTwo(Sprite):
#     def __init__(self, game):
#         Sprite.__init__(self)
#         # self.image = pg.Surface((50, 50))
#         # self.image.fill(GREEN)
#         # use an image for player sprite...
#         self.game = game
#         self.image = pg.image.load(os.path.join(img_folder, 'theBigBellTwo.png')).convert()
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.center = (0, 0)
#         self.pos = vec(WIDTH/2, HEIGHT/2)
#         self.vel = vec(0,0)
#         self.acc = vec(0,0)
#         self.hitpoints = 100
#     def controls(self):
#         keys = pg.key.get_pressed()
#         if keys[pg.K_LEFT]:
#             self.acc.x = -5
#         if keys[pg.K_RIGHT]:
#             self.acc.x = 5
#         if keys[pg.K_UP]:
#             self.jump()
#     def jump(self):
#         hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
#         if hits:
#             print("i can jump")
#             self.vel.y = -PLAYER_JUMP
#     def update(self):
#         # CHECKING FOR COLLISION WITH MOBS HERE>>>>>
#         self.acc = vec(0,PLAYER_GRAV)
#         self.controls()
#         # if friction - apply here
#         self.acc.x += self.vel.x * -PLAYER_FRIC
#         # self.acc.y += self.vel.y * -0.3
#         # equations of motion
#         self.vel += self.acc
#         self.pos += self.vel + 0.5 * self.acc
#         if self.rect.x > WIDTH:
#             self.pos.x = 0
#         if self.rect.right < 0:
#             self.pos.x = WIDTH
#         self.rect.midbottom = self.pos

# This would be for my gameover screen:
# class Button:
#     def __init__(self, x, y, width, height, fg, bg, content, fontsize):
#         self.font = pg.font.Font('arial.ttf', fontsize)
#         self.content = content
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.fg = fg
#         self.bg = bg

#         self.image = pg.Surface((self.width, self.height))
#         self.image.fill(self.bg)
#         self.rect = self.image.get_rect()

#         self.rect.x = self.x
#         self.rect.y = self.y

#         self.text = self.font.render(self.content, True, self.fg)
#         self.text_rect = self.text.get_rect(WIDTH/2, HEIGHT/2)
#         self.image.blit(self.text, self.text_rect)

#     def is_pressed(self, pos, pressed):
#         if self.rect.collidepoint(pos):
#             if pressed[0]:
#                 return True
#             return False
#         return False

class Coin(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        # An image for coins
        self.image = pg.image.load(os.path.join(img_folder, 'aCoin.png')).convert()
        self.image.set_colorkey(BLACK)
        # Same as Player, self.rect.x = x to be convenient
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)

class Platform(Sprite):
    # Sets a parameter for Platform
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        # Since there isn't an image, defining width, height, and color will create a Platform:
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHTWHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        # Creates a category, "moving"
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            # Makes the platform never go off screen: If it reaches a border, set the speed to negative
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        # An image for mobs
        self.image = pg.image.load(os.path.join(img_folder, 'theLancer.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
    # This is "seeking": has mobs follow the player
    def update(self):
        # i.e., if the mob is on the right, increase self.rect.x (right)
        if self.rect.x < self.game.playerOne.rect.x:
            self.rect.x +=1
        if self.rect.x > self.game.playerOne.rect.x:
            self.rect.x -=1
        if self.rect.y < self.game.playerOne.rect.y:
            self.rect.y +=1
        if self.rect.y > self.game.playerOne.rect.y:
            self.rect.y -=1