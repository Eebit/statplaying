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
    
    def movementCommand(self, grid):
        print("Move " + self.properties["cell-name"])
        print(self.getMovementRange(grid) )
        self.hasMoved = True
        
    def actionCommand(self, grid):
        print("Act " + self.properties["cell-name"])
        self.hasActed = True
        
    def waitCommand(self, grid):
        print("Wait " + self.properties["cell-name"])
        self.hasMoved = True
        self.hasActed = True
    
    def getMovementRange(self, grid):
        mov = self.stats["movement"]
        cur = (mov, self.position)
        
        queue = []
        queue.append(cur)
        possible = []
        
        while(queue != []):
            curMov, curPos = queue.pop()
            
            curCell = grid.getCell( curPos )
            
            #If you have 0 moves or more and the current cell is occupiable, then store the current path
            if( (curMov >= 0) and (curCell.properties["occupiable"] == True) and (curCell.position not in possible) ):
                possible.append( curCell.position )
            
            #If the current path ran out of moves or isn't passable, go to the next path
            if( (curMov == 0) or (curCell.properties["passable"] == False) ): #TODO: Test for equal alignment here too
                continue
            
            n = curCell.getNeighbors(grid)
            
            for cell in n:
                queue.append( (curMov - 1, cell.position) )
                
        return possible # This is a list of valid positions that can be moved to -- does not account for paths to that position