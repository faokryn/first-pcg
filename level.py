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
    
    MIN_WALL_LEN = 3

    def __init__(self, width, height):
        self.width, self.height, self.level, self.rooms = width, height, {}, []
        self.buildBlankLevel()
        self.placeRooms()
        
    def buildBlankLevel(self):
        self.level.update({ (i,j):Cell(i,j)
                            for i in range(self.width+2)
                            for j in range(self.height+2)
            })
        self.level.update({ (i,j):Wall(i,j)
                            for i in range(self.width+2)
                            for j in [0, self.height+1]
            })
        self.level.update({ (i,j):Wall(i,j)
                            for i in [0, self.width+1]
                            for j in range(self.height+2)
            })

    def placeRooms(self):
        x_cur = 1
        y_cur = 1
        room_num = 0
        while y_cur < self.height - 1:
            if  isinstance(self.level[(x_cur, y_cur)], Wall) or \
                isinstance(self.level[(x_cur, y_cur)], Room):
                if x_cur == self.width:
                    x_cur = 1
                    y_cur += 1
                else:
                    x_cur += 1
            else:
                self.placeRoom(x_cur, y_cur, room_num)
                room_num += 1
                if x_cur == self.width:
                    x_cur = 1
                    y_cur += 1
                else:
                    x_cur += 1


    def placeRoom(self, x_cur, y_cur, room_num):
        # Determine width
        #################
        # find available width
        x = x_cur
        while x < self.width + 1:
            if isinstance(self.level[(x, y_cur)], Wall) \
            or isinstance(self.level[(x, y_cur)], Room):
                break
            x += 1
        available_width = x - x_cur

        # set room width based on available width
        room_width = 0
        if available_width < 2*self.MIN_WALL_LEN + 1:
            room_width = available_width
        else:
            while room_width < self.MIN_WALL_LEN \
            or room_width > available_width - (self.MIN_WALL_LEN + 1):
                room_width = random.choice([3,3,4,4,4,5,5,5,5,6,6,6,7,7,8])

        # Determine height
        ##################

        y = y_cur
        while y < self.height + 1:
            if isinstance(self.level[(x_cur, y)], Wall) \
            or isinstance(self.level[(x_cur, y)], Room):
                break
            y += 1
        available_height = y - y_cur

        room_height = 0
        if available_height < 2*self.MIN_WALL_LEN + 1:
            room_height = available_height
        else:
            while room_height < self.MIN_WALL_LEN \
            or room_height > available_height - (self.MIN_WALL_LEN + 1):
                room_height = random.choice([3,3,4,4,4,5,5,5,5,6,6,6,7,7,8])


        print("\nRoom width", room_width, "\nRoom Height: ", room_height)
        # Add room to level
        ###################
        # add room
        self.level.update({ (i,j):Room(i,j,room_num)
                            for i in range(x_cur, x_cur + room_width)
                            for j in range(y_cur, y_cur + room_height)
            })
        # add walls
        self.level.update({ (i,j):Wall(i,j)
                            for i in range(x_cur - 1, x_cur + room_width + 1)
                            for j in [y_cur-1, y_cur+room_height]
                            if not isinstance((i,j), Wall)
            })
        self.level.update({ (i,j):Wall(i,j)
                            for i in [x_cur-1, x_cur+room_width]
                            for j in range(y_cur - 1, y_cur + room_height + 1)
                            if not isinstance((i,j), Wall)
            })
        self.rooms.append(( room_num, (x_cur,y_cur), (room_width,room_height) ))
        print(self)

    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.level[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"

