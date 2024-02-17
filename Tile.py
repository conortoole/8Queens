from enum import Enum

class tile():
    def __init__(self, position, N, E, S, W, NE, SE, SW, NW, previous):
        self.value = value.avail
        self.N = N
        self.E = E
        self.S = S
        self.W = W
        self.NE = NE
        self.SW = SW
        self.NW = NW
        self.SE = SE
        self.position = position
        self.previous = previous

    def setTile(self, value):
        self.value = value

class value(Enum):
    queen = 1
    avail = 2
    inValid = 3