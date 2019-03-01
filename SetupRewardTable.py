class SetupRewardTableWithDistanceMoveCost(object):
    def __init__(self,transitionTable, actionSet, goalStates = [], trapStates = []):
        self.transitionTable = transitionTable
        self.stateSet = list(transitionTable.keys())
        self.actionSet = actionSet
        self.goalStates = goalStates
        self.trapStates = trapStates
        
    def __call__(self, goalReward = 10, trapCost = -100):
        rewardTable = {state:{action:{nextState: self.applyRewardFunction(state, action, nextState, goalReward, trapCost) \
                                      for nextState in nextStateDict.keys() } \
                              for action, nextStateDict in actionDict.items()} \
                       for state, actionDict in self.transitionTable.items()}
        return(rewardTable)

    def applyRewardFunction(self, state, action, nextState, goalReward, trapCost):
        moveCost = self.getMoveCost(state, action, nextState)
        
        if state in self.goalStates:
            return(goalReward+moveCost)
        elif state in self.trapStates:
            return(trapCost)
        return(moveCost)
    
    def getMoveCost(self, state, action, nextState):
        if action == (0,0):
            return(-.1)
        else:
            actionDistance = sum([abs(action[i]) for i in range(len(action))])
            return(-actionDistance)



class SetupStateActionRewardTableWithDistanceMoveCost(object):
    def __init__(self, stateSet, actionSet, goalStates = [], trapStates = []):
        self.stateSet = stateSet
        self.actionSet = actionSet
        self.goalStates = goalStates
        self.trapStates = trapStates
        
    def __call__(self, goalReward = 10, trapCost = -100):
        rewardTable = {state:{action: self.applyRewardFunction(state, action, goalReward, trapCost) \
                              for action in self.actionSet} \
                       for state in self.stateSet}
        return(rewardTable)

    def applyRewardFunction(self, state, action, goalReward, trapCost):
        moveCost = self.getMoveCost(action)
        
        if state in self.goalStates:
            return(goalReward)
        elif state in self.trapStates:
            return(trapCost+moveCost)
        return(moveCost)
    
    def getMoveCost(self, action):
        if action == (0,0):
            return(-.1)
        else:
            actionDistance = sum([abs(action[i]) for i in range(len(action))])
            return(-actionDistance)


class SetupStateActionRewardWithUserSpecifiedCosts(object):
    def __init__(self, stateSet, actionSet, specialStates = []):
        self.stateSet = stateSet
        self.actionSet = actionSet
        self.specialStates = specialStates

    def __call__(self, stateRewards = 10):
        rewardTable = {state:{action: self.applyRewardFunction(state, action, stateRewards) \
                              for action in self.actionSet} \
                       for state in self.stateSet}
        return(rewardTable)

    def applyRewardFunction(self, state, action, stateRewards):
        moveCost = self.getMoveCost(action)
        
        if state in self.specialStates:
            if type(stateRewards) is int:
                return(stateRewards)
            return(stateRewards[state]+moveCost)
        return(moveCost)
    
    def getMoveCost(self, action):
        if action == (0,0):
            return(-.1)
        else:
            actionDistance = sum([abs(action[i]) for i in range(len(action))])
            return(-actionDistance)


