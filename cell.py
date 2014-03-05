################################################################################
#   Procedural Content Generation Game, name TBD
#
#   Author: Colin O'Neill   faokryn@gmail.com
#   github.com/Faokryn/1stPGC
#
#   cell.py
#   Defines the Cell class and its subclasses
################################################################################

import random

class Cell:
#   The Cell class is the superclass of all other cell classes.  It represents a
#   single cell on the level.  By itself, it represents a blank or "open space" 
#   cell
#   
#   Fields:
#       x (int):    The x coordinate of the cell on the level
#       y (int):    The y coordinate of the cell on the level
#
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return u"\u2591"

class Wall(Cell):
#   The wall class is a subclass of the Cell class.  It represents a wall on the
#   level.  By itself, it represents a wall that cannot be destroyed by the
#   player.  These walls will be used around the outer edge of each level.
    def __str__(self):
        #return u"\u2588"
        return u"\u2593"

class DestructableWall(Wall):
#   The DestructableWall class is a subclass of the Wall class.  It represents a
#   wall that can be damaged by the player.  These walls will be used inside of
#   each level.
    def __init__(self, x, y):
        super(DestructableWall, self).__init__(x, y)
        self.hp = 1000
    def __str__(self):
        return u"\u2591"

########################
#   START AND FINISH   #
########################

class Start(Cell):
#   The Start class represents the starting place for the player on the level.
    def __str__(self):
        return "S"

class Finish(Cell):
#   The Finish class represents the goal or exit for the player on the level.
    def __str__(self):
        return "F"

##################
#   OPEN SPACE   #
##################

class Room(Cell):
    def __str__(self):
        return "R"
        
        