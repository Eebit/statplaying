"""
Will probably use this class to wrap up the interface so it's not all done in the GameState class
"""
class Game:
    def __init__(self):
        self.startUp()
    
    def startUp(self):
        print("=============================================")
        print("=                                           =")
        print("=        STATISTICAL ROLEPLAY ENGINE        =")
        print("=                                           =")
        print("=============================================")
        
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
        pass

