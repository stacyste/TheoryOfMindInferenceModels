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
        
        delta = self.convergenceTolerance*100
        while(delta > self.convergenceTolerance):
            delta = 0
            for state, actionDict in self.transitionTable.items():
                valueOfStateAtTimeT = self.valueTable[state]
                qforAllActions = [self.getQValue(state, action) for action in actionDict.keys()]
                self.valueTable[state] = max(qforAllActions) 
                delta = max(delta, abs(valueOfStateAtTimeT-self.valueTable[state]))
        policyTable = {state:self.getBoltzmannPolicy(state) for state in self.transitionTable.keys()}

        return([self.valueTable, policyTable])
    
    def getBoltzmannPolicy(self, state):
        exponents = [self.beta*self.getQValue(state, action) for action in self.transitionTable[state].keys()]
        actions = [action for action in self.transitionTable[state].keys()]

        # Scale to [0,700] if there are exponents larger than 700
        if len([exponent for exponent in exponents if exponent>700])>0:
            print("scaling exponents to [0,700]... On State:")
            print(state)
            exponents = [700*(exponent/max(exponents)) for exponent in exponents]

        statePolicy = {action: math.exp(exponent) for exponent, action in zip(exponents,actions)}
        normalizedPolicy = self.normalizeDictionaryValues(statePolicy)
        return(normalizedPolicy)

    def getBoltzmannPolicyMathOverflowPossible(self, state):
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

class DeterministicValueIteration(object):
    def __init__(self, transitionTable, rewardTable, valueTable, convergenceTolerance, discountingFactor = .99):
        self.transitionTable = transitionTable
        self.rewardTable  = rewardTable
        self.valueTable = valueTable
        self.convergenceTolerance = convergenceTolerance
        self.gamma = discountingFactor

    def __call__(self):
        theta = self.convergenceTolerance*100
        while(theta > self.convergenceTolerance):
            theta = 0
            for state, actionDict in self.transitionTable.items():

                valueOfStateAtTimeT = self.valueTable[state]
                self.valueTable[state] = max([self.getQValue(state, action) for action in actionDict.keys()])
                theta = max(theta, abs(valueOfStateAtTimeT-self.valueTable[state]))

        policyTable = {state:self.getStatePolicy(state) for state in self.transitionTable.keys()}
        return([self.valueTable, policyTable])
    
    def getStatePolicy(self, state):
        roundingThreshold = 5

        maxQValue = max([round(self.getQValue(state, action),roundingThreshold) for action in self.transitionTable[state].keys()])
        optimalActionSet = [action for action in self.transitionTable[state].keys() \
                            if round(self.getQValue(state, action),roundingThreshold) == maxQValue]
        statePolicy = {action: 1/(len(optimalActionSet)) for action in optimalActionSet}
        return(statePolicy)
        
    def getQValue(self, state, action):
        nextStatesQ = [prob*(self.rewardTable[state][action][nextState] \
                             + self.gamma*self.valueTable[nextState]) \
                      for nextState, prob in self.transitionTable[state][action].items()]
        qValue = sum(nextStatesQ)
        return(qValue)