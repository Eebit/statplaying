from util import *

# This class will be used for the basic physical or magical stats
class Statistic:
    def __init__(self, type, value):
        self.type = type # the "type" of the stat, e.g. Atk, Int, Def, Res
        self.value = value # the base value of the stat
    
    def __repr__(self):
        return str(self.type) + ":\t\t" + str(self.value)
    
    # Add an equipment bonus
    def setEquipBonus(self, bonus):
        pass
    
    # Add a bonus from a buff
    def setBuffBonus(self, buff):
        pass

# This class will be used for HP and MP
class FractionStatistic:
    def __init__(self, type, numerator, denominator):
        self.type = type
        self.numerator = numerator
        self.denominator = denominator
    
    def __repr__(self):
        return str(self.type) + ": \t\t" + str(self.numerator) + "/" + str(self.denominator)
    
    # Add an equipment bonus
    def setEquipBonus(self, bonus):
        pass
    
    # Add a bonus from a buff
    def setBuffBonus(self, buff):
        pass
    
class PercentileStatistic:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return str(self.type) + ":\t" + str(self.value) + "%"
    
    def setEquipBonus(self, bonus):
        pass
    
    def setBuffBonus(self, buff):
        pass

class MovementStatistic:
    def __init__(self, moveCells):
        self.type = "Movement"
        self.value = moveCells
    
    def __repr__(self):
        return str(self.type) + ":\t" + str(self.value) + " Cells"
    
    def setEquipBonus(self, bonus):
        pass
    
    def setBuffBonus(self, buff):
        pass

class ExcessGauge:
    def __init__(self, current):
        self.type = "X-Gauge"
        self.numerator = current
        self.denominator = 30
    
    def __repr__(self):
        return str(self.type) + ":\t" + str(self.numerator) + "/" + str(self.denominator)

# ---------------------------------------------------
#   Split
# ---------------------------------------------------

class Cell:
    def __init__(self, cell_dict):
        self.properties = cell_dict
        self.id = cell_dict["cell-id"]
        
        self.position = None
        self.occupiedBy = None
    
    """
    Method to attach a position to the Cell in question.
    """
    def assignPosition(self, pos):
        self.position = pos
    
    def __str__(self):
        return self.id
        
    def __repr__(self):
        return str(self)
    
    """
    Method to output a Cell's details when called. If the Cell
    has stats, then it will also print out any important details.
    
    TODO: Add functionality to output any Trigger Commands, passability/occupiability,
    etc.
    """
    def output(self):
        if(self.properties["classification"] == 0): # empty cell
            outStr = "{" + str(self.properties["cell-id"]) + "} - " + str(self.properties["cell-name"])
        else: # object cell
            if(self.properties["block-ranged"] == True):
                block = "Block Property"
            else:
                block = ""
            
            if(self.properties["destructable"] == True):
                des = "Can be Destroyed"
            else:
                des = "Indestructible"
            
            if(self.properties["passable"] == True):
                pas = "Can be Passed"
            else:
                pas = "Cannot be Passed"
            
            if(self.properties["occupiable"] == True):
                occ = "Can be Occupied"
            else:
                occ = "Cannot be Occupied"
            
            if(self.properties["has-stats"] == True):
                stats = "CON: " + str(self.properties["stats"]["constitution"]) + "/10"
            else:
                stats = ""
            
            outStr = "{" + str(self.properties["cell-id"]) + "} - " +  str(self.properties["cell-name"] + "\n" + block + "\n" + des + "\n" + pas + "\n" + occ + "\n" + stats)
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
    
    def getDiagonals(self, grid):
        diagonals = []
        
        # top left
        if((self.position[0] > 0) and (self.position[1] > 0)):
            diagonals.append(grid.getCell( (self.position[0] - 1, self.position[1] - 1) ))
        
        # bottom left
        if((self.position[0] > 0) and (self.position[1] < grid.width - 1)):
            diagonals.append(grid.getCell( (self.position[0] - 1, self.position[1] + 1) ))
        
        # top right
        if((self.position[0] < grid.width - 1) and (self.position[1] > 0)):
            diagonals.append(grid.getCell( (self.position[0] + 1, self.position[1] - 1) ))
            
        # bottom right
        if((self.position[0] < grid.width - 1) and (self.position[1] < grid.width - 1)):
            diagonals.append(grid.getCell( (self.position[0] + 1, self.position[1] + 1) ))
        
        return diagonals
    
    def getSurrounding(self, grid):
        return self.getNeighbors(grid) + self.getDiagonals(grid)

