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
        self.placeRoomsTest()
        
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
        # rooms = [   (int(random.gauss(mu_size, sd_size)),
        #             int(random.gauss(mu_size, sd_size)))
        #             for i in range(int(random.gauss(mu_rooms, sd_rooms)))
        #         ]


        # place rooms
        failCount = 0
        while failCount < 50:
            # generate a random room
            room = (int(random.gauss(mu_size, sd_size)),
                    int(random.gauss(mu_size, sd_size)))

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

                # put walls around the room
                # Generate the north and south walls
                self.level.update({ (i, j):Wall(i,j)
                                    for i in range(x_corner, x_corner+room[0]+1)
                                    for j in [y_corner, y_corner+room[1]]
                                })
                # Generate the east and west walls
                self.level.update({ (i,j):Wall(i,j)
                                    for i in [x_corner, x_corner+room[0]]
                                    for j in range(y_corner, y_corner+room[1])
                                })
                # reset failCount
                print("Failures during this placement: ", failCount)
                print("\n")
                failCount = 0
            else:
                # increment failCounter
                failCount += 1

    def placeRoomsNew(self):
        room_count = 0
        x_cur = 1
        y_cur = 1
        room_width  = random.choice([3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8])
        room_height = random.choice([3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8])
        print("\nRoom width", room_width, "\nRoom Height: ", room_height)

        if room_width < (self.width - x_cur):
            self.level.update({ (i,j):Room(i, j, room_count)
                                for i in range(x_cur, x_cur + room_width)
                                for j in range(y_cur, y_cur + room_height)
                })
            self.level.update({ (i,y_cur+room_height):Wall(i,y_cur+room_height)
                                for i in range(x_cur, x_cur + room_width + 1)
                })
            self.level.update({ (x_cur+room_width, j):Wall(x_cur+room_width, j)
                                for j in range(y_cur, y_cur + room_height)
                })
            x_cur += room_width + 2
        else:
            print ("TAH-DAH!")

    def placeRooms3(self):
        for i in range(1, self.width+1):
            for j in range(1, self.height+1):
                if (i,j) not in self.level or isinstance(self.level[(i,j)], Cell):
                    placeRoom(i, j, room_num)

    def placeRoomsTest(self):
        self.placeRoom(1,1,0)

    def placeRoom(self, x_cur, y_cur, room_num):

        # Determine width
        #################

        # find available width
        x = x_cur
        while x < self.width:
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
            while room_width < self.MIN_WALL_LEN or room_width > available_width:
                room_width = random.choice([3,3,4,4,4,5,5,5,5,6,6,6,7,7,8])

        # Determine height
        ##################

        y = y_cur
        while y < self.height:
            if isinstance(self.level[(x_cur, y)], Wall) \
            or isinstance(self.level[(x_cur, y)], Room):
                break
            y += 1
        available_height = y - y_cur

        room_height = 0
        if available_height < 2*self.MIN_WALL_LEN:
            room_height = available_height
        else:
            while room_height < self.MIN_WALL_LEN or room_height > available_height:
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


    def __str__(self):
        return "\n" + "\n".join(
            [  "".join( ["\t"]  +   [   str(self.level[(i,j)])
                                        for i in range(self.width+2)
                                    ])
                                        for j in range(self.height+2)
            ]) + "\n"

