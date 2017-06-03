import json
from grid import *
from cell import *
from util import *
import game

class GameState:
    def __init__(self, grid):
        self.grid = grid
        self.turn = 0 # Turn 0 indicates the Placement Phase for each party; no actions/movement
        self.phase = 1 # The Phase corresponds to the team that is to act in increasing order
        
        self.num_teams = 2 # TODO: hardcoded value to be changed as code evolves
        
        self.teams = loadUnitsUtil(self.num_teams)
        
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
                except KeyError:
                    print("Invalid Unit Key")
            
            
            placed = False
            
            while (placed == False):
                coord = input("Enter Cell position for " + unit.properties["cell-name"] + ": ")
                
                pos = formatInputCoords(coord)
                print(pos)
                
                if(pos != None):
                    placed = self.placeUnit(unit, pos)
                
            placeable = placeable - 1 # decrement the number of placeable units
        
        # Update the Grid afterwards to remove all Starting Zone Cells for that team,
        # changing them to Empty Cells
        
        # print("Remaining Starting Zone Cells:")
        for rowInd, row in enumerate(self.grid.grid):
            for colInd, col in enumerate(row):
                # Checks to see if the team is the one that should be placing units 
                # and whether or not each Cell matches the corresponding Starting Zone
                if(team == self.teams[ self.phase - 1 ]) and (str(self.grid.getCell( (rowInd, colInd) )) == str(self.phase)):
                    # print((rowInd, colInd))
                    self.grid.addEmptyCell( (rowInd, colInd) )
        
        self.incrementPhase()
    
    """
    Method that places the unit on the grid during the placement phase.
    
    Takes the unit to be placed and the position for the unit to be placed at
    as parameters. Returns true if the unit was placed successfully, false otherwise.
    """
    def placeUnit(self, unit, pos):
        if(pos[0] < 0) or (pos[0] >= self.grid.height):
            print("Out of Bounds")
            return False
        if(pos[1] < 0) or (pos[1] >= self.grid.width):
            print("Out of Bounds")
            return False
        
        # Checks:
        # - Is this the placement phase (i.e. Turn == 0)
        # - Can the Cell be occupied? TODO: Maybe check instead if it IS occupied?
        # - Is this Cell a Starting Zone?
        # - Does the unit's team alignment match the Cell's alignment?
        if (self.turn == 0) and (self.grid.getCell(pos).properties["occupiable"] == True) and (self.grid.getCell(pos).properties["cell-name"] == "Starting Zone") and (self.grid.getCell(pos).properties["alignment"] == unit.properties["alignment"]):
            self.grid.addEmptyCell(pos)
            self.grid.grid[ pos[0] ][ pos[1] ].occupiedBy = unit
            unit.assignPosition(pos)
            return True # indicate that the unit was successfully placed on the grid
        else:
            print("Invalid position for placement.")
            return False # indicate that the unit was not placed successfully
    
    def gameplayPhase(self):
        print("\n~ Team " + str(self.phase) + " Phase " + str(self.turn) + " ~\n")
        
        while True:
            while True:
                print(self.grid)
                coord = input("Select coordinate: ")
                pos = formatInputCoords(coord)
                
                if pos == None:
                    print("NoneType")
                elif(pos[0] < 0) or (pos[0] >= self.grid.height):
                    print("Out of Bounds")
                elif(pos[1] < 0) or (pos[1] >= self.grid.width):
                    print("Out of Bounds")
                else:
                    break
            
            u = self.select(pos)
            
            if (type(u) == Unit) and (u.properties["alignment"] == self.phase):
                commandInput = {
                'm': u.movementCommand,
                'a': u.actionCommand,
                'w': u.waitCommand,
                }
                
                while not u.processed:
                    if(u.hasMoved == False):
                        print("\tMOVE\t\t(M)")
                    if(u.hasActed == False):    
                        print("\tACT\t\t(A)")
                    print("\tWAIT\t\t(W)")
                    print("\tCANCEL\t\t(C)")
                
                    i = input("Enter a Command: ")
                    i = i.casefold()
                    
                    if i == "c":
                        break
                    
                    try:
                        if i == 'm' and u.hasMoved == True:
                            print("failure")
                        elif i == 'a' and u.hasActed == True:
                            print("failure")
                        else:
                            commandInput[i](self.grid)
                    except KeyError:
                        print("failure")
                    
                    if(u.hasActed == True and u.hasMoved == True):
                        u.processed = True
    
    def select(self, pos):
        if self.grid.getCell(pos).occupiedBy == None:
            print("\n" + self.grid.getCell(pos).output() + "\n")
            return self.grid.getCell(pos)
        else:
            print("\n" + self.grid.getCell(pos).occupiedBy.output() + "\n")
            return self.grid.getCell(pos).occupiedBy
        
#######################################
# TEST AREA
#######################################

if __name__ == "__main__":
    g = game.Game()
    
    newGrid = Grid(9, 9)
    data = loadJson('cell_bank.json')
    grid_data = read_grid("state_rec_1.txt")
    newGrid.populate_grid_from_file(data, grid_data)
    
    gs = GameState(newGrid)
    print(gs)
    gs.teamStr()
    
    while(gs.turn == 0):
        gs.placementPhase()
        print(gs.grid.gridDisplay())
    
    #print("Yume T1 is at " + str(gs.teams[0]["yume"].position))
    
    while(True):
        gs.gameplayPhase()
        print(gs.grid)
    