class Unit(Cell):
    def __init__(self, cell_dict):
        #self.properties = cell_dict
        self.id = cell_dict["cell-id"]
        self.name = cell_dict["cell-name"]
        self.profession = cell_dict["profession"]
        self.alignment = cell_dict["alignment"]
        
        self.position = None
        self.basicAttackHitCount = 1
        
        self.statusEffects = []
        
        # ========================
        # LOADING STATS
        # ========================
        
        self.health = FractionStatistic("HP", cell_dict["base-stats"]["current-health"],                                cell_dict["base-stats"]["max-health"])
        self.mana = FractionStatistic("MP", cell_dict["base-stats"]["current-mana"],                              cell_dict["base-stats"]["max-mana"])
        
        self.attack = Statistic("Atk", cell_dict["base-stats"]["attack"])
        self.defense = Statistic("Def", cell_dict["base-stats"]["defense"])
        self.intelligence = Statistic("Int", cell_dict["base-stats"]["intelligence"])
        self.resistance = Statistic("Res", cell_dict["base-stats"]["spirit"])
        
        self.critical = PercentileStatistic("Critical", cell_dict["base-stats"]["critical"])
        self.evasion = PercentileStatistic("Evasion", cell_dict["base-stats"]["evasion"])
        
        self.movement = MovementStatistic(cell_dict["base-stats"]["movement"])
        
        self.excessGauge = ExcessGauge(0)
        
        """  !TODO: Reimplement loadEquipment()  """
        #self.loadEquipment(cell_dict)
        
        # ========================
        
        try:
            self.basicAttackRange = cell_dict["equipment"][0]["range"]
        except KeyError:
            self.basicAttackRange = 1
        
        self.hasMoved = False
        self.hasActed = False
        
        self.processed = False # processed flag is used for when a unit has been fully processed for the turn, either automatically (having taken both act and move commands) or manually (by waiting)
    
    def loadEquipment(self, cell_dict):
        self.equipment = cell_dict["equipment"]
        # ! TODO: Remove "equipment" dictionary and make them objects
        
        baCount = 0
        
        # TODO: Load any "on hit" effects / non-statistical bonuses from equipment
        for equip in self.equipment:
            # if the user has multiple weapons, they get that many Basic Attacks
            if equip["type"] == "weapon":
                baCount = baCount + 1
            
            # load up all stat bonuses from each piece of equipment
            for stat in equip["stats"]:
                self.stats[stat] = self.stats[stat] + equip["stats"][stat]
        
        # reload the current health and mana stats just in case they were changed
        # NOTE: This /could/ cause a bug. Keep an eye on whether changing current to reference max causes a problem where both change if one is changed.
        self.stats["current-health"] = self.stats["max-health"]
        self.stats["current-mana"] = self.stats["max-mana"]
        
        # update basic attack count
        if baCount < 1:
            self.basicAttackHitCount = 1
        else:
            self.basicAttackHitCount = baCount
    
    def output(self):
        outStr = str(self.name) + " (" + str(self.profession["name"]) + ")\n" + str(self.health) + "\n" + str(self.mana) + "\n" + str(self.attack) + "\n" + str(self.defense) + "\n" + str(self.intelligence) + "\n" + str(self.resistance) + "\n" + str(self.critical) + "\n" + str(self.evasion) + "\n" + str(self.movement) + "\n" + str(self.excessGauge)
        return outStr
    
    
    """
    #
    # SECTION FOR HELPER METHODS
    #
    """
    
    def getMovementRange(self, grid):
        mov = self.movement.value
        cur = (mov, self.position)
        
        stack = []
        stack.append(cur)
        possible = []
        
        while(stack != []):
            curMov, curPos = stack.pop()
            
            curCell = grid.getCell( curPos )
            
            #If you have 0 moves or more and the current cell is occupiable, then store the current path
            if( (curMov >= 0) and (curCell.properties["occupiable"] == True) and (curCell.occupiedBy == None) and (curCell.position not in possible) ):
                possible.append( curCell.position )
            
            #If the current path ran out of moves or isn't passable, go to the next path
            if( (curMov == 0) or ( (curCell.properties["passable"] == False) ) or ( (curCell.occupiedBy != None) and (curCell.occupiedBy.properties["alignment"] != 0) and (curCell.occupiedBy.properties["alignment"] != self.properties["alignment"]) ) ):
                continue
            
            n = curCell.getNeighbors(grid)
            
            for cell in n:
                stack.append( (curMov - 1, cell.position) )
            
        #possible.remove(self.position)
        return possible # This is a list of valid positions that can be moved to -- does not account for paths to that position
    
    """
    TODO: I'm sure this method could use some heavy optimization... but hey, it's in place
    """
    def getPaths(self, grid, target):
        mov = self.movement.value
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
            if (curPos == target.position) and (curMov >= 0) and (curCell.occupiedBy == None) and (curPath not in possiblePaths):
                possiblePaths.append(curPath)
                continue
            
            #If the current path ran out of moves or isn't passable, go to the next path
            if( (curMov == 0) or (curCell.properties["passable"] == False) or (len(curPath) > mov + 1 ) or ( (curCell.occupiedBy != None) and (curCell.occupiedBy.properties["alignment"] != 0) and (curCell.occupiedBy.properties["alignment"] != self.properties["alignment"]) )):
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
            if cell.occupiedBy != None:
                temp = cell.occupiedBy
                cell.occupiedBy = self
            else:
                cell.occupiedBy = self
                temp = None
            
            # TODO: test statements go in here (traps, passable effects, etc)
            
            # if the cell is not the last step in the path, i.e. the cell we finish on
            # then remove ourself from occupying it
            if(pos != path[-1]):
                print("proceeding movement")
                if(temp != None):
                    cell.occupiedBy = temp
                else:
                    cell.occupiedBy = None
            else:
                print("done")
        
        self.assignPosition(path[-1])
    
    def getActionRange(self, range, grid):
        cur = (range, self.position)
        
        stack = []
        stack.append(cur)
        possible = []
        
        while(stack != []):
            curRange, curPos = stack.pop()
            
            curCell = grid.getCell( curPos )
            
            if( (curRange >= 0) and (curCell.properties["has-stats"] == True or curCell.occupiedBy != None) and (curCell.position not in possible) ):
                possible.append( curCell.position )
            
            if( (curRange == 0) or ( (curCell.properties["block-ranged"] == True) ) ):
                continue
            
            n = curCell.getNeighbors(grid)
            
            for cell in n:
                stack.append( (curRange - 1, cell.position) )
        
        possible.remove(self.position)
        return possible 