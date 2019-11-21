class GetLikelihoodRewardFunction(object):
    def __init__(self, transitionTable, goalPolicies):
        self.transitionTable = transitionTable
        self.goalPolicies  = goalPolicies

    def __call__(self, trueGoal, originalReward):
        likelihoodRewardFunction = self.createLikelihoodReward(trueGoal)
        newReward = self.mergeRewards(originalReward, likelihoodRewardFunction)
        return(newReward)
    
    def createLikelihoodReward(self, trueGoal):
        rewardFunction = {state: {action :{nextState :  self.getLikelihoodRatio(state, nextState, trueGoal) \
                                             for nextState in self.transitionTable[state][action].keys() } \
                                    for action in self.transitionTable[state].keys() } \
                            for state in self.transitionTable.keys() }
        return(rewardFunction)
    
    def mergeRewards(self, reward1, reward2):
        mergedReward = {state: {action :{nextState :  reward1[state][action][nextState]+reward2[state][action][nextState] \
                                                     for nextState in reward1[state][action].keys() } \
                                            for action in reward1[state].keys() } \
                                    for state in reward1.keys() }
        return(mergedReward)
    
    def getLikelihoodRatio(self, state, nextState, goalTrue):
        infoScale =5
        goalLikelihood = self.getNextStateProbability(state, nextState, goalTrue)
        notGoalLikelihood = sum([self.getNextStateProbability(state, nextState, g)\
                                 for g in self.goalPolicies.keys()])
        
        likelihoodRatio = infoScale*goalLikelihood/notGoalLikelihood
        return(likelihoodRatio)
        
    def getNextStateProbability(self, state, nextState, goal):
        possibleActionsToNextState = [action for action in self.transitionTable[state] \
                                              if nextState in self.transitionTable[state][action]]
        probNextState = sum([self.transitionTable[state][action][nextState]*self.goalPolicies[goal][state][action] \
                             for action in possibleActionsToNextState])
        return(probNextState)
