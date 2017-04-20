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
    
    lul = GridDisplay(lol)
    print(str(lul))