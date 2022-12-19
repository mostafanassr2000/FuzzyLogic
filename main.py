from FuzzyLogic import FuzzyLogic
from parsing.Parser import Parser
from data import addAll

# Global fuzzy object
fuzzyLogic: FuzzyLogic = FuzzyLogic()

# Global parser object
parser: Parser = Parser()

def addVariables():
    print("Enter the variable’s name, type (IN/OUT) and range ([lower, upper]): (Press x to finish)")
    varLine = input()

    if (type(varLine) is not str):
        print(invalidInput())
        mainMenu()

    if (varLine != 'x'):
        var = parser.parseVariableLine(varLine)
        if (var):
            # add variables
            fuzzyLogic.addVariable(var)
            addVariables()
        else:
            # invalid input
            #fuzzyLogic.variables = []
            print(invalidInput())
            mainMenu()
    else:
        mainMenu()

def addFuzzySets(varName):
    print("Enter the fuzzy set name, type (TRI/TRAP) and values: (Press x to finish)")
    setLine = input()

    if (type(setLine) is not str):
        print(invalidInput())
        mainMenu()

    if (setLine != 'x'):
        set = parser.parseSetLine(setLine)
        if (set):
            # add sets to an existing variable
            fuzzyLogic.addSetToExistingVariable(set)
            addFuzzySets(varName)
        else:
            # invalid input
            print(invalidInput())
            mainMenu()
    else:
        print(fuzzyLogic.getAllVariables())
        mainMenu()

def variableSetsHandler():
    print("Enter the variable’s name:")
    print("--------------------------")
    varName = input()
    # check variable name existence
    if (not(fuzzyLogic.checkVariableName(varName))):
        print(notFound('variable name'))
        mainMenu()
    addFuzzySets(varName)

def addRules():
    print("Enter the rules in this format: (Press x to finish)")
    print("IN_variable set operator IN_variable set => OUT_variable set")
    print("------------------------------------------------------------")
    ruleLine = input()
  
    if (type(ruleLine) is not str):
        print(invalidInput())
        mainMenu()

    if (ruleLine != 'x'):
        rule = parser.parseRuleLine(ruleLine, fuzzyLogic)
        if (rule):
            # add rules
            fuzzyLogic.addRule(rule)
            addRules()
        else:
            # invalid input
            print(invalidInput())
            mainMenu()
    else:
        print(fuzzyLogic.getRules())
        mainMenu()

def runSimulation():
    if not(fuzzyLogic.canRunSimulation()):
        print("CAN’T START THE SIMULATION! Please add the fuzzy sets and rules first.")
        mainMenu()

    print("Enter the crisp values:")
    print("-----------------------")
    
    for var in fuzzyLogic.variables:
        if var['type'] == 'IN':
            varCrispValue = input(f"{var['name']}: ")
            var['crispValue'] = int(varCrispValue)

    print("Running the simulation…")
    print(fuzzyLogic.runSimulation())
    mainMenu()
    
# main menu
def mainMenu():
    print("Main Menu:")
    print("==========")
    print("1- Add variables.")
    print("2- Add fuzzy sets to an existing variable.")
    print("3- Add rules.")
    print("4- Run the simulation on crisp values.")
    print("5- Add inputs from data file")
    print("6- Back")
    choice = input()
    
    match choice:
        case '1':
            addVariables()
        case '2':
            variableSetsHandler()
        case '3':
            addRules()
        case '4':
            runSimulation()
        case '5':
            addAll(fuzzyLogic)
            print("Variables: ")
            print(fuzzyLogic.getAllVariables())
            print("Rules: ")
            print(fuzzyLogic.getRules())
            mainMenu()
        case '6':
            toolbox()
        case 'Close':
            toolbox()
        case _:
            print(invalidInput())
            mainMenu()

# create new fuzzy system
def createNewFuzzySystem():
    print("Enter the system’s name and a brief description:")
    print("------------------------------------------------")
    name = input()
    description = input()

    fuzzyLogic.__init__(name, description)

    if (type(name) is not str and type(description) is not str):
        print(invalidInput())
        createNewFuzzySystem()
    mainMenu()

# toolbox
def toolbox():
    print("Fuzzy Logic Toolbox")
    print("===================")
    print("1- Create a new fuzzy system")
    print("2- Quit")
    choice = input()

    match choice:
        case '1':
            createNewFuzzySystem()
        case '2':
            quit()
        case _:
            print(invalidInput())
            toolbox()

def quit():
    print("Good Bye!")
    raise SystemExit

def invalidInput():
    return "Invalid Input"

def notFound(notFound):
    return f"not found {notFound}"

def main():
    toolbox()

if __name__ == "__main__":
    main()