import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random
import time

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

class RegularTree(GameElement):
    IMAGE = 'ShortTree'
    CAN_PASS = False

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
            GAME_BOARD.del_el(i,3)
            rocks[i].appear(i,3)
        GAME_BOARD.draw_msg("Use rock for crossing the scary river.")

class MultiplyingTree(RegularTree):

    def interact(self):
        
        tree_count = 0

        while tree_count < 6:
            random_x = random.randint(0,6)
            random_y = random.randint(0,6)

            existing_el = GAME_BOARD.get_el(random_x, random_y)
            
            if existing_el is None:
                regular_tree = RegularTree()
                GAME_BOARD.register(regular_tree)
                GAME_BOARD.set_el(random_x, random_y, regular_tree)
                tree_count += 1
            else:
                continue
        GAME_BOARD.draw_msg("The MULTIPLYING tree! If you run into it too many times, you'll be lost in a forest!")

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
        GAME_BOARD.draw_msg("Oh yes! You hit the special tree! Now you are a horn-person!")

        global PLAYER 
        PLAYER = horn_player

class Water(GameElement):
    IMAGE = 'WaterBlock'
    CAN_PASS = False

    def appear(self,x, y):
        GAME_BOARD.register(self)
        GAME_BOARD.set_el(x, y, self)

    def interact(self):
        GAME_BOARD.draw_msg("Can't get across this river without some stones!")

class Door(GameElement):
    IMAGE = 'DoorClosed'
    CAN_PASS = False

    def interact(self):
        if len(PLAYER.inventory) == 3 and PLAYER.IMAGE == "Horns":
            open_door = Door()
            open_door.IMAGE = 'DoorOpen'
            open_door.CAN_PASS = True

            GAME_BOARD.del_el(self.x, self.y)
            GAME_BOARD.register(open_door)
            GAME_BOARD.set_el(self.x, self.y, open_door)
            GAME_BOARD.draw_msg("You opened the door with all your stoneblocks.")

        elif len(PLAYER.inventory) < 3:
            GAME_BOARD.draw_msg("You're at the door but you need %r more stoneblocks." % (3 - len(PLAYER.inventory)))
        elif PLAYER.IMAGE != "Horns":
            GAME_BOARD.draw_msg("Get yourself some horns! (Hint: find a special tree)")


class StoneBlock(GameElement):
    IMAGE = 'StoneBlock'
    CAN_PASS = False

class PassableStoneBlock(StoneBlock):
    CAN_PASS = True

    def interact(self):
        PLAYER.inventory.append(self)
        GAME_BOARD.draw_msg("You just picked up a special stone.")

def initialize():

### message
    GAME_BOARD.draw_msg("Travel through the enchanted forest to open the door. You have 30 seconds.")
### Girl player 
    girl = Character()
    GAME_BOARD.register(girl)
    GAME_BOARD.set_el(0, 0, girl)
    GAME_BOARD.register_initial(girl,(0,0))

    global PLAYER
    PLAYER = girl

### magical trees
    magical_tree = MagicalTree()
    GAME_BOARD.register(magical_tree)
    GAME_BOARD.set_el(6, 1, magical_tree)
    GAME_BOARD.register_initial(magical_tree,(6,1))

### Multiplying tree
    multiplying_tree = MultiplyingTree()
    GAME_BOARD.register(multiplying_tree)
    GAME_BOARD.set_el(3, 5, multiplying_tree)
    GAME_BOARD.register_initial(multiplying_tree,(3,5))

### bad tree
    bad_tree = BadTree()
    GAME_BOARD.register(bad_tree)
    GAME_BOARD.set_el(2, 1, bad_tree)
    GAME_BOARD.register_initial(bad_tree,(2,1))


### water
    water_blocks = []
    for i in range(GAME_WIDTH):
        water_block = Water()
        water_blocks.append(water_block)
    for i in range(len(water_blocks)):
        water_blocks[i].appear(i,3)
        GAME_BOARD.register_initial(water_blocks[i],(i,3))

### door
    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(6, 6, door)
    GAME_BOARD.register_initial(door,(6,6))

### stoneblocks
    normal_stones = 0
    passable_stones = 0

    while normal_stones < 3:
        random_x = random.randint(2,6)
        random_y = random.randint(1,6)

        existing_el = GAME_BOARD.get_el(random_x, random_y)
        
        if existing_el is None:
            stone_block = StoneBlock()
            GAME_BOARD.register(stone_block)
            GAME_BOARD.set_el(random_x, random_y, stone_block)
            GAME_BOARD.register_initial(stone_block,(random_x, random_y))
            normal_stones += 1
        else:
            continue

    while passable_stones < 3:
        random_x = random.randint(2,6)
        random_y = random.randint(3,6)

        existing_el = GAME_BOARD.get_el(random_x, random_y)
        
        if existing_el is None:
            stone_block = PassableStoneBlock()
            GAME_BOARD.register(stone_block)
            GAME_BOARD.set_el(random_x, random_y, stone_block)
            GAME_BOARD.register_initial(stone_block,(random_x, random_y))
            passable_stones += 1
        else:
            continue

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