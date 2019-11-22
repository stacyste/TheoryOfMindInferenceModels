import itertools
import numpy as np 

class SetupBeliefTransition(object):
    def __init__(self, positionSet, beliefSet, actionSet, observationPositionSet):
        self.positionSet = positionSet
        self.beliefSet = beliefSet
        self.actionSet = actionSet
        self.observationPositionSet = observationPositionSet

    def __call__(self):
        beliefTransition = {(position, belief): {action: self.getNewBeliefOfAction(position, belief, action)\
                             for action in self.actionSet} \
         for position in self.positionSet \
         for belief in self.beliefSet}
        return(beliefTransition)
        
    def getNewBeliefOfAction(self, position, oldBelief, action):     
        newPosition = self.getNextPosition(position, action)
        
        if self.recieveObservation(position, action) and oldBelief == .5:
            newBeliefDictionary = {(newPosition, 1): .5, (newPosition, 0):.5}
        else:
            newBeliefDictionary = {(newPosition, oldBelief):1}
            
        return(newBeliefDictionary)
    
    def recieveObservation(self, position, action):
        nextPosition = self.getNextPosition(position, action)
        return(nextPosition in self.observationPositionSet)
    
    def getNextPosition(self, position, action):
        potentialNextState = tuple([position[i] + action[i] for i in range(len(position))])
        if potentialNextState in self.positionSet:
            return(potentialNextState)
        return(position) 

class SetupRewardBeliefTable(object):
    def __init__(self, positionSet, beliefSet, actionSet):
        self.positionSet = positionSet
        self.beliefSet = beliefSet
        self.actionSet = actionSet
        
    def __call__(self, beliefTransition, worldRewardList):
        rewardTable = {(position, worldBelief): {action: {nextState:
                        self.getRewardBelief(position, worldBelief, action, worldRewardList) \
                                                         for nextState in beliefTransition[(position, worldBelief)][action].keys()}\
                             for action in self.actionSet} \
         for position in self.positionSet \
         for worldBelief in self.beliefSet}
        return(rewardTable)
    
    def getRewardBelief(self, position, probWorld1, action, worldRewards):
        rewardBelief = probWorld1*worldRewards[0][position][action] \
        + (1-probWorld1)*worldRewards[1][position][action]
        return(rewardBelief)


"""
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
        return(moveCost)"""