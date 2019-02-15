import itertools
import numpy as np 

class SetupEpsilonTransition(object):
    def __init__(self,epsilon):
        self.stateSet = None
        self.actionSet = None
        self.epsilon = epsilon

    def __call__(self, stateSet, actionSet):
        
        self.stateSet = stateSet
        self.actionSet = actionSet
        
        transitionTable = {state: self.getStateTransition(state) for state in self.stateSet}
        return(transitionTable) 

    def getStateTransition(self, state):
        actionTransitionDistribution = {action: self.getStateActionTransition(state, action) for action in self.actionSet}
        return(actionTransitionDistribution)
    
    def getStateActionTransition(self, currentState, action):
        nextState = self.getNextState(currentState, action)
        if currentState == nextState:
            transitionDistribution = {nextState: 1}
        else:
            transitionDistribution = {nextState: 1-self.epsilon, currentState: self.epsilon}
        return(transitionDistribution)

    
    def getNextState(self, state, action):
        potentialNextState = tuple([state[i] + action[i] for i in range(len(state))])
        if potentialNextState in self.stateSet:
            return(potentialNextState)
        return(state) 


class SetupRewardTable(object):
    def __init__(self,transitionTable, actionSet):
        self.transitionTable = transitionTable
        self.stateSet = list(transitionTable.keys())
        self.actionSet = actionSet
        
    def __call__(self, goalPreferences):
        rewardTable = {state:{action:{nextState: self.applyRewardFunction(state, action, nextState, goalPreferences) \
                                      for nextState in nextStateDict.keys() } \
                              for action, nextStateDict in actionDict.items()} \
                       for state, actionDict in self.transitionTable.items()}
        return(rewardTable)

    def applyRewardFunction(self, state, action, nextState, goalPreferences):
        moveCost = -1
        if (nextState in goalPreferences.keys() and action == (0,0)):
            return(goalPreferences[state])
        return(moveCost)