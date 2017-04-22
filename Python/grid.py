import json

def get_cell_data(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
        return data
    except IOError as e:
        print("Cannot open " + filepath)


class Cell:
    def __init__(self, cell_dict):
        self.properties = cell_dict
        
        #self.cellName = name
        #self.identifier = id
        #self.desc = desc
        
    
    def __str__(self):
        return self.properties["cell-id"]
    
    """
    def set_exists(self):
        self.exists = True
    
    def set_passable(self):
        self.passable = True
    
    def set_occupiable(self):
        self.occupiable = True
    
    def set_destructable(self):
        self.destructable = False
    
    def set_block_property(self):
        self.blockProperty = False
    
    def set_has_stats(self):
        self.hasStats = False
    """


class Grid:
    def __init__(self, width, height):
        self.width = width # width = number of columns
        self.height = height # height = number of rows
        
        d = get_cell_data('cell_bank.json')
        
        self.grid = []
        for row in range(height):
            rowList = []
            for col in range(width):
                rowList.append(Cell(d["global-cells"][0]))
            self.grid.append(rowList)
        
        #self.add_cell(Cell("lol", "l", ""), (2,4))
        #self.grid[2][4] = Cell("lol", "l", "")
    
    def __str__(self):
        out = []
        
        for row in range(self.height):
            out2 = []
            for col in range(self.width):
                # test if the Cell is an empty cell for printing the "basic" grid
                if(self.grid[row][col].properties["cell-id"] == " "):
                    out2.append("-") # prints a dash for empty cell rather than a space (for visibility)
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
    
    # iterate over the grid_data list of lists returned by read_grid()
    def populate_grid_from_file(self, data, grid_data):
        for list in range(len(grid_data)):
            for cell in range(len(grid_data[list])):
                found = False # set our "found" flag to false over each new symbol
                #print("trying " + str(grid_data[list][cell]) + " at (" + str(list) + ", " + str(cell) + "):")
                
                # iterate through the currently-defined Cell Database JSON file (passed as "data")
                for x in range(len(data["global-cells"])):
                    # if we hit the "null" in the array, break the loop; no Cell defined
                    if not data["global-cells"][x]:
                        break
                    # if the grid_data char is the empty cell, we modify its symbol so that we can parse it properly
                    if(grid_data[list][cell] == "-"):
                        grid_data[list][cell] = " "
                    # if the current symbol is equal to something in our database, we add it to the grid
                    # using its current coordinates (i.e. the index of the array)
                    if(grid_data[list][cell] == data["global-cells"][x]["cell-id"]):
                        self.add_cell(Cell(data["global-cells"][x]), (list,cell))
                        found = True
                
                if(found == False):
                    print("Could not find data for {" + grid_data[list][cell] + "} in JSON cell bank.")
        