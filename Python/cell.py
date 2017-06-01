from util import *

class Cell:
    def __init__(self, cell_dict):
        self.properties = cell_dict
        self.position = None
        self.occupiedBy = None
    
    """
    Method to attach a position to the Cell in question.
    """
    def assignPosition(self, pos):
        self.position = pos
    
    def __str__(self):
        return self.properties["cell-id"]
        
    def __repr__(self):
        return str(self)
    
    """
    Method to output a Cell's details when called. If the Cell
    has stats, then it will also print out any important details.
    
    TODO: Add functionality to output any Trigger Commands, passability/occupiability,
    etc.
    """
    def output(self):
        if(self.properties["has-stats"] == False):
            outStr = str(self.properties["cell-name"])
        else:
            outStr = str(self.properties["cell-name"] + "\nstats lol")
        return outStr
    
    """
    Method that checks the neighbors of the Cell and returns a list of those that are valid
    
    Currently does not check whether the Cell itself is valid, so I guess that's something to watch for
    """
    def getNeighbors(self, grid):
        neighbors = []
        
        if(self.position[0] > 0):
            neighbors.append(grid.getCell( (self.position[0] - 1, self.position[1]) ))
        
        if(self.position[1] > 0):
            neighbors.append(grid.getCell( (self.position[0], self.position[1] - 1) ))
        
        if(self.position[0] < grid.height - 1):
            neighbors.append(grid.getCell( (self.position[0] + 1, self.position[1]) ))
        
        if(self.position[1] < grid.width - 1):
            neighbors.append(grid.getCell( (self.position[0], self.position[1] + 1) ))
        
        return neighbors
        

class Unit(Cell):
    def __init__(self, cell_dict):
        self.properties = cell_dict
        self.position = None
        
        self.loadBaseStats()
        self.basicAttackRange = self.properties["equipment"][0]["range"]
        
        self.hasMoved = False
        self.hasActed = False
        
    def loadBaseStats(self):
        self.stats = self.properties["stats"]
    
    def output(self):
        outStr = str(self.properties["cell-name"]) + " (" + str(self.properties["profession"]["name"]) + ")" +"\nHP:\t\t" + str(self.stats["current-health"]) + "/" + str(self.stats["max-health"]) + "\nMP:\t\t" + str(self.stats["current-mana"]) + "/" + str(self.stats["max-mana"]) + "\nAtk:\t\t" + str(self.stats["attack"]) +"\nDef:\t\t" + str(self.stats["defense"]) + "\nInt:\t\t" + str(self.stats["intelligence"]) + "\nSpr:\t\t" + str(self.stats["spirit"]) + "\nCritical:\t" + str(self.stats["critical"]) + "%" + "\nEvasion:\t" + str(self.stats["evasion"]) + "%" + "\nMovement:\t" + str(self.stats["movement"]) + " Cells" + "\n{/////} {/////} {/////}"
        return outStr
    
    def movementCommand(self):
        print("Move " + self.properties["cell-name"])
        self.hasMoved = True
        
    def actionCommand(self):
        print("Act " + self.properties["cell-name"])
        self.hasActed = True
        
    def waitCommand(self):
        print("Wait " + self.properties["cell-name"])
        self.hasMoved = True
        self.hasActed = True
    
    def getRange(self, grid):
        pass
    
    #Takes in the grid and the entire cell dictionary does not account for other Units yet
    def getMovementRange(self, grid, full_cell_dict):
        mov = self.stats["movement"]
        cur = (mov, [self.position])
        globalCells = full_cell_dict["global-cells"]

        cellByID = {}
        for cellType in globalCells:
            cellByID[cellType["cell-id"]] = cellType

        paths = []
        paths.append(cur)
        possiblePaths = []
        while(paths != []):
            curMov, curPath = paths.pop()
            curPos = curPath[-1]
            curCell = grid[curPos[0]][curPos[1]]

            #If you have 0 moves or more and the current cell is occupiable, then store the current path
            if( (curMov >= 0) and (cellByID[curCell]["occupiable"] == True) and (curPath not in possiblePaths)):
                possiblePaths.append(curPath)

            #If the current path ran out of moves or isn't passable, go to the next path
            if(curMov == 0 or cellByID[curCell]["passable"] == False): #TODO: Test for equal alignment here too
                continue

            #Try to move up
            nextCell = (curPos[0]+1, curPos[1])
            if(nextCell[0] < len(grid) and nextCell[1] < len(grid[0])):
                newPath = curPath.append(nextCell[:])
                paths.append(curMov-1, newPath[:])
            
            #Try to move down
            nextCell = (curPos[0]-1, curPos[1])
            if(nextCell[0] < len(grid) and nextCell[1] < len(grid[0])):
                newPath = curPath.append(nextCell[:])
                paths.append(curMov-1, newPath[:])
            
            #Try to move to the right
            nextCell = (curPos[0], curPos[1]+1)
            if(nextCell[0] < len(grid) and nextCell[1] < len(grid[0])):
                newPath = curPath.append(nextCell[:])
                paths.append(curMov-1, newPath[:])
            
            #Try to move to the left
            nextCell = (curPos[0], curPos[1]-1)
            if(nextCell[0] < len(grid) and nextCell[1] < len(grid[0])):
                newPath = curPath.append(nextCell[:])
                paths.append(curMov-1, newPath[:])

        return possiblePaths
