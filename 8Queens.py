from Tile import tile
from Tile import value

class main():

    def __init__(self, size):
        Tile = tile([0, 0], None, None, None, None, None, None, None, None, None)
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
            #input handling
            if (num > self.size - 1 or num < 0 or int(start[1]) > self.size or int(start[1]) - 1 < 0):
                print("invalid input try again")
            else:
                flag = False
        #place first tile
        test = self.getTile(int(start[1]) - 1, num)
        self.setTile(test, value.queen)
        #^
        self.forwardCheck(test)
        self.printBoard()
        i = 1
        while i < 20:
            test = self.placeNext(test)
            self.forwardCheck(test)
            print("\n")
            print("------------------------")
            self.printBoard()
            i += 1

    def generateTiles(self, size): #a graph of tile classes 
        chars = "$ABCDEFGH"
        for row in range(size):
            for col in range(size):
                newTile = tile([row, chars[col]], None, None, None, None, None, None, None, None, None)
                self.board[row][col] = newTile

    def getTile(self, row, col):
        return self.board[row][col]
    
    def setTile(self, tile, value):
        tile.setTile(value)

    def connectTiles(self): #connecting the tiles so they know their neighbors
        col = 0
        for row in self.board:
            col = 0
            for tile in row: # the if checks for the edges of the board
                if (tile.position[0] - 1 >= 0):                    #top of board
                    tile.N = self.board[tile.position[0] - 1][col]
                if (col + 1 < self.size):                         #far right side of board
                    tile.E = self.board[tile.position[0]][col + 1]
                if (tile.position[0] + 1 < self.size):            #bottom of board
                    tile.S = self.board[tile.position[0] + 1][col]
                if (col - 1 > 0):                                 #left side of the board
                    tile.W = self.board[tile.position[0]][col - 1]
                if ((tile.position[0] - 1 >= 0) and (col + 1 < self.size)):#top right corner
                    tile.NE = self.board[tile.position[0] - 1][col + 1]
                if ((tile.position[0] + 1 < self.size) and (col - 1 > 0)):#top left corner
                    tile.SW = self.board[tile.position[0] + 1][col - 1]
                if ((tile.position[0] - 1 >= 0) and (col - 1 > 0)):        #bottom left corner
                    tile.NW = self.board[tile.position[0] - 1][col - 1]
                if ((tile.position[0] + 1 < self.size) and (col + 1 < self.size)):#bottom right corner
                    tile.SE = self.board[tile.position[0] + 1][col + 1]
                col += 1

    def printBoard(self):
        for row in self.board:
            print()
            for tile in row:
                if (tile.value == value.queen):
                    print("[Q]", end="") # x is a queen
                elif (tile.value == value.avail):
                    print("[_]", end="")
                else:
                    print("[X]", end="")

    def forwardCheck(self, tile):
        #up diagonal
        tempTile = tile.NE
        while tempTile != None:
            tempTile.setTile(value.inValid)
            tempTile = tempTile.NE

        #to the right
        tempTile = tile.E
        while tempTile != None:
            tempTile.setTile(value.inValid)
            tempTile = tempTile.E

        #down diagonal
        tempTile = tile.SE
        while tempTile != None:
            tempTile.setTile(value.inValid)
            tempTile = tempTile.SE

    def backtrack(self, tile):
        #up diagonal
        tempTile = tile.NE
        while tempTile != None:
            tempTile.setTile(value.avail)
            tempTile = tempTile.NE

        #to the right
        tempTile = tile.E
        while tempTile != None:
            tempTile.setTile(value.avail)
            tempTile = tempTile.E

        #down diagonal
        tempTile = tile.SE
        while tempTile != None:
            tempTile.setTile(value.avail)
            tempTile = tempTile.SE

        tile.setTile(value.inValid)
        tile = tile.previous
        return tile

    def placeNext(self, tile):
        flag = True
        tempTile = tile.E
        tempTile.previous = tile
        while tempTile.N != None:
            tempTile = tempTile.N

        while flag:
            if tempTile.value == value.avail:
                tempTile.setTile(value.queen)
                tempTile.previous = tile
                return tempTile
            else:
                if tempTile.S == None:
                    tile = self.backtrack(tile)
                    return tile
                else:
                    tempTile = tempTile.S

Main = main(8)
Main.run()