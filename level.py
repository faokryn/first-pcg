################################################################################
#   Procedural Content Generation Game, name TBD
#
#   Author: Colin O'Neill   faokryn@gmail.com
#   github.com/Faokryn/1stPGC
#
#   level.py
#   Defines the Level class.
################################################################################

from cell import *
import random

class Level:
#   The level class represents a single level of the game.  It consists of a
#   grid of cells.

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.level = {  (i, j):Wall(i, j)
                        for i in range(width+2)
                        for j in range(height+2)
                    }

    def __str__(self):
        result = "\n"
        j = 0
        while j < self.height+2:
            line = "\t"
            i = 0
            while i < self.width+2:
                line += str( self.level[ (i,j) ] )
                i = i+1
            result += line + "\n"
            j = j+1
        return result