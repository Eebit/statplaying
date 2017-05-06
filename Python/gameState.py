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
    
    
    while True:
        var = input("Enter Cell position for " + gs.team1[0].properties["cell-name"] + ": ")
        
        varList = list(var)
        
        if(len(varList) != 2):
            print("try again")
        elif(not varList[0].isalpha()):
            print("not char")
        elif(not varList[1].isdigit()):
            print("not num")
        else:
            
            # snippet to convert from our grid notation (i.e. I5) to a double, e.g. (8, 4)
            if(varList[0].isupper()):
                row = ord(varList[0]) - 65
            else:
                row = ord(varList[0]) - 97
            
            col = ord(varList[1]) - 49
            
            pos = (row, col)
            print(pos)
            break
    
    print([Cell for Cell in gs.team1])
    gs.placeUnit(gs.team1[0], pos)
    print(gs)
    