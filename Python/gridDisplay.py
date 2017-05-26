import json
from grid import *
from cell import *
from util import *

class GridDisplay:
    def __init__(self, grid):
        self.grid = grid
    
    def __str__(self):
        out = []
        for row in range(self.grid.height):
            
            out2 = []
            for col in range(self.grid.width):
                if(self.grid.grid[row][col].properties["exists"] == True):
                    out2.append("{" + str(self.grid.grid[row][col]) + "}")
                else:
                    out2.append("   ")
            out2.append(chr(row + 65)) # chr(row+65) generates the ASCII char for the capital letter
            out.append(out2)
        out.append(["-" + str(col + 1) + "-" for col in range(self.grid.width)])
        
        return ('\n').join([' '.join(x) for x in out])

#######################################
# TEST AREA
#######################################

if __name__ == "__main__":
    print("hello world")
    newGrid = Grid(9, 9)
    print(str(newGrid))
    
    data = get_cell_data('cell_bank.json')
    
    grid_data = read_grid("state_rec_1.txt")
    print(grid_data)
    
    newGrid.populate_grid_from_file(data, grid_data)
    
    print(newGrid)
    
    display = GridDisplay(newGrid)
    print(str(display))
    
    