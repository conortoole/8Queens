from Tile import tile
from Tile import value

class main():

    def __init__(self, size):
        Tile = tile([0, 0], None, None, None, None, None, None, None, None)
        self.size = size
        self.board = [[Tile] * size for _ in range(size)]

    def run(self):
        flag = True
        self.generateTiles(self.size)
        self.connectTiles()
        while(flag):
            start = input("select a starting position (A1, B3 etc)")
            #conversion from input to correct ints
            let = str(start[0])
            let = let.upper()
            num = ord(let) - ord('A')
            if (num > self.size - 1 or num < 0 or int(start[1]) > self.size or int(start[1]) - 1 < 0):
                print("invalid input try again")
            else:
                flag = False
        #^
        test = self.getTile(int(start[1]) - 1, num)
        self.setTile(test, value.queen)
        self.forwardCheck(test)
        self.printBoard()

    def generateTiles(self, size): #a graph of tile classes 
        chars = "$ABCDEFGH"
        for row in range(size):
            for col in range(size):
                newTile = tile([row, chars[col]], None, None, None, None, None, None, None, None)
                self.board[row][col] = newTile

    def getTile(self, row, col):
        return self.board[row][col]
    
    def setTile(self, tile, value):
        tile.setTile(value)

    def connectTiles(self): #connecting the tiles so they know their neighbors
        col = 0
        for row in self.board:
            col = 0
            for tile in row: # the if check for the edges of the board
                if (tile.position[0] - 1 > 0):
                    tile.N = self.board[tile.position[0] - 1][col]
                if (col + 1 < self.size):
                    tile.E = self.board[tile.position[0]][col + 1]
                if (tile.position[0] + 1 < self.size):
                    tile.S = self.board[tile.position[0] + 1][col]
                if (col - 1 > 0):
                    tile.W = self.board[tile.position[0]][col - 1]
                if ((tile.position[0] - 1 > 0) and (col + 1 < self.size)):
                    tile.NE = self.board[tile.position[0] - 1][col + 1]
                if ((tile.position[0] + 1 < self.size) and (col - 1 > 0)):
                    tile.SW = self.board[tile.position[0] + 1][col - 1]
                if ((tile.position[0] - 1 > 0) and (col - 1 > 0)):
                    tile.NW = self.board[tile.position[0] - 1][col - 1]
                if ((tile.position[0] + 1 < self.size) and (col + 1 < self.size)):
                    tile.SE = self.board[tile.position[0] + 1][col + 1]
                col += 1

    def printBoard(self):
        for row in self.board:
            print()
            for tile in row:
                if (tile.value == value.queen):
                    print("[Q]", end="") # x is a queen
                elif (tile.value == value.noQueen):
                    print("[_]", end="")
                else:
                    print("[X]", end="")

    def forwardCheck(self, tile):
        tempTile = tile
        while tile != None:
            tile = tile.NE
            self.setTile(tile, value.inValid)

Main = main(8)
Main.run()