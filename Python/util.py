import json
import random
import os
import copy

import cell

def loadJson(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
        return data
    except IOError:
        print("Cannot open " + filepath)
        
def loadUnits(numTeams):
    unitFiles = os.listdir("units")
    teamList = [] # a list of dictionaries that contain the units
    
    # create the number of dictionaries needed to store each team
    for i in range(numTeams):
        teamList.append({})
    
    for file in unitFiles:
        # load all JSON files in the current directory
        unitData = loadJson("units/" + file)
        
        try:
            # handler for situations when multiple units inherit from the same JSON
            if(type(unitData["cell-name"]) == list):
                for i in range(len(unitData["cell-name"])):
                    copiedData = copy.deepcopy(unitData)
                    
                    copiedData["cell-name"] = unitData["cell-name"][i]
                    copiedData["cell-id"] = unitData["cell-id"][i]
                    
                    u = cell.Unit(copiedData)
                    key = u.name.casefold()
            
                    team = teamList[ unitData["alignment"] - 1 ]
                    team[key] = u
            # single unit generated from single JSON
            else:
                u = cell.Unit(unitData)
                key = u.name.casefold()
        
                team = teamList[ unitData["alignment"] - 1 ]
                team[key] = u
        except KeyError:
            print("Error loading JSON file: " + file + " . Potentially improper Unit format?")

    
    return teamList

"""
Utility method that takes an input string in the form of our "grid notation"
and converts it from that notation into a double.

For example, given I5, the method will return (8, 4)
"""
def formatInputCoords(input):
    inputAsList = list(input)
    
    if( (len(inputAsList) < 2) or (len(inputAsList) > 3) ):
        print("try again")
        return None
    else:
        if(len(inputAsList) == 2):
            if(not inputAsList[0].isalpha()):
                print("not char")
                return None
            elif(not inputAsList[1].isdigit()):
                print("not num")
                return None
            else:
                if(inputAsList[0].isupper()):
                    row = ord(inputAsList[0]) - 65 # convert from ASCII capital letter char to int
                else:
                    row = ord(inputAsList[0]) - 97 # convert from ASCII lowercase letter char to int
                            
                col = int(inputAsList[1]) - 1 # subtract 1 to account for 0 being the first column internally, but 1 externally
        else:
            if(not inputAsList[0].isalpha()):
                print("not char")
                return None
            elif( (not inputAsList[1].isdigit()) or (not inputAsList[2].isdigit()) ):
                print("not num")
                return None
            else:
                if(inputAsList[0].isupper()):
                    row = ord(inputAsList[0]) - 65 # convert from ASCII capital letter char to int
                else:
                    row = ord(inputAsList[0]) - 97 # convert from ASCII lowercase letter char to int
                
                colStr = (inputAsList[1] + inputAsList[2])
                col = int(colStr) - 1 # subtract 1 to account for 0 being the first column internally, but 1 externally
        
        return (row, col)

"""
Utility method that takes a double as input and converts it to conventional
statplaying "grid notation".

For example, given (8, 4), the method will return I5
"""
def formatOutputCoords(input):
    if len(input) != 2:
        print("Invalid tuple value")
        return None
    else:
        row = str(chr(input[0] + 65))
        col = input[1] + 1
                
        return row + str(col)
        
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
        
def damageFormula(source, action, target):
    if(action == "ba"):
        print("basic attack")
        basicAttackType = source.properties["profession"]["ba-type"]
        
        if(basicAttackType == 0):
            print("physical")
            attackingStat = source.stats["attack"]
            defendingStat = target.stats["defense"]
            
        elif(basicAttackType == 1):
            print("magical")
            attackingStat = source.stats["intelligence"]
            defendingStat = target.stats["spirit"]
            
        else:
            print("undefined, default to physical")
            attackingStat = source.stats["attack"]
            defendingStat = target.stats["defense"]
        
        accuracyChance = random.randint(0, 100)
        #if(accuracyChance > source.stats["accuracy"]):
        if(accuracyChance > 100):
            print("accuracy miss")
            return None
        
        criticalChance = random.randint(0, 100)
        if(criticalChance <= source.stats["critical"]):
            print("critical hit")
            criticalHit = True
            baseModifier = 1.5
        else:
            criticalHit = False
            baseModifier = 1.0
        
        evade = random.randint(0, 100)
        if(evade <= target.stats["evasion"]):
            print("evasion dodge")
            return None
        else:
            # Base Damage = Attacking_Stat * Damage_Output
            baseDamage = attackingStat * 1.0
            
            # Protection Value is the value of defense plus any other mitigations that aren't necessarily modifiers
            protectionValue = defendingStat
            
            totalModifier = 1.0
            
            #Total Damage = ( ( Base_Damage * Base_Damage_Modifiers ) - Protection Value ) * Total Damage Modifiers
            totalDamage = ( ( baseDamage * baseModifier ) - protectionValue ) * totalModifier
            
            if(totalDamage < 1):
                print("scratch damage")
                totalDamage = 1
            else:
                round(totalDamage, 0)
                int(totalDamage)
                
            print("Total Damage: " + str(totalDamage))
            return totalDamage