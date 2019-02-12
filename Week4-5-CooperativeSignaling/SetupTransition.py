import itertools
import numpy as np 

class SetupTransition(object):
    def __init__(self, gridWidth, gridHeight, actionSet):
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.stateSet = list(itertools.product(range(self.gridWidth), range(self.gridHeight)))
        self.actionSet = actionSet


    def __call__(self):
        transitionTable = {state: self.getStateTransition(state) for state in self.stateSet}
        return(transitionTable) 

    def getStateTransition(self, state):
        actionTransitionDistribution = {action: self.getStateActionTransition(state, action) for action in self.actionSet}
        return(actionTransitionDistribution)
    
    def getStateActionTransition(self, currentState, action):
        nextState = self.getNextState(currentState, action)

        validNextStates = list(set([self.getNextState(currentState, a) for a in self.actionSet]))
        rangeValidNextStates = len(validNextStates)
        slipStates = np.random.choice(rangeValidNextStates, 3)
        transitionDistribution = {nextState:.7}

        for slipIndex in slipStates:
            if validNextStates[slipIndex] not in transitionDistribution:
                transitionDistribution[validNextStates[slipIndex]] = .1
            else:
                transitionDistribution[validNextStates[slipIndex]] += .1

        return(transitionDistribution)

    
    def getNextState(self, state, action):
        potentialNextState = tuple([state[i] + action[i] for i in range(len(state))])
        if potentialNextState in self.stateSet:
            return(potentialNextState)
        return(state) 