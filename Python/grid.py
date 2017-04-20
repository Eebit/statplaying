class Cell:
    def __init__(self):
        self.cellName = "Empty Cell"
        self.identifier = " "
        self.desc = ""
    
    def __str__(self):
        return self.identifier
    
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


class Grid:
    def __init__(self, width, height):
        self.width = width # width = number of columns
        self.height = height # height = number of rows
        
        self.grid = []
        for row in range(height):
            rowList = []
            for col in range(width):
                rowList.append(Cell())
            self.grid.append(rowList)
    
    def __str__(self):
        out = []
        
        for row in range(self.height):
            out2 = []
            for col in range(self.width):
                # test if the Cell is an empty cell for printing the "basic" grid
                if(self.grid[row][col].identifier == " "):
                    out2.append("-") # prints a dash for empty cell rather than a space (for visibility)
                else:
                    out2.append(str(self.grid[row][col]))
            out.append(out2)
        
        #out = [[str(self.grid[x][y]) for x in range(self.width)] for y in range(self.height)]
        #out.reverse()
        return '\n'.join([''.join(x) for x in out])