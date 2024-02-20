from Tile import tile
from Tile import value
from Board import board
from Results import results

class main():

    def __init__(self):
        self.boards = []
        self.fCounter = 0 #keeps track of back tracks
        self.dCounter = 0 #keeps track of back tracks
        self.visitedStack = []
        self.results = []
        self.rowCounter = 0

    def run(self):
        flag = True
        Board = board(8) 
        Board.generateTiles(Board.size)
        Board.connectTiles()
        while(flag):
            start = input("select a starting position from row 1 (A1, B1 etc)")
            #conversion from input to correct ints
            let = str(start[0])
            let = let.upper()
            num = ord(let) - ord('A')
            #input handling
            if (num > Board.size - 1 or num < 0 or int(start[1]) > Board.size or int(start[1]) != 1):
                print("invalid input try again")
            else:
                flag = False
        flag = True
        #place first tile
        test = self.getTile(int(start[1]) - 1, num, Board)
        self.setTile(test, value.queen)
        firstTest = test

        print("Solution 1 with Queen 1 in Position " + start + ":")
        print("\n\nThe positions of the Queens are:")

        #forward checking implementation
        self.forwardCheck(test)
        while test.S != None:
            test = self.placeNext(test)
            self.forwardCheck(test)

        self.printResults(test)
        Board.clearBoard
        
        print("\ntotal number of backtracks before this solution was found: ")
        print("Forward Checking: ", self.fCounter)
        print("Directional Look Ahead: ", self.dCounter)

        #directional arc implementation
        # test2 = firstTest
        # self.setTile(test2, value.queen)
        # self.check(test2)
        # while test2 != None and test2.S != None:
        #     #self.check(test)
        #     #Board.printBoard()
        #     test2 = self.directionalArc(test2)

        #self.boards[0].printBoard()
        #self.results[1].print()
        #self.boards[1].printBoard()
        #self.printBoard(self.boards[0])
        #self.printBoard(self.boards[1])

    def printResults(self, tile):
        while tile != None:
            print("Row: " + str(tile.position[0] + 1) + str(tile.position[1]))
            tile = tile.previous

    def getTile(self, row, col, board):
        return board.tiles[row][col]
    
    def setTile(self, tile, value):
        tile.setTile(value)

    def forwardCheck(self, tile):
        #if tile.position[0] == 7 and tile.value == value.queen:
        if tile.S == None:
            return
        self.check(tile)

    def check(self, tile):
        #left diagonal
        tempTile = tile.SW
        while tempTile != None:
            tempTile.setTile(value.inValid)
            if tempTile.previous == None: 
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
        self.clear(tile)
        tile.setTile(value.inValid)
        for child in tile.children:
            child.value = value.avail
        tile = tile.previous
        return tile

    def clear(self, tile):
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

    def directionalArc(self, tile):
        #if tile.position[0] == 7 and tile.value == value.queen:
        if tile.S == None:
            return tile
        
        tempTile = self.getStartRow(tile)
            
        while tempTile is not None:
            if tempTile.value == value.avail:
                availableMove = self.checkIfValid(tempTile)

                if availableMove: #places a queen in the first available spot
                    tempTile.value = value.queen
                    tempTile.previous = tile
                    tile.children.append(tempTile)
                    self.check(tempTile)
                    return tempTile    
            
            if tempTile.E is None: #if there are no avail tiles then backtrack is called
                self.dCounter += 1
                tile = self.backtrack(tile)
                return tile
            else:
                tempTile = tempTile.E #else move to the next tile to the right
        return tile

    def checkIfValid(self, tile):
        self.check(tile)
        tile = self.getStartRow(tile)

        while tile.E != None:
            if tile.value == value.avail:
                self.clear(tile)
                return True
            tile = tile.E

        self.clear(tile)
        return False
    
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
                    self.fCounter += 1
                    tile = self.backtrack(tile)
                    return tile
                else:
                    tempTile = tempTile.E #else move to the next tile to the right

    def getStartRow(self, tile):
        if tile.S == None:
            return tile
        
        tile = tile.S
        while tile.W != None: #gets to the left of the next row
            tile = tile.W
        return tile

Main = main()
Main.run()