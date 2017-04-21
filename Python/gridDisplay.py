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
        
#######################################
# TEST AREA
#######################################

if __name__ == "__main__":
    print("hello world")
    lol = Grid(9, 9)
    print(str(lol))
    
    with open('cell_bank.json') as data_file:
        data = json.load(data_file)
        
    print(data["global-cells"][2])
    
    # lol this is going to be ugly
    # This is where I add a bunch of Cells to populate my "lol" Grid, based on Recursion's 1.1
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (0,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (0,1))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (1,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (2,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (3,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (4,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (5,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (6,0))
    lol.add_cell(Cell(data["global-cells"][2]["cell-name"], data["global-cells"][2]["cell-id"], ""), (7,0))
    lol.add_cell(Cell(data["global-cells"][3]["cell-name"], data["global-cells"][3]["cell-id"], ""), (8,0))
    
    lul = GridDisplay(lol)
    print(str(lul))
    
    file = open("state_rec_1.txt", "r")
    for line in file:
        line = line.replace("\n", "")
        print(line)
    