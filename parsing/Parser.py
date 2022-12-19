import re
from FuzzyLogic import FuzzyLogic

class Parser: 
    variableTypes = ['IN', 'OUT']
    setTypes = ['TRI', 'TRAP']
    keywords = ['or', 'and', 'not_and']
    outputSymbol = '=>'

    def __init__(self):
        pass

    # proj_funding IN [0, 100]
    def parseVariableLine(self, line: str):
        args = list(line.split(" "))

        if (len(args) != 4):
            return None

        try:
            varName = args[0]
            varType = args[1]
            if (not(self.checkType(varType, self.variableTypes))): return None

            varLowerRange = list(re.split(r"\[|,", args[2]))
            varUpperRange = list(re.split(r"]", args[3]))

            lowerRange = varLowerRange[1]
            upperRange = varUpperRange[0]

            return {"name": varName, "type": varType, "range": [int(lowerRange), int(upperRange)]}
        except NameError:
            print("Something went wrong while parsing variable line")
            return None

    def parseSetLine(self, line: str):
        args = list(line.split(" "))

        if (len(args) != 5 and len(args) != 6):
            return None

        try:
            setName = args[0]
            setType = args[1]
            if (not(self.checkType(setType, self.setTypes))): return None

            match setType:
                case 'TRI':
                    return {"name": setName, "type": setType, "values": [int(args[2]), int(args[3]), int(args[4])]}
                case 'TRAP':
                    return {"name": setName, "type": setType, "values": [int(args[2]), int(args[3]), int(args[4]), int(args[5])]}

            # won't reach this line
            return None
        except NameError:
            print("Something went wrong while parsing set line")
            return None
       
    # proj_funding high or exp_level expert => risk low
    def parseRuleLine(self, line: str, fuzzyLogic: FuzzyLogic):
        args = list(line.split(" "))

        # first condition
        condition_1 = fuzzyLogic.getVarAndSetIndices(args[0], args[1])
        if (not(condition_1)): return None

        # keyword
        keyword = args[2]
        if (not(self.checkType(keyword, self.keywords))): return None # e.x: or, and, not_and

        # second condition
        condition_2 = fuzzyLogic.getVarAndSetIndices(args[3], args[4])
        if (not(condition_2)): return None

        # output symbol
        if (args[5] != self.outputSymbol): return None

        # rule result
        ruleResult = fuzzyLogic.getVarAndSetIndices(args[6], args[7])
        if (not(ruleResult)): return None
        return {'condition_1': condition_1, 'keyword': keyword, 'condition_2': condition_2, 'result': ruleResult}
        """
           [
            {
                'condition_1': [0, 0],
                'keyword': 'or'
                'condition_2': [1, 0],
                'result': [2 , 0]
            }
           ]
        """
        
    def checkType(self, type, types):
        if (type in types):
            return True
        else:
            return False








"""
        fuzzyLogic.addVariable({'name': 'proj_funding', 'type': 'IN', 'range': [0, 100]})
        fuzzyLogic.checkVariableName('proj_funding')
        fuzzyLogic.addSetToExistingVariable({'name': 'high', 'type': 'TRI', 'value': [0, 0, 0]})

        fuzzyLogic.addVariable({'name': 'exp_level', 'type': 'IN', 'range': [0, 60]})
        fuzzyLogic.checkVariableName('exp_level')
        fuzzyLogic.addSetToExistingVariable({'name': 'expert', 'type': 'TRI', 'value': [0, 0, 0]})

        fuzzyLogic.addVariable({'name': 'risk', 'type': 'OUT', 'range': [0, 60]})
        fuzzyLogic.checkVariableName('risk')
        fuzzyLogic.addSetToExistingVariable({'name': 'low', 'type': 'TRI', 'value': [0, 0, 0]})

"""