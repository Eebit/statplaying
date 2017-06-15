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
    commandInput = {
    'b': "",
    'm': "",
    'i': "",
    '1': unit.aSkillList,
    '2': unit.aSkillList,
    '3': unit.aSkillList,
    '4': unit.aSkillList,
    'e': "",
    'x': "",
    }
    
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
        
        # test for printing out an A-Ability
        if(val == '1' or val == '2' or val == '3' or val == '4'):
            i = int(val)
            
            if(i > numAbilities + 1):
                print("Error: Index exceeds number of A-Abilities for this unit")
            else:
                # call for the A-Skill list method
                commandInput[val](unit, i - 1)
        
        # return to command menu if the user declares "Cancel"
        if(val == 'c'):
            return False
    
def skillMenu(unit, index):
    commandInput = {
    'c': "",
    }
    
    numSkills = len(unit.properties["a-ability"][index]["a-skills"])
    
    for a in range(numSkills):
        print("\t\t" + str(unit.properties["a-ability"][index]["a-skills"][a]["skill-name"]).upper() + "\t\t(" + str(a + 1) + ")")
        commandInput[str(a + 1)] = unit.properties["a-ability"][index]["a-skills"][a]
    
    val = input("\nEnter the Value of the A-Skill: ")
    
    if val == c:
        return None
    else:
        try:
            print(commandInput[val]["skill-name"])
        except KeyError:
            print("ERROR: Key " + val + " does not correspond to a valid A-Skill for this unit.")