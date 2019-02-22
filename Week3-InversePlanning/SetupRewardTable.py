class SetupRewardTable(object):
    def __init__(self,transitionTable, actionSet, goalState, trapStates):
        self.transitionTable = transitionTable
        self.stateSet = list(transitionTable.keys())
        self.actionSet = actionSet
        self.goalState = goalState
        self.trapStates = trapStates
        
    def __call__(self):
        rewardTable = {state:{action:{nextState: self.applyRewardFunction(state, action, nextState) \
                                      for nextState in nextStateDict.keys() } \
                              for action, nextStateDict in actionDict.items()} \
                       for state, actionDict in self.transitionTable.items()}
        return(rewardTable)

    def applyRewardFunction(self, state, action, nextState):
        goalReward = 10
        trapCost = -100
        moveCost = self.getMoveCost(state, action, nextState)

        if state == self.goalState:
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

class SetupRewardTableLeaveGoal(object):
    def __init__(self,transitionTable, actionSet, goalState, trapState):
        self.transitionTable = transitionTable
        self.stateSet = list(transitionTable.keys())
        self.actionSet = actionSet
        self.goalState = goalState
        self.trapState = trapState
        
    def __call__(self):
        rewardTable = {state:{action:{nextState: self.applyRewardFunction(state, action, nextState) for nextState in nextStateDict.keys() }for action, nextStateDict in actionDict.items()} for state, actionDict in self.transitionTable.items()}
        return(rewardTable)

    def applyRewardFunction(self, state, action, nextState):
        goalReward = 10
        trapCost = -100
        moveCost = self.getMoveCost(state, action, nextState)
        
        if state == self.goalState and nextState != self.goalState:
            return(goalReward)
        elif state == self.trapState:
            return(trapCost)
        return(moveCost)

    def getMoveCost(self, state, action, nextState):
        if action == (0,0):
            return(-.1)
        else:
            actionDistance = sum([abs(action[i]) for i in range(len(action))])
            return(-(actionDistance**.5))