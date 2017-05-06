import json
from grid import *

def loadUnits(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
            
        unitList = []
        for i in data["team"]: # :^)
            unitList.append(Cell(i))
        
        return unitList
    except IOError as e:
        print("Cannot open " + filepath)

"""
Method that takes an input string in the form of our "grid notation"
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
        turnInfo = ('.').join(turnInfo)
    
        state = (turnInfo, "", str(self.grid))
        return ('\n').join(state)
    
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
            while True:
                var = input("Enter Cell position for " + team[i].properties["cell-name"] + ": ")
                
                pos = formatInputCoords(var)
                print(pos)
                
                if(pos != None):
                    self.placeUnit(team[0], pos)
                    break
            
    
    """
    Method that places the unit on the grid during the placement phase.
    
    Takes the unit to be placed and the position for the unit to be placed at
    as parameters.
    """
    def placeUnit(self, unit, pos):
        row, col = pos[0], pos[1]
        
        if (self.turn == 0) and (self.grid.grid[row][col].properties["occupiable"] == True):
            self.grid.grid[row][col] = unit
        else:
            print("oops no can do")

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
    