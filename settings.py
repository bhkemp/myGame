# This file was created by: Bradley Kemp
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

# game settings 
WIDTH = 700
HEIGHT = 400
FPS = 30

# player settings
PLAYER_JUMP = 23
PLAYER_GRAV = 1.5
global PLAYER_FRIC
PLAYER_FRIC = 0.2

# define colors
LIGHTWHITE = (227, 227, 227)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Creates platforms using (HEIGHT, WIDTH, x, y, and function)
GROUND = (0, HEIGHT - 40, WIDTH, 40, "normal")
PLATFORM_LIST = [(WIDTH / 2 - 50, HEIGHT / 2 + 10, 100, 20, "moving"),
                 (WIDTH / 2 - 50, HEIGHT / 2 - 130, 100, 20, "moving"),
                 (80, 275, 200, 20,"normal"),
                 (420, 275, 200, 20, "normal"),
                 (80, 150, 200, 20,"normal"),
                 (420, 150, 200, 20, "normal")]