import cell
import grid
import gameState
import util
import menu

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
            self.state.incrementPhase()
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
        
        print(self.state.teams[ self.state.phase - 1 ])
        
        toProcess = len(self.state.teams[ self.state.phase - 1 ])
        
        for key, unit in self.state.teams[ self.state.phase - 1 ].items():
            print(unit)
            print(unit.properties["cell-name"] + ": " + str(unit.hasActed) + ", " + str(unit.hasMoved) )
        
        while(toProcess > 0):
            print(toProcess)
            
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
                while not u.processed:
                    selection = menu.selectionMenu(u, self.state)
                    
                    if(selection == 'm'):
                        self.movementCommand(u, self.state.grid)
                    elif(selection == 'a'):
                        self.actionCommand(u, self.state.grid)
                    elif(selection == 'w'):
                        self.waitCommand(u)
                    else:
                        break
                    
                    # TODO: Implement support for Free Commands
                    if(u.hasActed == True and u.hasMoved == True):
                        u.processed = True
                        toProcess = toProcess - 1
                    
    
    """
    #
    # SECTION FOR COMMANDS
    #
    """
    
    def movementCommand(self, unit, grid):
        print("Move " + unit.properties["cell-name"])
        
        # output the list of Cells the unit can move to
        l = unit.getMovementRange(grid)
        
        for cell in l:
            print(util.formatOutputCoords(cell), end=", ")
        
        while True:
            # prompt user to select a Cell from the list
            take = input("\n\nSelect a Cell, or type \"cancel\": ")
            
            if take == "cancel":
                return None
            
            t = util.formatInputCoords(take)
            print(t)
            
            # if the user's chosen cell is in the list of cells, then
            if t in l:
                # get all valid paths to the Cell
                paths = unit.getPaths(grid, grid.getCell(t))
                
                if(len(paths) == 0):
                    print("Path Error")
                
                # if multiple paths are presented, then the user must be prompted to choose which specific path they would like to take
                elif(len(paths) > 1):
                    print("Choose the index of the path " + unit.properties["cell-name"] + " should follow: ")
                    paths.sort(key = len)
                    i = 1
                    for path in paths:
                        p = []
                        for pos in path:
                            pstr = util.formatOutputCoords(pos)
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
                            pstr = util.formatOutputCoords(pos)
                            p.append(pstr)
                        chosenPath = path
                    print("->".join(p))
                    break
        
        print("Chosen Path: " + str(chosenPath))
        unit.stepThroughMovement(chosenPath, grid)
        
        #unit.hasMoved = True # mark the unit as having moved
        #return the chosen path so that it can be appended to the game stack?
    
    def actionCommand(self, unit, grid):
        print("Act " + unit.properties["cell-name"])
        
        selection = menu.actionMenu(unit)
        
        if selection == None:
            return None
        else:
            if selection == "ba":
                print(unit.getActionRange(unit.basicAttackRange, self.state.grid))
            
            unit.hasActed = True
        
        """
        l = unit.getNeighbors(grid)
        
        for i in l:
            if(i.occupiedBy != None):
                d = damageFormula(unit, "ba", i.occupiedBy)
        """
    
    def waitCommand(self, unit):
        print("Wait " + unit.properties["cell-name"])
        unit.hasMoved = True
        unit.hasActed = True
        
        return ("w", unit.properties["cell-name"])
        
#######################################
# TEST AREA
#######################################

if __name__ == "__main__":

    g = Game()

    #gs.teamStr()
    

