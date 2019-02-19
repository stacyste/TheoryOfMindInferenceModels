class StateActionRewardTableWithDistanceMoveCost(object):
    def __init__(self,stateSet, actionSet, goalStates = [], trapStates = []):
        self.stateSet = stateSet
        self.actionSet = actionSet
        self.goalStates = goalStates
        self.trapStates = trapStates
        
    def __call__(self, goalReward = 10, trapCost = -100):
        rewardTable = {state:{action: self.applyRewardFunction(state, action, goalReward, trapCost) \
                              for action in self.actionSet} \
                       for state self.stateSet}
        return(rewardTable)

    def applyRewardFunction(self, state, action, goalReward, trapCost):
        moveCost = self.getMoveCost(action)
        
        if state in self.goalStates:
            return(goalReward+moveCost)
        elif state in self.trapStates:
            return(trapCost+moveCost)
        return(moveCost)
    
    def getMoveCost(self, action):
        if action == (0,0):
            return(-.1)
        else:
            actionDistance = sum([abs(action[i]) for i in range(len(action))])
            return(-actionDistance)