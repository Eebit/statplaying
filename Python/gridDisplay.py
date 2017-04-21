import json
from grid import *

class GridDisplay:
    def __init__(self, grid):
        self.grid = grid
    
    def __str__(self):
        out = []
        for row in range(self.grid.height):
            
            out2 = []
            for col in range(self.grid.width):
                out2.append("{" + str(self.grid.grid[row][col]) + "}")
            out2.append(chr(row + 65)) # chr(row+65) generates the ASCII char for the capital letter
            out.append(out2)
        out.append(["-" + str(col + 1) + "-" for col in range(self.grid.width)])
        
        return ('\n').join([' '.join(x) for x in out])

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
    
    