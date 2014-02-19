import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Dragon(GameElement):
    IMAGE = "PurpleDragon"
    SOLID = True

class Character(GameElement):
    IMAGE = "Cat"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []


#def movement of our character, which is called down below
    def next_pos(self, direction):
        if direction == "up":
            return(self.x, self.y-1)
        elif direction == "down":
            return(self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Horns(GameElement):
    IMAGE = "Horns"
    SOLID = True
    def interact(self, player):
        GAME_BOARD.draw_msg("Welcome to Water World. Beware, there be dragons here!")

class BlueGem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

class GreenGem(GameElement):
    IMAGE = "GreenGem"
    SOLID = False

    def interact (self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

class OrangeGem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(0, 0, PLAYER)
        GAME_BOARD.draw_msg("That's hot! Start over!")


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
            (random.randint(1,9), random.randint(1,9)),
            (random.randint(1,9), random.randint(1,9)),
            (random.randint(1,9), random.randint(1,9)),
            (random.randint(1,9), random.randint(1,9))
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
    rocks[-1].SOLID = False    


    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()    
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 0, PLAYER)
    print PLAYER

    gemb = BlueGem()
    GAME_BOARD.register(gemb)
    GAME_BOARD.set_el(3, 1, gemb)

    gemg = GreenGem()
    GAME_BOARD.register(gemg)
    GAME_BOARD.set_el(3, 3, gemg)

    gemo = OrangeGem()
    GAME_BOARD.register(gemo)
    GAME_BOARD.set_el(8, 8, gemo)

    horns = Horns()
    GAME_BOARD.register(horns)
    GAME_BOARD.set_el(1, 0, horns)

    pdragon = Dragon()
    GAME_BOARD.register(pdragon)
    GAME_BOARD.set_el(1, 4, pdragon)


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"

    if KEYBOARD[key.DOWN]:
        direction = "down"

    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if KEYBOARD[key.LEFT]:
        direction = "left"
        
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
        if next_x > 9 or next_x < 0:
            next_x = PLAYER.x
        elif next_y > 9 or next_y <0:
            next_y = PLAYER.y
        else:    
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)


            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)

    if KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()

    
