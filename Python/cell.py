class Cell:
    def __init__(self, cell_dict):
        self.properties = cell_dict
        self.occupiedBy = None
            
    def __str__(self):
        return self.properties["cell-id"]
        
    def __repr__(self):
        return str(self)
    
    def output(self):
        if(self.properties["has-stats"] == False):
            outStr = str(self.properties["cell-name"])
        else:
            outStr = str(self.properties["cell-name"] + "\nstats lol")
        return outStr

class Unit(Cell):
    def __init__(self, cell_dict):
        self.properties = cell_dict
        self.position = None
        
        self.loadBaseStats()
        self.basicAttackRange = self.properties["equipment"][0]["range"]
        
        self.hasMoved = False
        self.hasActed = False
        
    def loadBaseStats(self):
        self.stats = self.properties["stats"]
        
    def assignPosition(self, pos):
        self.position = pos
    
    def output(self):
        outStr = str(self.properties["cell-name"]) + " (" + str(self.properties["profession"]["name"]) + ")" +"\nHP:\t\t" + str(self.stats["current-health"]) + "/" + str(self.stats["max-health"]) + "\nMP:\t\t" + str(self.stats["current-mana"]) + "/" + str(self.stats["max-mana"]) + "\nAtk:\t\t" + str(self.stats["attack"]) +"\nDef:\t\t" + str(self.stats["defense"]) + "\nInt:\t\t" + str(self.stats["intelligence"]) + "\nSpr:\t\t" + str(self.stats["spirit"]) + "\nCritical:\t" + str(self.stats["critical"]) + "%" + "\nEvasion:\t" + str(self.stats["evasion"]) + "%" + "\nMovement:\t" + str(self.stats["movement"]) + " Cells" + "\n{/////} {/////} {/////}"
        return outStr