from Tile import tile
from Tile import value
from Board import board
import copy

class main():

    def __init__(self):
        self.boards = []
        self.fCounter = 0 #keeps track of back tracks
        self.dCounter = 0 #keeps track of back tracks
        self.visitedStack = []
        self.results = []
        self.ForwardCounts = []
        self.DARCCounts = []
        self.EndTile = tile([11, 11], None, None, None, None, None, None, None, None, None)

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
        
        firstTile = self.getTile(int(start[1]) - 1, num, Board)
        firstTest = firstTile
        self.setTile(firstTile, value.queen)

        ##### forward checking implementation ################################################################
        while firstTile != self.EndTile:
            self.forwardCheck(firstTile)
            while firstTile.S != None:
                firstTile = self.placeNext(firstTile)
                if tile is not self.EndTile:
                    self.forwardCheck(firstTile)

            copyy = copy.copy(board)
            self.boards.append(copyy)
            self.results.append(self.getPositions(firstTile))
            self.ForwardCounts.append(self.fCounter)
            self.fCounter = 0
            firstTile = self.backtrack(firstTile)
        
        Board.clearBoard()
        firstTile = firstTest #reset first tile

        ##### directional arc implementation ################################
        while firstTile != self.EndTile:
            self.setTile(firstTile, value.queen)
            self.check(firstTile)
            while firstTile != None and firstTile.S != None:
                firstTile = self.directionalArc(firstTile)
            
            #self.results.append(self.getPositions(firstTile))
            self.DARCCounts.append(self.dCounter)
            self.dCounter = 0
            firstTile = self.backtrack(firstTile)
        
        self.printResults()
        Board.clearBoard()

    def getFinalCount(self, items):
        count = 0
        for item in items:
            count = count + item
        return count

    def printResults(self):
        i = 0
        for solution in self.results:
            if len(solution) != 8:
                break
            print("\nSolution 1 with Queen 1 in Position " + str(solution[0][0]) + str(solution[0][1]) + ":")
            print("\nThe positions of the Queens are:")
            #self.boards[i].printBoard(self.boards[i])
            for item in solution:
                print("Row: " + str(item[0]) + str(item[1]))

            print("\n\ntotal number of backtracks before this solution was found: ")
            print("Forward Checking: ", self.ForwardCounts[i])
            if len(self.DARCCounts) <= i :
                print("Directional Look Ahead: no solution")
            else:
                print("Directional Look Ahead: ", self.DARCCounts[i])
            i += 1
        print("Total numbers of backtracks before this solution was found:")
        print("Forward Checking: " + str(self.getFinalCount(self.ForwardCounts)))
        print("Directional Look Ahead: " + str(self.getFinalCount(self.DARCCounts)))

    def getPositions(self, tile):
        result = []
        if tile == None:
            return []
        
        while tile != None:
            result.append((tile.position[0] + 1, tile.position[1]))
            tile = tile.previous
        result.reverse()
        return result

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
        directions = [tile.SW, tile.S, tile.SE]
        
        for direction in directions:
            tempTile = direction
            while tempTile is not None:
                tempTile.setTile(value.inValid)
                if tempTile.previous is None: 
                    tile.children.append(tempTile)
                    tempTile.previous = tile # this will allow us to prevent overwriting during back tracking
                if (direction == tile.SW):
                    tempTile = tempTile.SW
                elif (direction == tile.S):
                    tempTile = tempTile.S
                else:
                    tempTile = tempTile.SE

    def backtrack(self, tile):
        #does the oppisate of place next removing X from any tiles related to the backtracked tile
        if tile.N == None:
            #no more solutions
            return self.EndTile
        self.clear(tile)
        tile.setTile(value.inValid)
        tile.previous.children.append(tile)
        tile = tile.previous
        return tile

    def clear(self, tile):
        for child in tile.children:
            child.value = value.avail
            child.previous = None
            self.clear(child)
        tile.children.clear()

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
        tempTile = tile
        tile = self.getStartRow(tile)

        while tile.E != None:
            if tile.value == value.avail:
                self.clear(tempTile)
                return True
            tile = tile.E

        self.clear(tempTile)
        return False
    
    def placeNext(self, tile):
        flag = True
        if tile.S == None:
            return tile #tile
        
        tempTile = tile.S
        #tempTile.previous = tile
        while tempTile.W != None: #gets to the left of the next row
            tempTile = tempTile.W

        while flag:
            if tempTile.value == value.avail: #places a queen in the first available spot
                tempTile.setTile(value.queen)
                tempTile.previous = tile
                tile.children.append(tempTile)
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