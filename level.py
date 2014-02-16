#   Procedural Content Generation Game, name TBD
#   Author: Colin O'Neill   faokryn@gmail.com
#   github.com/Faokryn/1stPGC

import random

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obj = "W"

    def __str__(self):
        if self.obj == "W":
            return("W")
        else:
            return(" ")

class Level:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.level = {}

        i = 0
        while i < width+2:
            j = 0
            while j < height+2:
                self.level[(i,j)] = Cell(i,j)
                j = j+1
            i = i+1

    def __str__(self):
        result = "\n\n"
        j = 0
        while j < self.height+2:
            line = ""
            i = 0
            while i < self.width+2:
                line += str( self.level[ (i,j) ] )
                i = i+1
            result += line + "\n"
            j = j+1
        return result

def main():
    width = int(input("Width?"))
    height = int(input("Height?"))
    level = Level(width, height)
    print(str(level))
main()