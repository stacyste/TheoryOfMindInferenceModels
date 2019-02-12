import math

class BoltzmannValueIteration(object):
    def __init__(self, transitionTable, rewardTable, valueTable, convergenceTolerance, discountingFactor, beta):
        self.transitionTable = transitionTable
        self.rewardTable  = rewardTable
        self.valueTable = valueTable
        self.convergenceTolerance = convergenceTolerance
        self.gamma = discountingFactor
        self.beta = beta

    def __call__(self):
        
        theta = self.convergenceTolerance*100
        while(theta > self.convergenceTolerance):
            theta = 0
            for state, actionDict in self.transitionTable.items():
                valueOfStateAtTimeT = self.valueTable[state]
                qforAllActions = [self.getQValue(state, action) for action in actionDict.keys()]
                self.valueTable[state] = max(qforAllActions) 
                theta = max(theta, abs(valueOfStateAtTimeT-self.valueTable[state]))
        policyTable = {state:self.getBoltzmannPolicy(state) for state in self.transitionTable.keys()}

        return([self.valueTable, policyTable])
    
    def getBoltzmannPolicy(self, state):
        statePolicy = {action: math.exp(self.beta*self.getQValue(state, action)) for action in self.transitionTable[state].keys()}
        normalizedPolicy = self.normalizeDictionaryValues(statePolicy)
        return(normalizedPolicy)
        
    def getQValue(self, state, action):
        nextStatesQ = [prob*(self.rewardTable[state][action][nextState] \
                             + self.gamma*self.valueTable[nextState]) \
                      for nextState, prob in self.transitionTable[state][action].items()]
        qValue = sum(nextStatesQ)
        return(qValue)
    
    def normalizeDictionaryValues(self, unnormalizedDictionary):
        totalSum = sum(unnormalizedDictionary.values())
        normalizedDictionary = {originalKey: val/totalSum for originalKey, val in unnormalizedDictionary.items()}
        return(normalizedDictionary)