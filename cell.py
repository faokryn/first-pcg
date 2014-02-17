################################################################################
#   Procedural Content Generation Game, name TBD
#
#   Author: Colin O'Neill   faokryn@gmail.com
#   github.com/Faokryn/1stPGC
#
#   cell.py
#   Defines the Cell class and its subclasses
################################################################################


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
        return " "

class Wall(Cell):
#   The wall class is a subclass of the Cell class.  It represents a wall on the
#   level.
    def __str__(self):
        return u"\u2588"