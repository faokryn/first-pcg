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
        self.placeRooms()
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

    def placeRooms(self):
        # determine max height and width
        max_height = self.height//3
        max_width  = self.width//3

        # determine number of rooms
        n = random.randrange(2,14)

        # create a list of n tuples
        rooms = [ (random.randrange(3,max_width+1),
                   random.randrange(3,max_height+1))
                  for k in range(n)
                ]

        # place rooms
        while rooms != []:
            # get a random room from the list
            random.shuffle(rooms)
            room = rooms.pop()

            # determine corner
            x_corner = random.randrange(1, self.width - room[0])
            y_corner = random.randrange(1, self.height - room[1])

            # check that the room can fit there
            placeable = True
            for i in range(x_corner, x_corner+room[0]):
                for j in range(y_corner, y_corner+room[1]):
                    if (i,j) in self.level:
                        placeable = False

            if placeable == True:
                # place the room
                self.level.update({ (i,j):Wall(i,j)
                            for i in range(x_corner, x_corner+room[0])
                            for j in range(y_corner, y_corner+room[1])
                         })
            else:
                # put the room back in the list
                rooms.append(room)


    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.level[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"

