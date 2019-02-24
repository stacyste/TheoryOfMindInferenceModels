import itertools
import numpy as np

"""
Creates a determinsitic transition table for a grid defined by its width and height and set of actions. 
If the action takes the agent off the board, the action should result in the next state being the same 
as the current state.

Inputs:
    gridWidth - positive whole number
    gridHeight - positive whole number
    action set - list of actions as tuples
Output: nested dictionary {state:{action:nextState:probability}} where there is every state and action pair and only the next states that result in a non-zero probability
"""
class SetupDeterministicTransitionByGrid(object):
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
        transitionDistribution = {nextState: 1}
        return(transitionDistribution)

    def getNextState(self, state, action):
        potentialNextState = tuple([state[i] + action[i] for i in range(len(state))])
        if potentialNextState in self.stateSet:
            return(potentialNextState)
        return(state) 


"""
Creates a determinsitic transition table for a set of states and actions. If the action takes the agent off the board, the action should result in the next state being the same 
as the current state.

Inputs:
    state set - list of states as tuples
    action set - list of actions as tuples
Output: nested dictionary {state:{action:nextState:probability}} where there is every state and action pair and only the next states that result in a non-zero probability
"""
class SetupDeterministicTransitionByStateSet(object):
    def __init__(self, stateSet, actionSet):
        self.stateSet = stateSet
        self.actionSet = actionSet

    def __call__(self, randomSeed = None):
        if randomSeed:
            np.random.seed(randomSeed)
        transitionTable = {state: self.getStateTransition(state) for state in self.stateSet}
        return(transitionTable) 

    def getStateTransition(self, state):
        actionTransitionDistribution = {action: self.getStateActionTransition(state, action) for action in self.actionSet}
        return(actionTransitionDistribution)
    
    def getStateActionTransition(self, currentState, action):
        nextState = self.getNextState(currentState, action)
        transitionDistribution = {nextState: 1}
        return(transitionDistribution)

    def getNextState(self, state, action):
        potentialNextState = tuple([state[i] + action[i] for i in range(len(state))])
        if potentialNextState in self.stateSet:
            return(potentialNextState)
        return(state) 


"""
Creates a stochastic transition table for a set of states and actions. The probability of reacing the typical next state will be initialized by nextStateProb, and 
the remaining probability will be split equally across a specified number of other direcions.

Inputs:
    gridWidth - positive whole number
    gridHeight - positive whole number
    action set - list of actions as tuples

    Callable:
        trueNextStateProbability - the probability of successfully getting to the intended next state with the action
        numberOfSlipDirections - the number of states to sample from the possible directions leading to slippage
Output: nested dictionary {state:{action:nextState:probability}} where there is every state and action pair and only the next states that result in a non-zero probability
"""
class SetupSlipperyTransitionByGrid(object):
    def __init__(self, gridWidth, gridHeight, actionSet):
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.stateSet = list(itertools.product(range(self.gridWidth), range(self.gridHeight)))
        self.actionSet = actionSet

    def __call__(self, trueNextStateProbability = .7, numberOfSlipDirections = 3):
        transitionTable = {state: self.getStateTransition(state, trueNextStateProbability, numberOfSlipDirections) for state in self.stateSet}
        return(transitionTable) 

    def getStateTransition(self, state,trueNextStateProbability, numberOfSlipDirections):
        actionTransitionDistribution = {action: self.getStateActionTransition(state, action,trueNextStateProbability, numberOfSlipDirections) for action in self.actionSet}
        return(actionTransitionDistribution)
    
    def getStateActionTransition(self, currentState, action, trueNextStateProbability, numberOfSlipDirections):
        nextStateProbability = min(trueNextStateProbability, 1)
        remainingProbability = 1-nextStateProbability
        slipProbability = remainingProbability/numberOfSlipDirections

        nextState = self.getNextState(currentState, action)
        transitionDistribution = {nextState: nextStateProbability}
    
        validNextStates = list(set([self.getNextState(currentState, a) for a in self.actionSet]))
        rangeValidNextStates = len(validNextStates)
        slipStates = np.random.choice(rangeValidNextStates, numberOfSlipDirections)
        

        for slipIndex in slipStates:
            if validNextStates[slipIndex] not in transitionDistribution:
                transitionDistribution[validNextStates[slipIndex]] = slipProbability
            else:
                transitionDistribution[validNextStates[slipIndex]] += slipProbability
        return(transitionDistribution)

    def getNextState(self, state, action):
        potentialNextState = tuple([state[i] + action[i] for i in range(len(state))])
        if potentialNextState in self.stateSet:
            return(potentialNextState)
        return(state) 


"""
Creates a stochastic transition table for a set of states and actions with barriers in the environment.
The agent will take the intended action with probability 1-epsilon and stay where it is with probability epsilon.
If the action takes the agent off the board, the action should result in the next state being the same 
as the current state.

Inputs:
    state set - list of states as tuples
    action set - list of actions as tuples
    Callable:
        barrierList: a list of lists where each inner list contains the state, nextstate tuples that cannot be crossed. Barriers can be uni-directional
        epsilon: probability of staying instead of taking intended action
Output: nested dictionary {state:{action:nextState:probability}} where there is every state and action pair and only the next states that result in a non-zero probability
"""
class SetupEpsilonTransitionWithBarrier(object):
    def __init__(self, stateSet, actionSet):
        self.stateSet = stateSet
        self.actionSet = actionSet

    def __call__(self, barrierList, epsilon=0):
        transitionTable = {state: {action:  self.getStateActionTransition(state, action, epsilon, barrierList) \
                                   for action in self.actionSet}\
                           for state in self.stateSet}
        return(transitionTable) 
    
    def getStateActionTransition(self, currentState, action, epsilon, barriers):
        nextState = self.getNextState(currentState, action, barriers)
        if currentState == nextState or epsilon == 0:
            transitionDistribution = {nextState: 1}
        else:
            transitionDistribution = {nextState: 1-epsilon, currentState:epsilon}
        return(transitionDistribution)

    def getNextState(self, state, action, barriers):
        potentialNextState = tuple([state[i] + action[i] for i in range(len(state))])
        if potentialNextState in self.stateSet and (not [state, potentialNextState] in barriers):
            return(potentialNextState)
        return(state) 