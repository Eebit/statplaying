import json
from grid import *

def loadUnits(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
            
        unitList = {}
        for i in data["team"]: # :^)
            u = Unit(i)
            key = u.properties["cell-name"]
            unitList[key] = u
        
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
        
        teamsList = []
        
        for i in range(len(self.teams)):
            teamStr = "team" + str(i + 1) + "\n"
            for key, value in self.teams[i].items():
                ("\n").join((teamStr, value.properties["cell-name"]))
            teamsList.append(teamStr)
        
        # TODO: Currently, teamsList doesn't actually print out the teams.
        # It only prints out [team1, team2]. The next step will be to properly output
        # the list of Units on each team.
        state = (turnInfo, str(self.grid), str(self.num_teams), str(teamsList))
        
        return ('\n;\n').join(state)
    
    def incrementPhase(self):
        if(self.phase + 1 % self.num_teams == 0):
            self.turn = self.turn + 1
            self.phase = 1
        else:
            self.phase = self.phase + 1
    
    def placementPhase(self, team):
        for key, value in team.items():
            print(key)
            print(value)
            
            placed = False
            
            while (placed == False):
                coord = input("Enter Cell position for " + value.properties["cell-name"] + ": ")
                
                pos = formatInputCoords(coord)
                print(pos)
                
                if(pos != None):
                    placed = self.placeUnit(value, pos)
        
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
    
    gs.placementPhase(gs.teams[0])
    
    
    print([Unit for Unit in gs.teams[0]])
    
    print(gs)
