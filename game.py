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

GAME_WIDTH = 7
GAME_HEIGHT = 7

class Rock(GameElement):
    IMAGE = "Rock"
    CAN_PASS = True

    def appear(self,x, y):
        GAME_BOARD.register(self)
        GAME_BOARD.set_el(x, y, self)

class Character(GameElement):
    IMAGE = "Girl"

    def next_pos(self,direction):
        if direction == 'up':
            return(self.x, self.y-1)
        elif direction == 'down':
            return (self.x, self.y+1)
        elif direction == 'left':
            return (self.x-1, self.y)
        elif direction == 'right':
            return (self.x+1, self.y)
        return None

    def go_home(self):
        GAME_BOARD.del_el(self.x, self.y)
        GAME_BOARD.set_el(2, 2, self)

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

# class BlueGem(GameElement):
#     IMAGE = 'BlueGem' 
#     CAN_PASS = False

#     def interact(self):
#         player.inventory.append(self)
#         GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

# class OrangeGem(GameElement):
#     IMAGE = 'OrangeGem'
#     CAN_PASS = True

#     def interact(self, player):
#         player.go_home()
#         GAME_BOARD.draw_msg("You just hit a wicked gem. Go back home!") 

class MagicalTree(GameElement):
    IMAGE = 'UglyTree'
    CAN_PASS = False

    def interact(self):
        print "This is the magical tree interact"
        rocks = []
        for i in range(GAME_WIDTH):
            rock = Rock()
            rocks.append(rock)
        for i in range(len(rocks)):
            rocks[i].appear(i,3)
        GAME_BOARD.draw_msg("Use rock for crossing the scary river.")

class RegularTree(GameElement):
    IMAGE = 'ShortTree'
    CAN_PASS = False

    def interact(self):
        print "This is the regular tree interact"
        random_x = random.randint(0,6)
        random_y = random.randint(4,6)

        regular_tree = RegularTree()
        GAME_BOARD.register(regular_tree)
        GAME_BOARD.set_el(random_x, random_y, regular_tree)


class BadTree(GameElement):
    IMAGE = 'TallTree'
    CAN_PASS = True

    def interact(self):
        print "This is the bad tree interact"
        current_x = PLAYER.x
        current_y = PLAYER.y

        horn_player = Character()
        horn_player.IMAGE = 'Horns'

        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.register(horn_player)
        GAME_BOARD.set_el(current_x, current_y, horn_player)
        GAME_BOARD.draw_msg("Oh no! You hit the poison tree! Now you are a horn-person!")

        global PLAYER 
        PLAYER = horn_player

class Water(GameElement):
    IMAGE = 'WaterBlock'
    CAN_PASS = False

    def appear(self,x, y):
        GAME_BOARD.register(self)
        GAME_BOARD.set_el(x, y, self)

def initialize():

### player 

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(3, 2, PLAYER)
    print PLAYER

### rocks

    # rock_positions = None
    #  # [
    #  #     (2,1),
    #  #     (1,2),
    #  #     (3,2),
    #  #     (2,3)
    #  #     ]
    # rocks = []

    # for pos in rock_positions:
    #      rock = Rock()
    #      GAME_BOARD.register(rock)
    #      GAME_BOARD.set_el(pos[0], pos[1], rock)
    #      rocks.append(rock)

    # rocks[-1].CAN_PASS = False

### game board message

#     GAME_BOARD.draw_msg("This game is wicked awesome.")

### gems

#     gem = BlueGem()
#     GAME_BOARD.register(gem)
#     GAME_BOARD.set_el(3, 1, gem)

#     gem2 = OrangeGem()
#     GAME_BOARD.register(gem2)
#     GAME_BOARD.set_el(0, 0, gem2)

### magical trees

    magical_tree = MagicalTree()
    GAME_BOARD.register(magical_tree)
    GAME_BOARD.set_el(6, 1, magical_tree)

### regular trees

    regular_tree = RegularTree()
    GAME_BOARD.register(regular_tree)
    GAME_BOARD.set_el(1, 1, regular_tree)




### bad trees

    bad_tree = BadTree()
    GAME_BOARD.register(bad_tree)
    GAME_BOARD.set_el(4, 2, bad_tree)
    
### water
    water_blocks = []
    for i in range(GAME_WIDTH):
        water_block = Water()
        water_blocks.append(water_block)
    for i in range(len(water_blocks)):
        water_blocks[i].appear(i,3)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = 'down'
    if KEYBOARD[key.RIGHT]:
        direction ='right'
    if KEYBOARD[key.LEFT]:
        direction = 'left'
    if KEYBOARD[key.SPACE]:
        PLAYER.go_home()

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = None

        try:
            existing_el = GAME_BOARD.get_el(next_x, next_y)
        except IndexError:
            existing_el = Water()

        if existing_el:
            existing_el.interact()

        if existing_el is None or existing_el.CAN_PASS:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)