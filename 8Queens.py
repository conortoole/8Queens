from Tile import tile
from Tile import value

class main():

    def __init__(self, size):
        Tile = tile([0, 0], None, None, None, None, None, None, None, None, None)
        self.size = size
        self.board = [[Tile] * size for _ in range(size)]
        self.bCounter = 0 #keeps track of back tracks

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

       # while test.position[0] != 7 or test.value != value.queen:
        while test.S != None:
            test = self.placeNext(test)
            self.forwardCheck(test)

        print("Solution 1 with Queen 1 in Position " + start + ":")
        self.printBoard()
        print("\n\nThe positions of the Queens are:")

        while test != None:
            print("Row: " + str(test.position[0] + 1) + str(test.position[1]))
            test = test.previous
        print("\ntotal number of backtracks: ", self.bCounter)

    def generateTiles(self, size): #a graph of tile classes 
        chars = "ABCDEFGH"
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
                if (col - 1 >= 0):                                 #left side of the board
                    tile.W = self.board[tile.position[0]][col - 1]
                if ((tile.position[0] - 1 >= 0) and (col + 1 < self.size)):#top right corner
                    tile.NE = self.board[tile.position[0] - 1][col + 1]
                if ((tile.position[0] + 1 < self.size) and (col - 1 >= 0)):#top left corner
                    tile.SW = self.board[tile.position[0] + 1][col - 1]
                if ((tile.position[0] - 1 >= 0) and (col - 1 >= 0)):        #bottom left corner
                    tile.NW = self.board[tile.position[0] - 1][col - 1]
                if ((tile.position[0] + 1 < self.size ) and (col + 1 < self.size)):#bottom right corner
                    tile.SE = self.board[tile.position[0] + 1][col + 1]
                col += 1
                #print(f"Tile: {tile.position}, N: {tile.N.position if tile.N else None}, E: {tile.E.position if tile.E else None}, S: {tile.S.position if tile.S else None}, W: {tile.W.position if tile.W else None}")

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
        #if tile.position[0] == 7 and tile.value == value.queen:
        if tile.S == None:
            return
        
        #left diagonal
        tempTile = tile.SW
        while tempTile != None:
            tempTile.setTile(value.inValid)
            if tempTile.previous == None: #### THERE IS A ISSUE WITH THIS PART 
               tempTile.previous = tile # this will allow us to prevent overwriting during back tracking
            tempTile = tempTile.SW

        #Down
        tempTile = tile.S
        while tempTile != None:
            tempTile.setTile(value.inValid)
            if tempTile.previous == None:
                tempTile.previous = tile 
            tempTile = tempTile.S

        #right diagonal  
        tempTile = tile.SE
        while tempTile != None:
            tempTile.setTile(value.inValid)
            if tempTile.previous == None:
                tempTile.previous = tile 
            tempTile = tempTile.SE

    def backtrack(self, tile):
        #does the oppisate of place next removing X from any tiles related to the backtracked tile
        self.bCounter += 1
        #left diagonal
        tempTile = tile.SW
        while tempTile != None:
            if tempTile.previous == tile:
                tempTile.setTile(value.avail)
                tempTile.previous = None
            tempTile = tempTile.SW

        #down
        tempTile = tile.S
        while tempTile != None:
            if tempTile.previous == tile:
                tempTile.setTile(value.avail)
                tempTile.previous = None
            tempTile = tempTile.S

        #right diagonal
        tempTile = tile.SE
        while tempTile != None:
            if tempTile.previous == tile:
                tempTile.setTile(value.avail)
                tempTile.previous = None
            tempTile = tempTile.SE

        tile.setTile(value.inValid)
        tile = tile.previous
        return tile

    def placeNext(self, tile):
        flag = True
        if tile.S == None:
            print("\n")
            print("Solution Found!")
            return tile #tile
        
        tempTile = tile.S
        tempTile.previous = tile
        while tempTile.W != None: #gets to the left of the next row
            tempTile = tempTile.W

        while flag:
            if tempTile.value == value.avail: #places a queen in the first available spot
                tempTile.setTile(value.queen)
                tempTile.previous = tile
                return tempTile
            else:
                if tempTile.E == None: #if there are no avail tiles then backtrack is called
                    tile = self.backtrack(tile)
                    return tile
                else:
                    tempTile = tempTile.E #else move to the next tile to the right

Main = main(8)
Main.run()