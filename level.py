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

    def __init__(self, width, height, start=None):
        self.width, self.height, self.map, self.rooms = width, height, {}, []
        self.buildBlankLevel()
        self.placeRooms()
        self.placeExits(start)
        
    def buildBlankLevel(self):
        self.map.update({ (i,j):Cell(i,j)
                            for i in range(self.width+2)
                            for j in range(self.height+2)
            })
        self.map.update({ (i,j):Wall(i,j)
                            for i in range(self.width+2)
                            for j in [0, self.height+1]
            })
        self.map.update({ (i,j):Wall(i,j)
                            for i in [0, self.width+1]
                            for j in range(self.height+2)
            })

    def placeRooms(self):
        x_cur = 1
        y_cur = 1
        room_num = 0
        while y_cur < self.height - 1:
            if  isinstance(self.map[(x_cur, y_cur)], Wall) or \
                isinstance(self.map[(x_cur, y_cur)], Room):
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

        for room in self.rooms: 
            # Determine neighbors: neighbors are saved as a dictionary, with
            # the room number of the neighbor as the key and a list of tuples
            # of the coordinates of the walls between the neighbors as the value
            if room.x != 1:                                 # Check west
                for i in range(room.y, room.y + room.height):
                    if isinstance(self.map[(room.x - 2, i)], Room):
                        neighborNum = self.map[(room.x - 2, i)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (room.x-1, i)
                        )
            if room.x + room.width - 1 != self.width:       # Check east
                for i in range(room.y, room.y + room.height):
                    if isinstance(
                        self.map[(room.x + room.width + 1, i)], Room
                    ):
                        neighborNum = \
                            self.map[(room.x + room.width + 1, i)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (room.x + room.width, i)
                        )
            if room.y != 1:                                 # Check north
                for i in range(room.x, room.x + room.width):
                    if isinstance(self.map[(i, room.y - 2)], Room):
                        neighborNum = self.map[(i, room.y - 2)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (i, room.y - 1)
                        )
            if room.y + room.height - 1 != self.height:     # Check south
                for i in range(room.x, room.x + room.width):
                    if isinstance(
                        self.map[(i, room.y + room.height + 1)], Room
                    ):
                        neighborNum = \
                            self.map[(i, room.y + room.height + 1)].room_num
                        if neighborNum not in room.neighbors:
                            room.neighbors[neighborNum] = []
                        room.neighbors[neighborNum].append(
                            (i, room.y + room.height)
                        )

            # For each neighbor, if there isn't already an entrance, place an
            # entrance randomly (Maybe not at all?)

            for n in room.neighbors:
                hasEntrance = False
                # Check if there is already an entrance to the neigboring room
                for coordinate in room.neighbors[n]:
                    if isinstance(self.map[coordinate], Entrance):
                        hasEntrance = True
                # If there isn't already an entrance, place one randomly
                if not hasEntrance:
                    newEntrance = random.choice(room.neighbors[n])
                    self.map.update({ 
                        newEntrance:Entrance(newEntrance[0],newEntrance[1])
                    })



    def placeRoom(self, x_cur, y_cur, room_num):
        # Determine width
        #################
        # find available width
        x = x_cur
        while x < self.width + 1:
            if isinstance(self.map[(x, y_cur)], Wall) \
            or isinstance(self.map[(x, y_cur)], Room):
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
            if isinstance(self.map[(x_cur, y)], Wall) \
            or isinstance(self.map[(x_cur, y)], Room):
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


        # Add room to level
        ###################
        # add room
        self.map.update({ (i,j):Room(i,j,room_num)
                            for i in range(x_cur, x_cur + room_width)
                            for j in range(y_cur, y_cur + room_height)
            })
        # add walls
        self.map.update({ (i,j):Wall(i,j)
                            for i in range(x_cur - 1, x_cur + room_width + 1)
                            for j in [y_cur-1, y_cur+room_height]
                            if not isinstance((i,j), Wall)
            })
        self.map.update({ (i,j):Wall(i,j)
                            for i in [x_cur-1, x_cur+room_width]
                            for j in range(y_cur - 1, y_cur + room_height + 1)
                            if not isinstance((i,j), Wall)
            })
        self.rooms.append(
            RoomInfo(room_num, x_cur, y_cur, room_width, room_height)
        )

    def placeExits(self, start):
        # place start and finish blocks

        # make sure start is an exceptable value
        if start != 'N' and start != 'S' and start != 'E' and start != 'W' and \
            start != None:
            print("\nERROR: Unacceptable value for start\n")
            raise SystemExit

        # if there isn't a start specified, choose one randomly
        if start == None:
            start = random.choice(['N', 'S', 'W', 'E'])


        if start == 'N':
            # set start block
            x = random.randrange(1, self.width + 1)
            y = 0
            while not isinstance(self.map[x, y+1], Room):
                x = random.randrange(1, self.width + 1)
            self.map.update({ (x,y):Start(x,y) })
            self.start_pos = (x,y)

        elif start == 'S':
            # set start block
            x = random.randrange(1, self.width + 1)
            y = self.height + 1
            while not isinstance(self.map[x, y-1], Room):
                x = random.randrange(1, self.width + 1)
            self.map.update({ (x,y):Start(x,y) })
            self.start_pos = (x,y)

        elif start == 'W':
            # set start block
            x = 0
            y = random.randrange(1, self.height + 1)
            while not isinstance(self.map[x+1, y], Room):
                y = random.randrange(1, self.height + 1)
            self.map.update({ (x,y):Start(x,y) })
            self.start_pos = (x,y)

        elif start == 'E':
            # set start block
            x = self.width + 1
            y = random.randrange(1, self.height + 1)
            while not isinstance(self.map[x-1, y], Room):
                y = random.randrange(1, self.height + 1)
            self.map.update({ (x,y):Start(x,y) })
            self.start_pos = (x,y)


    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.map[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"

class RoomInfo:
    def __init__(self, num, x, y, width, height):
        self.num, self.x, self.y, self.width, self.height, self.neighbors = \
        num, x, y, width, height, {}

    def __str__(self):
        s = "Room " + str(self.num) + " [ (" + str(self.x) + "," + str(self.y) \
            + "); " + str(self.width) + " x " + str(self.height) + " ]"
        return s