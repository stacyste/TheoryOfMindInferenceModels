import numpy as np

class TableTransition(object):
    def __init__(self, transitionTable):
        self.transitionTable = transitionTable
        
    def __call__(self, currentState, action):
        assert currentState in self.transitionTable, "Current state not in set of possible states"
        assert action in self.transitionTable[currentState], "Action not valid"
        
        resultingStates,nextStateDistribution = self.transitionTable[currentState][action]
        resultingStateIndex = np.random.choice(np.arange(len(resultingStates)), p=transitionProbabilityDistributionOfState)
        
        nextState = resultingStates[resultingStateIndex]
        return(nextState)


def main():
	def elementwiseTupleAddition(firstTuple, secondTuple):
	    assert len(firstTuple) == len(secondTuple),"Tuples are of different length."
	    return(tuple([firstTuple[i] + secondTuple[i] for i in range(len(firstTuple))]))

	def isCoordinateValid(coordinate, gridWidth, gridHeight):
	    xCoordinate, yCoordinate = coordinate
	    if(xCoordinate < 0 or  xCoordinate >= gridWidth):
	        return(False)
	    if(yCoordinate < 0 or yCoordinate >= gridHeight):
	        return(False)
	    return(True)

	gridWidth = 5
	gridHeight = 10
	gridCoordinates = [(x, y) for x in range(gridWidth) for y in range(gridHeight)]

	allActions = [(0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1, 1)]
	transition = {}

	for xyCoordinate in gridCoordinates:
	    transition[xyCoordinate] = {}
	    for actionIndex, actionTuple in enumerate(allActions):
	        resultingStates = [elementwiseTupleAddition(xyCoordinate, action) for action in allActions]
	        transitionPDF = np.zeros(len(allActions))
	        
	        if isCoordinateValid(resultingStates[actionIndex], gridWidth=gridWidth, gridHeight = gridHeight):
	            transitionPDF[actionIndex] = 1
	        else:
	            transitionPDF[0] = 1
	            
	        transition[xyCoordinate][actionTuple] = (resultingStates, transitionPDF)

	getGridTransition = Transition(transition)
	getGridTransition((2,2), (-1,-1))

if __name__ == '__main__':
	main()