

class FuzzyLogic:

    variables = []  #{'name': 'name', 'type': 'IN', 'crispValue': 50, 'range': ['0', '100'], sets: [{'name': 'name', 'type': 'TRI', 'value': [0, 0, ...]}]}
    rules = []

    centroids = []
    memberships = []

    currVarIndex = None
    finalResult = None
    outputMessage = ""

    # constructor
    def __init__(self, name='', description=''):
        self.name = name
        self.description = description

    def addVariable(self, var):
        #print(var)
        self.variables.append(var)

    def addSetToExistingVariable(self, set):
        if self.currVarIndex != None:
            if ('sets' in self.variables[self.currVarIndex]):
                self.variables[self.currVarIndex]['sets'].append(set)
            else: # if the variable doesn't have sets (first time)
                self.variables[self.currVarIndex]['sets'] = [set]

    def addRule(self, rule):
        self.rules.append(rule)

    def runSimulation(self):
        if (self.fuzzify()): print("Fuzzification => done")
        if (self.infer()): print("Inference => done")
        if (self.deffuzify()): print("Defuzzification => done\n")
        return self.getOutputMessage(self.finalResult)

    def fuzzify(self):
        # loop over variables
        for var in self.variables:
            if 'sets' not in var: continue
            if 'crispValue' not in var: var['crispValue'] = 0
            crispValue = var['crispValue']
            # loop over variable sets
            for set in var['sets']:
                try:
                    # if the crisp value in the set values, get the index of that set value
                    index = set['value'].index(crispValue)
                    if (index != None):
                        # set the membership with the middle value
                        set['membership'] = self.getMiddleValue(index, set['type'])
                except ValueError:
                    # crisp value was not found in the set
                    x1 = y1 = x2 = y2 = None
                    # we search the two nearest values to the crisp value
                    for i in range(len(set['value'])-1):
                        # if the crisp falls between two values
                        if (crispValue > set['value'][i] and crispValue < set['value'][i+1]):
                            # points to calc the slop
                            x1 = set['value'][i]
                            y1 = self.getMiddleValue(i, set['type'])
                            x2 = set['value'][i+1]
                            y2 = self.getMiddleValue(i+1, set['type'])
                        #if no range found
                        if (x1 == y1 == x2 == y2 == None): set['membership'] = 0
                        else:
                            set['membership'] = self.evaluateMembership(x1, y1, x2, y2, crispValue)
        return True

    def infer(self):
        for rule in self.rules:
            memebership = 0
            # First variable 
            var_index_1 = rule['condition_1'][0] # index of first variable in the rule
            set_index_1 = rule['condition_1'][1] # index of the selected set connected to that variable

            variable_1 = self.variables[var_index_1]
            set_1 = variable_1['sets'][set_index_1]
            set_membership_1 = set_1['membership']

            # Second variable 
            var_index_2 = rule['condition_2'][0] # index of second variable in the rule
            set_index_2 = rule['condition_2'][1] # index of the selected set connected to that variable

            variable_2 = self.variables[var_index_2]
            set_2 = variable_2['sets'][set_index_2]
            set_membership_2 = set_2['membership']

            match rule['keyword']:
                case 'or':
                    memebership = max(set_membership_1, set_membership_2)
                case 'and':
                    memebership = min(set_membership_1, set_membership_2)
                case 'or_not':
                    memebership = max(set_membership_1, 1 - set_membership_2)
                case 'and_not':
                    memebership = min(set_membership_1, 1 - set_membership_2)
                case _:
                    memebership = memebership

            # Result variable 
            var_index_3 = rule['result'][0] # index of result variable in the rule
            set_index_3 = rule['result'][1] # index of the selected set connected to that variable

            result_var = self.variables[var_index_3]
            result_set = result_var['sets'][set_index_3]
            self.centroids.append(self.calcCentroid(result_set))
            self.memberships.append(memebership)
        return True

    def deffuzify(self):
        numerator = 0 
        denominator = 0
        result = 0
        for i in range(len(self.memberships)):
            numerator += (self.memberships[i] * self.centroids[i])
            denominator += self.memberships[i]
        
        self.finalResult = numerator / denominator
        return True

    def evaluateMembership(self, x1, y1, x2, y2, crisp):
        slope = (y2 - y1)/(x2 - x1)
        x =  x2 if slope < 0 else x1
        intercept = -(slope * x)
        return (slope * crisp) + intercept

    def getMiddleValue(self, index, _type):
        # get the middle value
        if _type == 'TRI':
            return 1 if (index == 1) else 0
        else: # TRAP
            return 1 if (index == 1 or index == 2) else 0

    def calcCentroid(self, set):
        total = 0
        for val in set['value']:
            total += val
        return (total / len(set['value']))


    # Helper Func #
    def checkVariableName(self, name):
        for i in range(len(self.variables)):
            if self.variables[i]['name'] == name:
                self.currVarIndex = i
                return True
        return False

    def canRunSimulation(self):
        return (len(self.rules) != 0)   # rules should exist to run simulation

    # Getters #
    def getVarAndSetIndices(self, varName: str, setName: str): 
        # e.x: var_and_set = ['proj_funding', 'high']
        varIndex = None
        setIndex = None
        for i in range(len(self.variables)):
            if self.variables[i]['name'] == varName:
                varIndex = i
                if 'sets' in self.variables[i]:
                    for j in range(len(self.variables[i]['sets'])):
                        if self.variables[i]['sets'][j]['name'] == setName:
                            setIndex = j
                            break
                break

        print(f'index: {varIndex} {setIndex}')
        if varIndex != None and setIndex != None:
            return [varIndex, setIndex]
        else:
            return None

    def getAllVariables(self):
        return self.variables

    def getRules(self):
        return self.rules

    def getOutputMessage(self, result=0):
        result = float("{:.2f}".format(result))
        return f"The predicted risk is normal {result}"