import json
from grid import *
from cell import *
from util import *

class GameState:
    def __init__(self, grid):
        self.grid = grid
        self.turn = 0 # Turn 0 indicates the Placement Phase for each party; no actions/movement
        self.phase = 1 # The Phase corresponds to the team that is to act in increasing order
        
        self.num_teams = 2 # TODO: hardcoded value to be changed as code evolves
        
        self.teams = loadUnits(self.num_teams)
        
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
        
    def select(self, pos):
        if self.grid.getCell(pos).occupiedBy == None:
            print("\n" + self.grid.getCell(pos).output() + "\n")
            
            print("\nAdjacent Cells: " + str(self.grid.getCell(pos).getNeighbors(self.grid)) + "\nDiagonal Cells: " + str(self.grid.getCell(pos).getDiagonals(self.grid)) + "\nSurrounding Cells: " + str(self.grid.getCell(pos).getSurrounding(self.grid)) + "\n")
            
            return self.grid.getCell(pos)
        else:
            print("\n" + self.grid.getCell(pos).occupiedBy.output() + "\n")
            print("\tIS OCCUPYING\n\n")
            print(self.grid.getCell(pos).output() + "\n")
            
            return self.grid.getCell(pos).occupiedBy  
