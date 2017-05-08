import json
from grid import *

def loadUnits(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
            
        unitList = []
        for i in data["team"]: # :^)
            unitList.append(Unit(i))
        
        return unitList
    except IOError as e:
        print("Cannot open " + filepath)

"""
Utility method that takes an input string in the form of our "grid notation"
and converts it from that notation into a double.

For example, given I5, the method will return (8, 4)
"""
def formatInputCoords(input):
    inputAsList = list(input)
    
    if(len(inputAsList) != 2):
        print("try again")
    elif(not inputAsList[0].isalpha()):
        print("not char")
    elif(not inputAsList[1].isdigit()):
        print("not num")
    else:
        if(inputAsList[0].isupper()):
            row = ord(inputAsList[0]) - 65 # convert from ASCII capital letter char to int
        else:
            row = ord(inputAsList[0]) - 97 # convert from ASCII lowercase letter char to int
                    
        col = int(inputAsList[1]) - 1 # subtract 1 to account for 0 being the first column internally, but 1 externally
                    
        pos = (row, col)
        return pos
    

class GameState:
    def __init__(self, grid):
        self.grid = grid
        self.turn = 0 # Turn 0 indicates the Placement Phase for each party; no actions/movement
        self.phase = 1 # The Phase corresponds to the team that is to act in increasing order
        
        self.num_teams = 2 # TODO: hardcoded value to be changed as code evolves
        
        # TODO: Fix these hardcoded values and load files based on the number of teams initialized
        self.team1 = loadUnits('units/team1.json')
        self.team2 = loadUnits('units/team2.json')
    
    def __str__(self):
        turnInfo = (str(self.turn), str(self.phase))
        turnInfo = ('\n').join(turnInfo)
    
        state = (turnInfo, str(self.grid), str(self.num_teams), str(self.team1), str(self.team2))
        return ('\n;\n').join(state)
    
    def incrementPhase(self):
        if(self.phase + 1 % self.num_teams == 0):
            self.turn = self.turn + 1
            self.phase = 1
        else:
            self.phase = self.phase + 1
    
    def placementPhase(self, team):
        for i, unit in enumerate(team):
            print(i)
            print(unit)
            
            placed = False
            
            while (placed == False):
                coord = input("Enter Cell position for " + team[i].properties["cell-name"] + ": ")
                
                pos = formatInputCoords(coord)
                print(pos)
                
                if(pos != None):
                    placed = self.placeUnit(team[i], pos)
        
        #TODO (WIP): Update the Grid afterwards to remove all Starting Zone Cells for that team
        #changing them to Empty Cells
        print("Remaining Starting Zone Cells:")
        for rowInd, row in enumerate(self.grid.grid):
            for colInd, col in enumerate(row):
                if(team == self.team1) and (str(self.grid.grid[rowInd][colInd]) == "1"):
                    print((rowInd, colInd))
        
        self.incrementPhase()
    
    """
    Method that places the unit on the grid during the placement phase.
    
    Takes the unit to be placed and the position for the unit to be placed at
    as parameters. Returns true if the unit was placed successfully, false otherwise.
    """
    def placeUnit(self, unit, pos):
        row, col = pos[0], pos[1]
        
        # Checks:
        # - Is this the placement phase (i.e. Turn == 0)
        # - Can the Cell be occupied? TODO: Maybe check instead if it IS occupied?
        # - Is this Cell a Starting Zone?
        # - Does the unit's team alignment match the Cell's alignment?
        if (self.turn == 0) and (self.grid.grid[row][col].properties["occupiable"] == True) and (self.grid.grid[row][col].properties["cell-name"] == "Starting Zone") and (self.grid.grid[row][col].properties["alignment"] == unit.properties["alignment"]):
            """
            # TODO: Do not destructively place the unit on the grid (overwriting the cell); 
            # instead the unit should be stored with a pointer to the Cell it is placed at
            # and the Cell's is-occupied should be updated to indicate what is occupying it
            """
            
            self.grid.grid[row][col] = unit 
            return True # indicate that the unit was successfully placed on the grid
        else:
            print("Invalid position for placement.")
            return False # indicate that the unit was not placed successfully

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
    
    gs.placementPhase(gs.team1)
    
    
    print([Cell for Cell in gs.team1])
    
    print(gs)
    