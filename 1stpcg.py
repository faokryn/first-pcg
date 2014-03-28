################################################################################
#   Procedural Content Generation Game, name TBD
#
#   Author: Colin O'Neill   faokryn@gmail.com
#   github.com/Faokryn/1stPGC
#
#   1stpcg.py
#   Acts as a temporary main function for use during early development.
#   Currently, prompts the user to input a width and height, generates a level
#   with that width and height, and prints the generated level.
################################################################################

from level import *

def main():
    width = int(input("Width?"))
    height = int(input("Height?"))
    level = Level(width, height)
    print(str(level))
main()