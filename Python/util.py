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