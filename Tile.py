from enum import Enum

class tile(): 
    #stores the nodes/tiles children, neighbors, and parent(previous)
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
        self.children = []

    def setTile(self, value):
        self.value = value

#used for determining a tiles status
class value(Enum):
    queen = 1
    avail = 2
    inValid = 3