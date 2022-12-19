

class FuzzyLogic:

    variables = []  #{'name': 'name', 'type': 'IN', 'crispValue': 50, 'range': ['0', '100'], sets: [{'name': 'name', 'type': 'TRI', 'value': [0, 0, ...]}]}
    rules = []
    currVarIndex = None

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
        if (self.deffuzify()): print("Defuzzification => done")


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
                            y1 = self.getMiddleValue(i, set['value'])
                            x2 = set['value'][i+1]
                            y2 = self.getMiddleValue(i+1, set['value'])
                            break

                    #if no range found
                    if (x1 == y1 == x2 == y2 == None): set['membership'] = 0
                    else: set['membership'] = self.evaluateMembership(x1, y1, x2, y2, crispValue)
        return True

    def infer(self):
        pass

    """
    defuzz
    double numerator = 0, denominator = 0, result = 0;
        for (int i=0 ; i<outputMemberships.size() ; i++) {
            numerator += outputMemberships.get(i) * centroids.get(i);
            denominator += outputMemberships.get(i);
        }
        result = numerator / denominator;
        System.out.println("Defuzzification => done");
        System.out.println(result);
    """
    """
    infer
      for (Rule rule: rules) {
            double membership = 0;

            if(rule.operators.size() == 0){
                Variable variable = rule.variables.get(0);
                membership = variable.getMembership(rule.memberships.get(0));
            }

            for (int i = 0; i < rule.operators.size(); i++) {
                Variable variable1 = getVariable(rule.variables.get(i).getName());
                Variable variable2 = getVariable(rule.variables.get(i + 1).getName());

                membership = switch (rule.operators.get(i)) {
                    case "or" -> Math.max(variable1.getMembership(rule.memberships.get(i)),
                            variable2.getMembership(rule.memberships.get(i + 1)));
                    case "and" -> Math.min(variable1.getMembership(rule.memberships.get(i)),
                            variable2.getMembership(rule.memberships.get(i + 1)));
                    case "or_not" -> Math.max(variable1.getMembership(rule.memberships.get(i)),
                            1 - variable2.getMembership(rule.memberships.get(i + 1)));
                    case "and_not" -> Math.min(variable1.getMembership(rule.memberships.get(i)),
                            1 - variable2.getMembership(rule.memberships.get(i + 1)));
                    default -> membership;
                };
            }

            Variable outputVariable = getVariable(rule.getOutVariable());
            for (FuzzySet set: outputVariable.getFuzzySets()) {
                if(set.getName().equals(rule.getOutSet())){
                    centroids.add(set.getCentroid());
                }
            }

            outputMemberships.add(membership);
            outputSets.add(rule.outVariable);



        }
        System.out.println("Inference => done");
    """
    def deffuzify(self):
        pass

    def evaluateMembership(self, x1, y1, x2, y2, crisp):
        slope = (y2 - y1)/(x2 - x1)
        x =  x2 if slope < 0 else x1
        c = -(slope * x)
        return (slope * crisp) + c

    def getMiddleValue(self, index, _type):
        # get the middle value
        if _type == 'TRI':
            return 1 if (index == 1) else 0
        else: # TRAP
            return 1 if (index == 1 or index == 2) else 0

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