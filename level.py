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
        self.width, self.height, self.level = width, height, {}
        # Fill the center with empty cells
        self.buildBorder()
        self.fillWhitespace()

    def buildBorder(self):
        # Generate the north and south walls
        self.level = {  (i, j):Wall(i,j)
                        for i in range(self.width+2)
                        for j in [0, self.height+1]
                     }
        # Generate the east and west walls
        self.level.update({ (i,j):Wall(i,j)
                            for i in [0, self.width+1]
                            for j in range(self.height+2)
                         })

        # Place Start and Finish cells
        sides = ['N', 'S', 'W', 'E']
        random.shuffle(sides)
        sides = random.sample(sides, 2)

        if sides[0] == 'N':
            x = random.randrange(1, self.width+1)
            self.level.update({(x, 0):Start(x, 0)})
        elif sides[0] == 'S':
            x = random.randrange(1, self.width+1)
            self.level.update({(x, self.height+1):Start(x, self.height+1)})
        elif sides[0] == 'W':
            y = random.randrange(1, self.height+1)
            self.level.update({(0, y):Start(0, y)})
        elif sides[0] == 'E':
            y = random.randrange(1, self.height+1)
            self.level.update({(self.width+1, y):Start(self.width+1,y)})

        if sides[1] == 'N':
            x = random.randrange(1, self.width+1)
            self.level.update({(x, 0):Finish(x, 0)})
        elif sides[1] == 'S':
            x = random.randrange(1, self.width+1)
            self.level.update({(x, self.height+1):Finish(x, self.height+1)})
        elif sides[1] == 'W':
            y = random.randrange(1, self.height+1)
            self.level.update({(0, y):Finish(0, y)})
        elif sides[1] == 'E':
            y = random.randrange(1, self.height+1)
            self.level.update({(self.width+1, y):Finish(self.width+1,y)})


    def fillWhitespace(self):
        self.level.update({ (i,j):Cell(i,j)
                            for i in range(1, self.width+1)
                            for j in range(1, self.height+1)
                            if (i,j) not in self.level
                         })


    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.level[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"

