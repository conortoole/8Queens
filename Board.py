from Tile import tile
from Tile import value

class board():
    def __init__(self, size):
        Tile = tile([0, 0], None, None, None, None, None, None, None, None, None)
        self.size = size
        self.tiles = [[Tile] * size for _ in range(size)]

    def generateTiles(self, size): #a graph of tile classes 
                chars = "ABCDEFGH"
                for row in range(size):
                    for col in range(size):
                        newTile = tile([row, chars[col]], None, None, None, None, None, None, None, None, None)
                        self.tiles[row][col] = newTile
    
    def connectTiles(self): #connecting the tiles so they know their neighbors
        col = 0
        for row in self.tiles:
            col = 0
            for tile in row: # the if checks for the edges of the board
                if (tile.position[0] - 1 >= 0):                    #top of board
                    tile.N = self.tiles[tile.position[0] - 1][col]
                if (col + 1 < self.size):                         #far right side of board
                    tile.E = self.tiles[tile.position[0]][col + 1]
                if (tile.position[0] + 1 < self.size):            #bottom of board
                    tile.S = self.tiles[tile.position[0] + 1][col]
                if (col - 1 >= 0):                                 #left side of the board
                    tile.W = self.tiles[tile.position[0]][col - 1]
                if ((tile.position[0] - 1 >= 0) and (col + 1 < self.size)):#top right corner
                    tile.NE = self.tiles[tile.position[0] - 1][col + 1]
                if ((tile.position[0] + 1 < self.size) and (col - 1 >= 0)):#top left corner
                    tile.SW = self.tiles[tile.position[0] + 1][col - 1]
                if ((tile.position[0] - 1 >= 0) and (col - 1 >= 0)):        #bottom left corner
                    tile.NW = self.tiles[tile.position[0] - 1][col - 1]
                if ((tile.position[0] + 1 < self.size ) and (col + 1 < self.size)):#bottom right corner
                    tile.SE = self.tiles[tile.position[0] + 1][col + 1]
                col += 1
    
    def printBoard(self):
        for row in self.tiles:
            print()
            for tile in row:
                if (tile.value == value.queen):
                    print("[Q]", end="") # x is a queen
                elif (tile.value == value.avail):
                    print("[_]", end="")
                else:
                    print("[X]", end="")
        print("\n")

    def clearBoard(self):
        for row in self.tiles:
            for item in row:
                item.value = value.avail
                item.previous = None
                item.children = None