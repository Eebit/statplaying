class Cell:
    def __init__(self):
        self.cellName = "Empty Cell"
        self.identifier = "-"
        self.desc = ""
    
    def __str__(self):
        return self.identifier
    
    # helper method to set all flags?
    # for the future? maybe have this method import a Cell's JSON data
    def set_flags(self):
        return True
    
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
        self.width = width
        self.height = height
        
        self.grid = [[Cell() for x in range(width)] for y in range(height)]
    
    def __str__(self):
        out = [[str(self.grid[x][y]) for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])


class GridDisplay:
    def __init__(self, grid):
        self.grid = grid
    
    def __str__(self):
        out = [["{" + str(self.grid.grid[x][y]) + "}" for x in range(self.grid.width)] for y in range(self.grid.height)]
        
        return ('\n').join([' '.join(x) for x in out])

#######################################
# TEST AREA
#######################################

if __name__ == "__main__":
    print("hello world")
    lol = Grid(5, 5)
    print(str(lol))
    
    lul = GridDisplay(lol)
    print(str(lul))