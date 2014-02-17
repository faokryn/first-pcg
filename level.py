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
        #   Generate the north and south walls
        self.level = {  (i, j):Wall(i, j)
                        for i in range(width+2)
                        for j in [0, height+1]
                     }
        # Generate the east and west walls
        self.level.update({ (i,j):Wall(i, j)
                            for i in [0, width+1]
                            for j in range(height+2)
                         })
        # Fill the center wil empty cells
        self.level.update({ (i,j):Cell(i, j)
                            for i in range(1, width+1)
                            for j in range(1, height+1)
                         })


    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.level[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"

