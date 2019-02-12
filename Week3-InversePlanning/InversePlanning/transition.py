import numpy as np
import itertools

class TableTransition(object):
    def __init__(self, transitionTable):
        self.transitionTable = transitionTable
        
    def __call__(self, currentState, action):
        assert currentState in self.transitionTable, "Current state not in set of possible states"
        
        nextStateDistributionDictionary = self.transitionTable[currentState][action]        
        nextStateIndex = np.random.choice(len(nextStateDistributionDictionary.items()), p=list(nextStateDistributionDictionary.values()))
        nextState = list(nextStateDistributionDictionary.keys())[nextStateIndex]
        return(nextState)


def createTransitionTable(gridCoordinates, allActions):
    return({xyCoordinate: getCoordinateTransitionDistribution(xyCoordinate, allActions) for xyCoordinate in gridCoordinates})

def getCoordinateTransitionDistribution(coordinateTuple, actions):
    return({action: getStateActionTransitionDistribution(coordinateTuple, action) for action in actions})

def getStateActionTransitionDistribution(currentState, action):
    nextState = elementwiseTupleAddition(currentState, action)
    allStates = [elementwiseTupleAddition(currentState, a) for a in allActions]
    stateActionTransitionDistribution = {state: 0 for state in allStates}
    
    if validCoordinate(nextState, gridWidth, gridHeight):
        stateActionTransitionDistribution[nextState] = 1
    else:
        stateActionTransitionDistribution[currentState] = 1
    return(stateActionTransitionDistribution)

def validCoordinate(coordinate, gridWidth, gridHeight):
    xCoordinate, yCoordinate = coordinate
    if(xCoordinate < 0 or  xCoordinate >= gridWidth):
        return(False)
    if(yCoordinate < 0 or yCoordinate >= gridHeight):
        return(False)
    return(True)

def elementwiseTupleAddition(firstTuple, secondTuple):
    assert len(firstTuple) == len(secondTuple),"Tuples are of different length."
    return(tuple([firstTuple[i] + secondTuple[i] for i in range(len(firstTuple))]))


def main():
	gridWidth = 5
	gridHeight = 10

	gridCoordinates = list(itertools.product(range(gridWidth), range(gridHeight)))
	allActions = list(set(itertools.permutations([-1,-1, 0, 0, 1, 1], 2)))

	transition = createTransitionTable(gridCoordinates, allActions)

	getGridTransition = TableTransition(transition)
	getGridTransition((4,9), (-1,0))

if __name__ == '__main__':
	main()