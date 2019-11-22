import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


#Belief Transition funtion
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

#Helper functions for belief transition
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

#Setup reward function
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

#Trajectory sampling
def samplePathToGoal(position, belief, policy, transition, goals):
    trajectory = [(position, belief)]

    while position not in goals:
        #take action probabilisitically
        actions = list(policy[(position, belief)].keys())
        probOfAction = [policy[(position, belief)][action] for action in actions]
        actionIndex = np.random.choice(len(actions), 1, p = probOfAction)
        sampledAction = actions[int(actionIndex)]
        
        #get new position and belief
        newPosition = list(transition[(position, belief)][sampledAction].keys())[0][0]
        possibleBeliefs = list(transition[(position, belief)][sampledAction].keys())
        sampledNewBeliefIndex = int(np.random.choice(len(possibleBeliefs), 1))
        
        #update to new belief/position and add to trajectory
        belief = possibleBeliefs[sampledNewBeliefIndex][1]
        position = newPosition
        trajectory.append((position, belief))
    return(trajectory)

#Inference functions
def inferBelief(positionTrajectory, world, initialBelief = (.17,.17,.17,.17,.17,.17)):
    positionsTruck1Visible = [(0, 0),(1, 3),(3, 0),(0, 2),(2, 1),(1, 0),(0, 3),(4, 0),(0, 1),(1, 2),(3, 1),(2, 0),(4, 1),(1, 1)]
    positionsTruck2Visible = [(0,3), (1,3), (2,3), (3,3), (4,3)] 
    
    stateTrajectory = [(positionTrajectory[0], initialBelief)]
    beliefAtTimeT = initialBelief
    for position in positionTrajectory[1:]:
        observation = ["", ""]
        if position in positionsTruck1Visible:
            observation[0] = world[0] 
        if position in positionsTruck2Visible:
            observation[1] = world[1]
        beliefAtTimeT = createBelief(beliefAtTimeT, tuple(observation))   
        stateTrajectory.append((position, beliefAtTimeT))
    return(stateTrajectory)

class PerformDesireInference(object):
    def __init__(self, transitionTable, desirePolicies, desirePriors, stateTrajectory):
        self.transitionTable = transitionTable
        self.desirePolicies  = desirePolicies
        self.desirePriors = desirePriors
        self.stateTrajectory = stateTrajectory

    def __call__(self):
        posterior = self.getSequenceOfBeliefProbabilities()*np.array(self.desirePriors)        
        row_sums = posterior.sum(axis=1, keepdims=True)
        normalizedPosterior = posterior / row_sums
        return(normalizedPosterior)
        
    def getNextStateProbability(self, state, nextState, policy):
        possibleActionsToNextState = [action for action in self.transitionTable[state] \
                                      if nextState in self.transitionTable[state][action]]

        probNextState = sum([self.transitionTable[state][action][nextState]*policy[state][action] \
                             for action in possibleActionsToNextState])
        return(probNextState)
    
    def getSequenceOfBeliefProbabilities(self):
        probNextState = [self.desirePriors]
        for t, state in enumerate(self.stateTrajectory[:-1]):
            nextState = self.stateTrajectory[t+1]
            probNextState.append([self.getNextStateProbability(state, nextState, desirePolicy) \
                         for desirePolicy in self.desirePolicies])
        observedStateProbs = np.cumprod(np.array(probNextState), axis=0)
        return(observedStateProbs)

# Visualization Tool
"""
    Visualizes policy of a given belief state where the input is a set of states to visualize instead of a grid - can take in irregular state spaces.
    Inputs: 
        states: list of state position tuples (x,y)
        policy: probability of an action given the state s is of form (positionx, positiony), belief
        belief: the belief state for which to visualize the policy
        goalStates: list of possible goals 
        trapStates: list of obstacle or trap spaces
        trajectory: list of states an agent travels through
"""
def visualizePolicyOfBeliefByState_FoodTruck(states, policy, belief, goalStates = [], trapStates = [], trajectory = [], arrowScale = .3, orderedWorlds = ['KL', 'KM', 'LK', 'LM', 'MK', 'ML']):
    gridAdjust = .5
    gridScale = 1.5
    
    minimumx, minimumy = [min(coord) for coord in zip(*states)]
    maximumx, maximumy = [max(coord) for coord in zip(*states)]
    
    plt.rcParams["figure.figsize"] = [(maximumx-minimumx)*gridScale, (maximumy-minimumy)*gridScale]
    ax = plt.gca(frameon=False, xticks = range(minimumx-1, maximumx+2), yticks = range(minimumy-1, maximumy+2))

    #gridline drawing
    for (statex, statey) in states:
        ax.add_patch(Rectangle((statex-gridAdjust, statey-gridAdjust), 1, 1, fill=False, color='black', alpha=1))

    #goal and trap coloring 
    for (goalx,goaly) in goalStates:
        ax.add_patch(Rectangle((goalx-gridAdjust, goaly-gridAdjust), 1, 1, fill=True, color='green', alpha=.1))
    for (trapx, trapy) in trapStates:
        ax.add_patch(Rectangle((trapx-gridAdjust, trapy-gridAdjust), 1, 1, fill=True, color='red', alpha=.1))

    #trajectory path coloring
    for indx, (statex, statey) in enumerate(trajectory):
        ax.add_patch(Rectangle((statex-gridAdjust, statey-gridAdjust), 1, 1, fill=True, color='blue', alpha=.1))
        ax.text(statex-.1, statey-.1, str(indx), fontsize = 25)
    
    #Truck Label for Belief
    consistentBeliefs = [world for b, world in zip(belief, orderedWorlds) if b > 0]
    truck1 = [z[0] for z in consistentBeliefs]
    truck2 = [z[1] for z in consistentBeliefs]
    
    if all(x == truck1[0] for x in truck1):
        #label truck 1
        ax.text(0-.15, 0-.15, truck1[0], fontsize = 25)
    else: 
        ax.text(0-.15, 0-.15, "?", fontsize = 25)
    
    if all(x == truck2[0] for x in truck2):
        #label truck 2
        ax.text(4-.15, 3-.15, truck2[0], fontsize = 25)
    else: 
        ax.text(4-.15, 3-.15, "?", fontsize = 25)

    #labeled values
    for ((statex, statey), b) in policy.keys():
        if b == belief:
            for (actionx, actiony), actionProb in policy[((statex, statey), b)].items():
                plt.arrow(statex, statey, actionx*actionProb*arrowScale, actiony*actionProb*arrowScale, head_width=0.05*actionProb, head_length=0.1*actionProb)    
    plt.show()