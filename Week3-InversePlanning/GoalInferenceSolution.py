import numpy as np

class PerformGoalInference(object):
    def __init__(self, transitionTable, goalPolicies, goalPriors, stateTrajectory):
        self.transitionTable = transitionTable
        self.goalPolicies  = goalPolicies
        self.goalPriors = goalPriors
        self.stateTrajectory = stateTrajectory

    def __call__(self):
        posterior = self.getSequenceOfStateProbabilities()*np.array(self.goalPriors)        
        row_sums = posterior.sum(axis=1, keepdims=True)
        normalizedPosterior = posterior / row_sums
        return(normalizedPosterior)
        
    def getNextStateProbability(self, state, nextState, policy):
        possibleActionsToNextState = [action for action in self.transitionTable[state] \
                                      if nextState in self.transitionTable[state][action]]

        probNextState = sum([self.transitionTable[state][action][nextState]*policy[state][action] \
                             for action in possibleActionsToNextState])
        return(probNextState)
    
    def getSequenceOfStateProbabilities(self):
        probNextState = [self.goalPriors]
        for t, state in enumerate(self.stateTrajectory[:-1]):
            nextState = self.stateTrajectory[t+1]
            probNextState.append([self.getNextStateProbability(state, nextState, goalPolicy) \
                         for goalPolicy in self.goalPolicies])
        observedStateProbs = np.cumprod(np.array(probNextState), axis=0)
        return(observedStateProbs)
