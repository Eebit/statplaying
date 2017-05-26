import json
from cell import *
from util import *

def get_cell_data(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
        return data
    except IOError as e:
        print("Cannot open " + filepath)
        
"""
Method that takes a filepath to a valid Grid *.txt file as its parameter,
then reads it character by character and parses that into a list of lists
for easy Grid construction.
"""
def read_grid(filepath):
    # read a grid from a txt file and use that to populate our grid
    try:
        file = open(filepath, "r")
        list = []
        list2 = []
        
        # loops until it sees that there is no further characters available, i.e. hits EOF 
        while True:
            # read in each byte at a time
            ch = file.read(1)
            
            # hits EOF
            if not ch:
                list.append(list2) # append the last inner list before breaking
                break
            
            # if it sees a newline char, it terminates the inner list and appends it to the outer list
            elif(ch == "\n"):
                list.append(list2)
                list2 = [] # restart the inner list
            
            else:
                list2.append(ch)
        return list
        
    except IOError as e:
        print("Cannot open " + filepath)
        return []

class Grid:
    def __init__(self, width, height):
        self.width = width # width = number of columns
        self.height = height # height = number of rows
        
        self.d = get_cell_data('cell_bank.json')
        
        d = self.d
        
        self.grid = []
        for row in range(height):
            rowList = []
            for col in range(width):
                rowList.append(Cell(d["global-cells"][0]))
            self.grid.append(rowList)
        
    
    def __str__(self):
        out = []
        
        for row in range(self.height):
            out2 = []
            for col in range(self.width):
                if(self.grid[row][col].occupiedBy != None):
                    out2.append(str(self.grid[row][col].occupiedBy))
                else:
                    # test if the Cell is an empty cell for printing the "basic" grid
                    if(self.grid[row][col].properties["cell-id"] == " "):
                        if(self.grid[row][col].properties["exists"] == True):
                            out2.append("-") # prints a dash for empty cell rather than a space (for visibility)
                        else:
                            out2.append(" ")
                    else:
                        out2.append(str(self.grid[row][col]))
            out.append(out2)
        
        return '\n'.join([''.join(x) for x in out])
    
    
    """
    Method that takes a Cell and adds it to the specified location 
    (as a tuple; (row,col)) on the Grid.
    """
    def add_cell(self, cell, location):
        self.grid[location[0]][location[1]] = cell
    
    def addEmptyCell(self, location):
        self.grid[location[0]][location[1]] = Cell(self.d["global-cells"][0])
    
    """
    Iterate over the grid_data list of lists returned by read_grid()
    """
    def populate_grid_from_file(self, data, grid_data):
        for list in range(len(grid_data)):
            for cell in range(len(grid_data[list])):
                found = False # set our "found" flag to false over each new symbol
                
                # iterate through the currently-defined Cell Database JSON file (passed as "data")
                for x in range(len(data["global-cells"])):
                    # if we hit the "null" in the array, break the loop; no Cell defined
                    if not data["global-cells"][x]:
                        break
                    
                    """
                    # !!!! TEMPORARY !!!!
                    # handler for the nonexistent cell
                    """
                    if(grid_data[list][cell] == " "):
                        self.add_cell(Cell(data["global-cells"][1]), (list,cell))
                        found = True
                        break
                    """
                    # !!!! End of Temporary !!!!
                    """
                    
                    # if the grid_data char is the empty cell, we modify its symbol so that we can parse it properly
                    if(grid_data[list][cell] == "-"):
                        grid_data[list][cell] = " "
                    
                    # if the current symbol is equal to something in our database, we add it to the grid
                    # using its current coordinates (i.e. the index of the array)
                    if(grid_data[list][cell] == data["global-cells"][x]["cell-id"]):
                        self.add_cell(Cell(data["global-cells"][x]), (list,cell))
                        found = True
                        break # break the loop so we don't keep looking after adding
                
                if(found == False):
                    print("Could not find data for {" + grid_data[list][cell] + "} in JSON cell bank.")
    
    
    def getCell(self, coord):
        try:
            cell = self.grid[coord[0]][coord[1]]
        except IndexError:
            cell = None
            print("Coordinate was not in bounds")
        
        return cell