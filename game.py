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

class Fire(GameElement):
    IMAGE = "Fire"

class Character(GameElement):
    IMAGE = "Cat"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.key = []
        self.heart = []


   
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
        if len(player.heart) == 1:
            dragon = Dragon()
            GAME_BOARD.register(dragon)
            GAME_BOARD.set_el(1, 0, dragon)
            GAME_BOARD.draw_msg("Gotcha! You just freed the dragon.  You are dead!")
            fire = Fire()
            GAME_BOARD.register(fire)
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(PLAYER.x, PLAYER.y, fire)

class Chest(GameElement): 
    IMAGE = "Chest"
    SOLID = True
    def interact(self, player):
        if len(player.key) == 1:
            heart = Heart()
            GAME_BOARD.register(heart)
            GAME_BOARD.set_el(8, 0, heart)
         
class Gem(GameElement):   
    SOLID = False
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems!"%(len(player.inventory)))
        if len(player.inventory) == 10:
            mykey = Key()
            GAME_BOARD.register(mykey)
            GAME_BOARD.set_el(0, 0, mykey)
            GAME_BOARD.draw_msg("Now, go get the key!")
            
class BlueGem(Gem):
    IMAGE = "BlueGem"

class GreenGem(Gem):
    IMAGE = "GreenGem"
    

class Tree(GameElement):
    SOLID = True

class TallTree(Tree):
    IMAGE = "TallTree"

class ShortTree(Tree):
    IMAGE = "ShortTree"

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    def interact(self, player):
        player.heart.append(self)
        GAME_BOARD.draw_msg("You won my heart! Now come give me a big kiss!")


class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.key.append(self)
        GAME_BOARD.draw_msg("You found the key! Go open the treasure chest and free my heart!")
    
    
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""



    rocks = [Rock()] * 10
    number_rocks = 0 

    while number_rocks < 10:
        random_x = random.randint(0,9)
        random_y = random.randint(0,9)
        rock = Rock()
        if not GAME_BOARD.get_el(random_x, random_y) and ((random_x, random_y) != (0,1)):
            GAME_BOARD.register(rock)
            GAME_BOARD.set_el(random_x, random_y, rock)
            rocks.append(rock)
            number_rocks += 1

       # rocks[-1].SOLID = False  

    global PLAYER
    PLAYER = Character()    
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 0, PLAYER)
    GAME_BOARD.draw_msg("Collect 10 gems to win my heart! But beware! There be dragons here!")
    print PLAYER

    gemb = [BlueGem()] * 7
    number_gems = 0

    while number_gems < 7:
        random_x = random.randint(0,9)
        random_y = random.randint(0,9)
        gem = BlueGem()
        if not GAME_BOARD.get_el(random_x, random_y):
            GAME_BOARD.register(gem)
            GAME_BOARD.set_el(random_x, random_y, gem)
            gemb.append(gem)
            number_gems += 1

    gemg = [GreenGem()] * 7
    number_gems = 0

    while number_gems < 7:
        random_x = random.randint(0,9)
        random_y = random.randint(0,9)
        gem = GreenGem()
        if not GAME_BOARD.get_el(random_x, random_y):
            GAME_BOARD.register(gem)
            GAME_BOARD.set_el(random_x, random_y, gem)
            gemg.append(gem)
            number_gems += 1

    
    horns = Horns()
    GAME_BOARD.register(horns)
    GAME_BOARD.set_el(1, 0, horns)

    # pdragon = Dragon()
    # GAME_BOARD.register(pdragon)
    # GAME_BOARD.set_el(1, 4, pdragon)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(8, 0, chest)

    talltree = TallTree()
    GAME_BOARD.register(talltree)
    GAME_BOARD.set_el(5, 8, talltree)

    shorttree = ShortTree()
    GAME_BOARD.register(shorttree) 
    GAME_BOARD.set_el(3, 4, shorttree)

    
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

    
