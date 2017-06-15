import game
import cell

def selectionMenu(u, state):
    while True:
        if(u.hasMoved == False):
            print("\tMOVE\t\t(M)")
        if(u.hasActed == False):    
            print("\tACT\t\t(A)")
        print("\tWAIT\t\t(W)")
        print("\tCANCEL\t\t(C)")
    
        i = input("Enter a Command: ")
        i = i.casefold()
        
        if i == 'm':
            if u.hasMoved == True:
                print("ERROR: Unit has already moved.")
            else:
                return i
        elif i == 'a':
            if u.hasActed == True:
                print("ERROR: Unit has already acted.")
            else:
                return i
        elif i == "w":
            return i
        elif i == "c":
            return i
        else:
            print("ERROR: Invalid option.")

def actionMenu(unit):
    numAbilities = len(unit.properties["a-ability"])
    
    while True:
        print("\t\tBASIC ATTACK\t\t(B)")
        for a in range(numAbilities):
            print("\t\t" + str(unit.properties["a-ability"][a]["name"]).upper() + "\t\t(" + str(a + 1) + ")")
        print("\t\tCYCLE MANA\t\t(M) \n\t\tITEM\t\t\t(I)")
        if(unit.stats["x-gauge"] >= 0):
            print("\t\tE-Trigger\t\t(E)")
        if(unit.stats["x-gauge"] >= 0):
            print("\t\tX-Ability\t\t(X)")
        print("\t\tCANCEL\t\t\t(C)")
        
        val = input("\nEnter a Command: ")
        val = val.casefold()
        
        if(val == 'b'):
            return "ba"
        
        # test for printing out an A-Ability
        elif(val == '1' or val == '2' or val == '3' or val == '4'):
            i = int(val)
            
            try:
                # call for the A-Skill list method
                return skillMenu(unit, i - 1)
            except IndexError:
                print("Error: Index " + str(i) + " exceeds number of A-Abilities for this unit")
        
        elif(val == 'm'):
            print("TODO: Get Cycle Mana from here!")
            return None
        
        elif(val == 'i'):
            print("TODO: Get Inventory from here!")
            return None
        
        elif(val == 'e'):
            if(unit.stats["x-gauge"] >= 10):
                print("E-Trigger!")
                return None
            else:
                print("No E-Trigger!")
        
        elif(val == 'x'):
            if(unit.stats["x-gauge"] >= 20):
                print("X-Ability!")
                return None
            else:
                print("No X-Ability!")
        
        # return to command menu if the user declares "Cancel"
        elif(val == 'c'):
            return None
    
def skillMenu(unit, index):
    numSkills = len(unit.properties["a-ability"][index]["a-skills"])
    
    for a in range(numSkills):
        print("\t\t" + str(unit.properties["a-ability"][index]["a-skills"][a]["skill-name"]).upper() + "\t\t(" + str(a + 1) + ")")
    
    val = input("\nEnter the Value of the A-Skill: ")
    
    if val == "c":
        return None
    else:
        try:
            print(unit.properties["a-ability"][index]["a-skills"][int(val) - 1]["skill-name"])
            return unit.properties["a-ability"][index]["a-skills"][int(val) - 1] # return the A-Skill selected from the menu
            #TODO: Call a "target selection" method from here
        except KeyError:
            print("ERROR: Key " + val + " does not correspond to a valid A-Skill for this unit.")