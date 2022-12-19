from FuzzyLogic import FuzzyLogic

def addAll(fuzzyLogic: FuzzyLogic):
    # add sets and vars
    fuzzyLogic.addVariable({'name': 'proj_funding', 'type': 'IN', 'range': [0, 100]})
    fuzzyLogic.checkVariableName('proj_funding')
    fuzzyLogic.addSetToExistingVariable({'name': 'very_low', 'type': 'TRAP', 'value': [0, 0, 10, 30]})
    fuzzyLogic.addSetToExistingVariable({'name': 'low', 'type': 'TRAP', 'value': [10, 30, 40, 60]})
    fuzzyLogic.addSetToExistingVariable({'name': 'medium', 'type': 'TRAP', 'value': [40, 60, 70, 90]})
    fuzzyLogic.addSetToExistingVariable({'name': 'high', 'type': 'TRAP', 'value': [70, 90, 100, 100]})

    fuzzyLogic.addVariable({'name': 'exp_level', 'type': 'IN', 'range': [0, 60]})
    fuzzyLogic.checkVariableName('exp_level')
    fuzzyLogic.addSetToExistingVariable({'name': 'beginner', 'type': 'TRI', 'value': [0, 15, 30]})
    fuzzyLogic.addSetToExistingVariable({'name': 'intermediate', 'type': 'TRI', 'value': [15, 30, 45]})
    fuzzyLogic.addSetToExistingVariable({'name': 'expert', 'type': 'TRI', 'value': [30, 60, 60]})

    fuzzyLogic.addVariable({'name': 'risk', 'type': 'OUT', 'range': [0, 100]})
    fuzzyLogic.checkVariableName('risk')
    fuzzyLogic.addSetToExistingVariable({'name': 'low', 'type': 'TRI', 'value': [0, 25, 50]})
    fuzzyLogic.addSetToExistingVariable({'name': 'normal', 'type': 'TRI', 'value': [25, 50, 75]})
    fuzzyLogic.addSetToExistingVariable({'name': 'high', 'type': 'TRI', 'value': [50, 100, 100]})

    # add rules
    fuzzyLogic.addRule({
        'condition_1': [0, 3],
        'keyword': 'or',
        'condition_2': [1, 2],
        'result': [2 , 0]
    })
    fuzzyLogic.addRule({
        'condition_1': [0, 2],
        'keyword': 'and',
        'condition_2': [1, 1],
        'result': [2 , 1]
    })
    fuzzyLogic.addRule({
        'condition_1': [0, 2],
        'keyword': 'and',
        'condition_2': [1, 0],
        'result': [2 , 1]
    })
    fuzzyLogic.addRule({
        'condition_1': [0, 1],
        'keyword': 'and',
        'condition_2': [1, 0],
        'result': [2 , 2]
    })
    fuzzyLogic.addRule({
        'condition_1': [0, 0],
        'keyword': 'and_not',
        'condition_2': [1, 2],
        'result': [2 , 2]
    })

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
    """
    proj_funding high or exp_level expert => risk low
    proj_funding medium and exp_level intermediate => risk normal
    proj_funding medium and exp_level beginner => risk normal
    proj_funding low and exp_level beginner => risk high
    proj_funding very_low and_not exp_level expert => risk high

    """