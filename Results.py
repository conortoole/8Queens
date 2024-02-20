from Tile import tile
from Tile import value

class results:
    def __init__(self, tile):
        self.tile = tile

    def print(self):
        while self.tile != None:
            print("Row: " + str(self.tile.position[0] + 1) + str(self.tile.position[1]))
            self.tile = self.tile.previous