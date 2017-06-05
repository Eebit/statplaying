import cell
import grid
import gameState
import util

"""
Will probably use this class to wrap up the interface so it's not all done in the GameState class
"""
class Game:
    def __init__(self):
        self.startUp()
        
        self.run()
    
    def startUp(self):
        print("=============================================")
        print("=                                           =")
        print("=        STATISTICAL ROLEPLAY ENGINE        =")
        print("=                                           =")
        print("=============================================")
        
        print("\n\n[1] - New Game\n[2] - Load Existing Game State")
        
        while True:
            i = input(">")
            
            if(i == "1"):
                newGrid = grid.Grid(9, 9)
                data = util.loadJson('cell_bank.json')
                grid_data = util.read_grid("state_rec_1.txt")
                newGrid.populate_grid_from_file(data, grid_data)
                
                self.state = gameState.GameState(newGrid)
                print(self.state)
                
                break
            elif(i == "2"):
                print(":)")
                break
            else:
                print("Try again")
        # TODO: get input from player to determine whether they want to:
        #   -> Start a new game
        #       --- GM Mode or Play Mode?
        #       --- GM Mode => Simulate one phase of the game and serialize
        #   -> Load from a predetermined GameState file
        
        # TODO: Implement different game TYPES, such as ShadowSystem, Masqplays, etc.
    
    def load(self):
        pass
        
    def save(self):
        pass
    
    def run(self):
        while(self.state.turn == 0):
            print(self.state.grid.gridDisplay())
            self.placementPhase()
        
        while(True):
            self.gameplayPhase()
            print(self.state.grid.gridDisplay())

    def placementPhase(self):
        team = self.state.teams[ self.state.phase - 1 ]
        
        print("\n~ Team " + str(self.state.phase) + " Placement Phase ~\n")
        
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
                
                pos = util.formatInputCoords(coord)
                #print(pos)
                
                if(pos != None):
                    placed = self.state.placeUnit(unit, pos)
                
            placeable = placeable - 1 # decrement the number of placeable units
        
        # Update the Grid afterwards to remove all Starting Zone Cells for that team,
        # changing them to Empty Cells
        
        # print("Remaining Starting Zone Cells:")
        for rowInd, row in enumerate(self.state.grid.grid):
            for colInd, col in enumerate(row):
                # Checks to see if the team is the one that should be placing units 
                # and whether or not each Cell matches the corresponding Starting Zone
                if(team == self.state.teams[ self.state.phase - 1 ]) and (str(self.state.grid.getCell( (rowInd, colInd) )) == str(self.state.phase)):
                    # print((rowInd, colInd))
                    self.state.grid.addEmptyCell( (rowInd, colInd) )
        
        self.state.incrementPhase()

    def gameplayPhase(self):
        print("\n~ Team " + str(self.state.phase) + " Phase " + str(self.state.turn) + " ~\n")
        
        while True:
            
            # Loop for getting coordinate selection
            # TODO: Add a selection method by unit name (or identifier?) as well as by coordinate
            while True:
                print(self.state.grid.gridDisplay())
                coord = input("Select coordinate: ")
                pos = util.formatInputCoords(coord)
                
                if pos == None:
                    print("NoneType")
                elif(pos[0] < 0) or (pos[0] >= self.state.grid.height):
                    print("Out of Bounds")
                elif(pos[1] < 0) or (pos[1] >= self.state.grid.width):
                    print("Out of Bounds")
                else:
                    break
            
            u = self.state.select(pos)
            
            if (type(u) == cell.Unit) and (u.properties["alignment"] == self.state.phase):
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
                            commandInput[i](self.state.grid)
                    except KeyError:
                        print("failure")
                    
                    if(u.hasActed == True and u.hasMoved == True):
                        u.processed = True

        
#######################################
# TEST AREA
#######################################

if __name__ == "__main__":

    g = Game()

    #gs.teamStr()
    

