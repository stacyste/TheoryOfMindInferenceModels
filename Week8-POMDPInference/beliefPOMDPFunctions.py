import numpy as np
import itertools

class SetupBeliefTransition(object):
    def __init__(self, positionSet, beliefSet, actionSet):
        self.positionSet = positionSet
        self.beliefSet = beliefSet
        self.actionSet = actionSet

    def __call__(self, getNewBelief):
        beliefTransition = {(position, belief): self.getActionNewBeliefTransition(position, belief, getNewBelief) \
         for position in self.positionSet \
         for belief in self.beliefSet}
        return(beliefTransition)
    
    def getActionNewBeliefTransition(self, position, belief, getNewBelief):
        actionTransition = {}
        for action in self.actionSet:
            newPosition = self.updatePosition(position, action)
            newBeliefDictionary = getNewBelief(newPosition, belief)
            actionTransition[action] = newBeliefDictionary
        return(actionTransition)
        
    def updatePosition(self, position, action):
        potentialNextState = tuple([position[i] + action[i] for i in range(len(position))])
        if potentialNextState in self.positionSet:
            return(potentialNextState)
        return(position) 

def updateBelief(newPosition, belief):
    positionsTruck1Visible = [(0, 0),(1, 3),(3, 0),(0, 2),(2, 1),(1, 0),(0, 3),(4, 0),(0, 1),(1, 2),(3, 1),(2, 0),(4, 1),(1, 1)]
    positionsTruck2Visible = [(0,3), (1,3), (2,3), (3,3), (4,3)] 
    truck1Observed, truck2Observed = [1 if newPosition in truckPositions else 0 for truckPositions in [positionsTruck1Visible,positionsTruck2Visible]]
    
    if truck1Observed and truck2Observed:
        possibleObservations = [("K", "L"), ("K", "M"), ("L", "K"), ("L", "M"), ("M", "K"),("M", "L")]
    elif truck1Observed and not truck2Observed:
        possibleObservations = [("K",""), ("L", ""), ("M", "")]
    elif truck2Observed and not truck1Observed:
        possibleObservations = [("", "K"), ("", "L"), ("", "M")]
    else:
        possibleObservations = [("", "")]
        
    unNormalizedBeliefs = [createBelief(belief, observation) for observation in possibleObservations if compatible(observation,belief)]
    normalizedBeliefs = [tuple([float(i)/sum(belief) for i in belief]) for belief in unNormalizedBeliefs]
    
    nextBeliefs = {(newPosition, belief): 1/len(normalizedBeliefs) for belief in normalizedBeliefs}
    return(nextBeliefs)


def createBelief(belief, truckObservation):
    beliefTruck = convertBeliefToTruck(belief)
    newTruck = addTrucks(beliefTruck, truckObservation)
    return(convertTruckToBelief(newTruck))

def addTrucks(trucks1,trucks2):
    newTruck = list(trucks1)
    for i in range(len(trucks1)):
        if trucks1[i] != "" and trucks2[i] != "":
            assert trucks1[i] == trucks2[i], "Error! observation is inconsistent with belief!!!"
    for i in range(len(trucks1)):
        if trucks1[i] == "" and trucks2[i] != "":
            newTruck[i] = trucks2[i]
    return tuple(newTruck)

def compatible(observation, belief):
    beliefTruck = convertBeliefToTruck(belief)
    for i in range(len(beliefTruck)):
        if beliefTruck[i] != "" and observation[i] != "":
            if beliefTruck[i] != observation[i]:
                return False
    if beliefTruck[0] == observation[1] and beliefTruck[0] != "": return False
    if beliefTruck[1] == observation[0] and beliefTruck[1] != "": return False
    return True

def convertTruckToBelief(truck):
    truckNames = ["K", "L", "M"]
    beliefArray = np.array([[0, 0, 0], [0, 0, 0],[0, 0, 0]])
    belief = [0,0,0,0,0,0]
    
    for i in range(len(truckNames)):
        if truck[0] == truckNames[i]: beliefArray[i,:] = 1
        if truck[1] == truckNames[i]: beliefArray[:,i] = 1
        beliefArray[i,i]=0 

    rowSums = np.sum(beliefArray, axis = 1)
    colSums = np.sum(beliefArray, axis = 0)
    beliefArraySum = np.array([[          0          , rowSums[0]+colSums[1], rowSums[0]+colSums[2]],
                               [rowSums[1]+colSums[0],           0          , rowSums[1]+colSums[2]],
                               [rowSums[2]+colSums[0], rowSums[2]+colSums[1],           0          ]])
    maxBelief = np.max(beliefArraySum)
    
    world = 0
    for i in range(beliefArraySum.shape[0]):
        for j in range(beliefArraySum.shape[1]):
            if i==j: continue
            if beliefArraySum[i,j] == maxBelief:
                belief[world] = 1
            world = world+1
    belief = [b/sum(belief) for b in belief]
    
    return(tuple([round(x,2) for x in belief]))

def convertBeliefToTruck(belief):
    truckNames = ["K", "L", "M"]
    beliefArray = np.array([[0, belief[0], belief[1]], [belief[2], 0, belief[3]],[belief[4], belief[5], 0]])
    
    beliefTruck = ["", ""]
    rowSums = np.sum(beliefArray, axis = 1)
    colSums = np.sum(beliefArray, axis = 0)
    if np.argwhere(rowSums == 1).size ==1:
        beliefTruck[0] = truckNames[int(np.argwhere(rowSums == 1))]
    if np.argwhere(colSums == 1).size ==1:
        beliefTruck[1] = truckNames[int(np.argwhere(colSums == 1))]
    return(tuple(beliefTruck))

class SetupRewardBeliefTable(object):
    def __init__(self, positionSet, beliefSet, actionSet):
        self.positionSet = positionSet
        self.beliefSet = beliefSet
        self.actionSet = actionSet
        
    def __call__(self, beliefTransition, worldRewardList):
        rewardTable = {(position, belief): {action: {nextState: self.getRewardBelief(position, belief, action, worldRewardList) \
                                                         for nextState in beliefTransition[(position, belief)][action].keys()}\
                             for action in self.actionSet} \
         for position in self.positionSet \
         for belief in self.beliefSet}
        return(rewardTable)
    
    def getRewardBelief(self, position, belief, action, worldRewards):
        rewardBelief = sum([reward[position][action]*probWorld for reward, probWorld in zip(worldRewards, belief)])
        return(rewardBelief)

def constructGoalStateRewards(truck1truck2,  preference, truckLocations = [(0,0), (4,3)], preferenceRewards = [100, 75, 50]):
    goalPreferences = {location : preferenceRewards[preference.index(truck)] for location, truck in zip(truckLocations, truck1truck2)}
    return(goalPreferences)
