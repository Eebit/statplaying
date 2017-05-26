import json

def loadJson(filepath):
    try:
        with open(filepath) as data_file:
            data = json.load(data_file)
        return data
    except IOError:
        print("Cannot open " + filepath)
        
def loadUnitsUtil():
    # load the team file here

    unitList = {}
    for i in data["team"]: # :^)
        u = Unit(i)
        key = u.properties["cell-name"].casefold()
        unitList[key] = u
    
    return unitList

"""
Utility method that takes an input string in the form of our "grid notation"
and converts it from that notation into a double.

For example, given I5, the method will return (8, 4)
"""
def formatInputCoords(input):
    inputAsList = list(input)
    
    if(len(inputAsList) != 2):
        print("try again")
    elif(not inputAsList[0].isalpha()):
        print("not char")
    elif(not inputAsList[1].isdigit()):
        print("not num")
    else:
        if(inputAsList[0].isupper()):
            row = ord(inputAsList[0]) - 65 # convert from ASCII capital letter char to int
        else:
            row = ord(inputAsList[0]) - 97 # convert from ASCII lowercase letter char to int
                    
        col = int(inputAsList[1]) - 1 # subtract 1 to account for 0 being the first column internally, but 1 externally
        
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