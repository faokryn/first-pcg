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
        self.buildBlankLevel()
        self.placeExits()
        self.placeRooms()
        
    def buildBlankLevel(self):
        self.level.update({ (i,j):Cell(i,j)
                            for i in range(self.width)
                            for j in range(self.height)
                          })

    def placeExits(self):
        sides = ['N', 'S', 'W', 'E']
        random.shuffle(sides)
        sides = random.sample(sides, 2)

        if sides[0] == 'N':
            x = random.randrange(1, self.width-1)
            self.level.update({(x, 0):Start(x, 0)})
        elif sides[0] == 'S':
            x = random.randrange(1, self.width-1)
            self.level.update({(x, self.height-1):Start(x, self.height-1)})
        elif sides[0] == 'W':
            y = random.randrange(1, self.height-1)
            self.level.update({(0, y):Start(0, y)})
        elif sides[0] == 'E':
            y = random.randrange(1, self.height-1)
            self.level.update({(self.width-1, y):Start(self.width-1,y)})

        if sides[1] == 'N':
            x = random.randrange(1, self.width-1)
            self.level.update({(x, 0):Finish(x, 0)})
        elif sides[1] == 'S':
            x = random.randrange(1, self.width-1)
            self.level.update({(x, self.height-1):Finish(x, self.height-1)})
        elif sides[1] == 'W':
            y = random.randrange(1, self.height-1)
            self.level.update({(0, y):Finish(0, y)})
        elif sides[1] == 'E':
            y = random.randrange(1, self.height-1)
            self.level.update({(self.width-1, y):Finish(self.width,y)})

    def placeRooms(self):
        # Set the mean and standard deviation of room size distribution
        mu_size = 8
        sd_size = 2

        # Determine mean and standard deviation of room number distribution
        mu_rooms = (self.height * self.width)//mu_size**2
        sd_rooms = 1

        # generate rooms
        rooms = [   (int(random.gauss(mu_size, sd_size)),
                    int(random.gauss(mu_size, sd_size)))
                    for i in range(int(random.gauss(mu_rooms, sd_rooms)))
                ]


        # place rooms
        failCount = 0
        while rooms != []:
            # get a random room from the list
            random.shuffle(rooms)
            room = rooms.pop()

            # determine corner
            x_corner = random.randrange(1, self.width - room[0])
            y_corner = random.randrange(1, self.height - room[1])

            # # check that the room can fit there
            placeable = True
            for i in range(x_corner, x_corner+room[0]):
                for j in range(y_corner, y_corner+room[1]):
                    if  isinstance(self.level[(i,j)], Wall) or \
                        isinstance(self.level[(i,j)], Room):
                        placeable = False

            if placeable == True:
                # place the room
                self.level.update({ (i,j):Room(i,j)
                            for i in range(x_corner, x_corner+room[0])
                            for j in range(y_corner, y_corner+room[1])
                         })
                # reset failCount
                print("Failures during this placement: ", failCount)
                print("Rooms still to be printed:\n", rooms)
                print("\n")
                failCount = 0
            else:
                # put the room back in the list
                rooms.append(room)
                # increment failCounter
                failCount += 1

            if failCount > 10:
                print("ERROR: Failed to place room 10 times!")
                print("Room failed on: ", room)
                print("Rooms still to be printed:\n", rooms)
                rooms = []


    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.level[(i,j)])
                                        for i in range(self.width)
                                    ])
                                        for j in range(self.height)
            ]) + "\n"

