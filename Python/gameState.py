import json
from grid import *
from cell import *
from util import *

def loadUnits(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
            
        unitList = {}
        for i in data["team"]: # :^)
            u = Unit(i)
            key = u.properties["cell-name"].casefold()
            unitList[key] = u
        
        return unitList
    except IOError as e:
        print("Cannot open " + filepath)

class GameState:
    def __init__(self, grid):
        self.grid = grid
        self.turn = 0 # Turn 0 indicates the Placement Phase for each party; no actions/movement
        self.phase = 1 # The Phase corresponds to the team that is to act in increasing order
        
        self.num_teams = 2 # TODO: hardcoded value to be changed as code evolves
        
        self.teams = []
        
        for i in range(self.num_teams):
            # TODO: Replace "team#.json" with the loading of individual units
            team = loadUnits("units/team" + str(i + 1) + ".json")
            self.teams.append(team)
        
    """
    Method for formatting the GameState information. 
    """
    def __str__(self):
        turnInfo = (str(self.turn), str(self.phase))
        turnInfo = ('\n').join(turnInfo)
        
        teamsList = self.teamStr()
        state = (turnInfo, str(self.grid), str(self.num_teams), teamsList)
        
        return ('\n;\n').join(state)
       
    """
    Helper method to declutter the __str__ method. Constructs a list of
    units by team and outputs it as a string.
    """
    def teamStr(self):
        strList = []
        for i in range(len(self.teams)):
            strList.append("team" + str(i + 1))
            for key, value in self.teams[i].items():
                strList.append(str((key, value)))
            
            strList.append(";")
        return ("\n").join(strList)
    
    def incrementPhase(self):
        if(self.phase % self.num_teams == 0):
            self.turn = self.turn + 1
            self.phase = 1
        else:
            self.phase = self.phase + 1
    
    def placementPhase(self):
        team = self.teams[ self.phase - 1 ]
        
        placeable = len(team.keys()) # The number of units on this team that can be placed (that is, all of them)
        
        while(placeable > 0):
            print("Available Units for Placement:")
            for k in team.keys():
                if team[k].position == None:
                    print(k)
            
            # Loop the input state until the user provides a valid key as an identifier
            while True:
                u = input("Select a Unit for Placement: ")
                u = u.casefold()
                
                try:
                    unit = team[u]
                    break
                except KeyError as e:
                    print("didn't work")
            
            
            placed = False
            
            while (placed == False):
                coord = input("Enter Cell position for " + unit.properties["cell-name"] + ": ")
                
                pos = formatInputCoords(coord)
                print(pos)
                
                if(pos != None):
                    placed = self.placeUnit(unit, pos)
                
            placeable = placeable - 1 # decrement the number of placeable units
        
        #TODO (WIP): Update the Grid afterwards to remove all Starting Zone Cells for that team
        #changing them to Empty Cells
        print("Remaining Starting Zone Cells:")
        for rowInd, row in enumerate(self.grid.grid):
            for colInd, col in enumerate(row):
                #TODO: Replace hardcoded team variables for general versions
                if(team == self.teams[0]) and (str(self.grid.grid[rowInd][colInd]) == "1"):
                    print((rowInd, colInd))
        
        self.incrementPhase()
    
    """
    Method that places the unit on the grid during the placement phase.
    
    Takes the unit to be placed and the position for the unit to be placed at
    as parameters. Returns true if the unit was placed successfully, false otherwise.
    """
    def placeUnit(self, unit, pos):
        row, col = pos[0], pos[1]
        
        if(row < 0) or (row >= self.grid.height):
            print("Out of Bounds")
            return False
        if(col < 0) or (col >= self.grid.width):
            print("Out of Bounds")
            return False
        
        # Checks:
        # - Is this the placement phase (i.e. Turn == 0)
        # - Can the Cell be occupied? TODO: Maybe check instead if it IS occupied?
        # - Is this Cell a Starting Zone?
        # - Does the unit's team alignment match the Cell's alignment?
        if (self.turn == 0) and (self.grid.grid[row][col].properties["occupiable"] == True) and (self.grid.grid[row][col].properties["cell-name"] == "Starting Zone") and (self.grid.grid[row][col].properties["alignment"] == unit.properties["alignment"]):
            self.grid.addEmptyCell((row, col))
            self.grid.grid[row][col].occupiedBy = unit
            unit.assignPosition((row,col))
            return True # indicate that the unit was successfully placed on the grid
        else:
            print("Invalid position for placement.")
            return False # indicate that the unit was not placed successfully
    
    def gameplayPhase(self):
        print("\n~ Team " + str(self.phase) + " Phase " + str(self.turn) + " ~\n")
        
        while True:
            while True:
                coord = input("Select coordinate: ")
                pos = formatInputCoords(coord)
                
                if(pos[0] < 0) or (pos[0] >= self.grid.height):
                    print("Out of Bounds")
                elif(pos[1] < 0) or (pos[1] >= self.grid.width):
                    print("Out of Bounds")
                else:
                    break
            
            u = self.select(pos)
            
            if (type(u) == Unit) and (u.properties["alignment"] == self.phase):
                commandInput = {
                'm': self.movementCommand,
                'a': self.actionCommand,
                'w': self.waitCommand,
                'c': None
                }
                
                while True:
                    if(u.hasMoved == False):
                        print("\tMOVE\t\t(M)")
                    if(u.hasActed == False):    
                        print("\tACT\t\t(A)")
                    print("\tWAIT\t\t(W)")
                    print("\tCANCEL\t\t(C)")
                
                    i = input()
                    i = i.casefold()
                    try:
                        commandInput[i](u)
                    except KeyError:
                        print("failure")
    
    def movementCommand(self, unit):
        print("Move " + unit.properties["cell-name"])
        
    def actionCommand(self, unit):
        print("Act " + unit.properties["cell-name"])
        
    def waitCommand(self, unit):
        print("Wait " + unit.properties["cell-name"])
        unit.hasMoved = True
        unit.hasActed = True
    
    def select(self, pos):
        if self.grid.grid[pos[0]][pos[1]].occupiedBy == None:
            print(self.grid.grid[pos[0]][pos[1]].output())
            return self.grid.grid[pos[0]][pos[1]]
        else:
            print(self.grid.grid[pos[0]][pos[1]].occupiedBy.output())
            return self.grid.grid[pos[0]][pos[1]].occupiedBy

"""
Will probably use this class to wrap up the interface so it's not all done in the GameState class
"""
class Game:
    def __init__(self):
        pass
        
#######################################
# TEST AREA
#######################################

if __name__ == "__main__":
    newGrid = Grid(9, 9)
    data = get_cell_data('cell_bank.json')
    grid_data = read_grid("state_rec_1.txt")
    newGrid.populate_grid_from_file(data, grid_data)
    
    
    gs = GameState(newGrid)
    print(gs)
    gs.teamStr()
    
    print("\n")
    print(formatOutputCoords( (1, 8) ))
    
    print(gs.grid.getCell( (1, 8) ))
    print(gs.grid.getCell( (0, 10) ))
    
    while(gs.turn == 0):
        gs.placementPhase()
        print(gs.grid)
    
    #print("Yume T1 is at " + str(gs.teams[0]["yume"].position))
    
    while(True):
        gs.gameplayPhase()
        print(gs.grid)
    
