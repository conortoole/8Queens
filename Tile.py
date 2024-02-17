from enum import Enum

class tile():
    def __init__(self, position, N, E, S, W, NE, SE, SW, NW):
        self.value = value.noQueen
        self.N = N
        self.E = E
        self.S = S
        self.W = W
        self.NE = NE
        self.SW = SW
        self.NW = NW
        self.SE = SE
        self.position = position

    def setTile(self, value):
        self.value = value

class value(Enum):
    queen = 1
    noQueen = 2
    inValid = 3