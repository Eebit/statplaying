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
        
        self.processed = False # processed flag is used for when a unit has been fully processed for the turn, either automatically (having taken both act and move commands) or manually (by waiting)
        
    def loadBaseStats(self):
        self.stats = self.properties["stats"]
    
    def output(self):
        outStr = str(self.properties["cell-name"]) + " (" + str(self.properties["profession"]["name"]) + ")" +"\nHP:\t\t" + str(self.stats["current-health"]) + "/" + str(self.stats["max-health"]) + "\nMP:\t\t" + str(self.stats["current-mana"]) + "/" + str(self.stats["max-mana"]) + "\nAtk:\t\t" + str(self.stats["attack"]) +"\nDef:\t\t" + str(self.stats["defense"]) + "\nInt:\t\t" + str(self.stats["intelligence"]) + "\nSpr:\t\t" + str(self.stats["spirit"]) + "\nCritical:\t" + str(self.stats["critical"]) + "%" + "\nEvasion:\t" + str(self.stats["evasion"]) + "%" + "\nMovement:\t" + str(self.stats["movement"]) + " Cells" + "\n{/////} {/////} {/////}"
        return outStr
        
    """
    #
    # SECTION FOR COMMANDS
    #
    """
    
    def movementCommand(self, grid):
        print("Move " + self.properties["cell-name"])
        
        # output the list of Cells the unit can move to
        l = self.getMovementRange(grid)
        
        for cell in l:
            print(formatOutputCoords(cell))
        
        while True:
            # prompt user to select a Cell from the list
            take = input("Select a Cell: ")
            
            t = formatInputCoords(take)
            print(t)
            
            # if the user's chosen cell is in the list of cells, then
            if t in l:
                # get all valid paths to the Cell
                paths = self.getPaths(grid, grid.getCell(t))
                
                if(len(paths) == 0):
                    print("Path Error")
                
                elif(len(paths) > 1):
                    print("Choose the index of the path " + self.properties["cell-name"] + " should follow: ")
                    paths.sort(key = len)
                    i = 1
                    for path in paths:
                        p = []
                        for pos in path:
                            pstr = formatOutputCoords(pos)
                            p.append(pstr)
                        print("[" + str(i) + "]: " + "->".join(p))
                        i += 1
                    
                    while(True):
                        index = input("> ")
                        if(int(index) <= 0):
                            print("Invalid Index")
                        else:
                            try:
                                print(paths[int(index) - 1])
                                chosenPath = paths[int(index) - 1]
                                break
                            except IndexError:
                                print("Invalid Index")
                    
                    break
                
                else: # exactly one path
                    for path in paths:
                        p = []
                        for pos in path:
                            pstr = formatOutputCoords(pos)
                            p.append(pstr)
                        chosenPath = path
                    print("->".join(p))
                    break
        
        print("Chosen Path: " + str(chosenPath))
        self.stepThroughMovement(chosenPath, grid)
        
        self.hasMoved = True # mark the unit as having moved
        #return the chosen path so that it can be appended to the game stack?
    
    def actionCommand(self, grid):
        print("Act " + self.properties["cell-name"])
        self.hasActed = True
        
    def waitCommand(self, grid):
        print("Wait " + self.properties["cell-name"])
        self.hasMoved = True
        self.hasActed = True
        self.processed = True
    
    """
    #
    # SECTION FOR HELPER METHODS
    #
    """
    
    def getMovementRange(self, grid):
        mov = self.stats["movement"]
        cur = (mov, self.position)
        
        stack = []
        stack.append(cur)
        possible = []
        
        while(stack != []):
            curMov, curPos = stack.pop()
            
            curCell = grid.getCell( curPos )
            
            #If you have 0 moves or more and the current cell is occupiable, then store the current path
            if( (curMov >= 0) and (curCell.properties["occupiable"] == True) and (curCell.position not in possible) ):
                possible.append( curCell.position )
            
            #If the current path ran out of moves or isn't passable, go to the next path
            if( (curMov == 0) or (curCell.properties["passable"] == False) ): #TODO: Test for equal alignment here too
                continue
            
            n = curCell.getNeighbors(grid)
            
            for cell in n:
                stack.append( (curMov - 1, cell.position) )
                
        return possible # This is a list of valid positions that can be moved to -- does not account for paths to that position
    
    """
    TODO: I'm sure this method could use some heavy optimization... but hey, it's in place
    """
    def getPaths(self, grid, target):
        mov = self.stats["movement"]
        cur = (mov, [self.position])

        paths = []
        paths.append(cur)
        possiblePaths = []
        while(paths != []):
            #print(paths)
            curMov, curPath = paths.pop()
            curPos = curPath[-1]
            curCell = grid.getCell(curPos)
            
            #If you have 0 moves or more and the current cell is occupiable, then store the current path
            if (curPos == target.position) and (curMov >= 0) and (curPath not in possiblePaths):
                possiblePaths.append(curPath)
                continue
            
            #If the current path ran out of moves or isn't passable, go to the next path
            if( (curMov == 0) or (curCell.properties["passable"] == False) or (len(curPath) > mov + 1 ) ): #TODO: Test for equal alignment here too
                continue
                
            n = curCell.getNeighbors(grid)
            
            for cell in n:
                newPath = curPath[:]
                newPath.append(cell.position)
                
                paths.append( (curMov - 1, newPath) )
        
        return possiblePaths
    
    """
    Helper method that is called by the Movement Phase method in order to have the unit
    step through each individual Cell on their desired path. This allows for us to check
    whether they spring a trap, or are affected by "passable" effects along their path.
    """
    def stepThroughMovement(self, path, grid):
        grid.getCell(self.position).occupiedBy = None
        
        # For every Cell along the path aside from the first (our current Cell)
        for pos in path[1:]:
            cell = grid.getCell(pos)
            
            # Set ourselves to occupy this Cell, if only temporarily
            cell.occupiedBy = self
            
            # TODO: test statements go in here (traps, passable effects, etc)
            
            # if the cell is not the last step in the path, i.e. the cell we finish on
            # then remove ourself from occupying it
            if(pos != path[-1]):
                print("proceeding movement")
                cell.occupiedBy = None
            else:
                print("done")
        
        self.assignPosition(path[-1])