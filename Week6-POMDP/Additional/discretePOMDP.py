import itertools
from ValueIteration import *

class SetupBeliefTransition(object):
    def __init__(self, positionSet, beliefSet, actionSet, observationPositionSet):
        self.positionSet = positionSet
        self.beliefSet = beliefSet
        self.actionSet = actionSet
        self.observationPositionSet = observationPositionSet

    def __call__(self, sign):
		##############################################
		######### Your Code Here #####################
		##############################################
        return(beliefTransitionTable)

class SetupRewardBeliefTable(object):
    def __init__(self, positionSet, beliefSet, actionSet):
        self.positionSet = positionSet
        self.beliefSet = beliefSet
        self.actionSet = actionSet
        
    def __call__(self, beliefTransition, worldRewardList):
    	##############################################
		######### Your Code Here #####################
		##############################################
        return(rewardTable)


def main():
	#actions
	allActions = [(1,0), (0,1), (-1,0), (0,-1), (0,0)] # Actions correspond to E, N, W, S, Stay respectively

	#states
	gridWidth = 5
	gridHeight = 5
	gridSet = set(itertools.product(range(gridWidth), range(gridHeight))) #all location states in grid
	barriers = {(2,1), (3,1), (4,1)} #set of states to remove from each environment
	positionSet = list(gridSet.difference(barriers)) #final environment state sets
	beliefSet = [0,-1,1] #possible world beliefs

	#observations
	positionsToObserveSign = [(0,0), (1,0), (2,0), (3,0), (4,0)] #positions where you can observe the sign 

	#belief transitions for each true world
	getBeliefTransition = SetupBeliefTransition(positionSet, beliefSet, allActions, positionsToObserveSign)
	
	"""	
	YOUR CODE HERE: 
	world1BeliefTransitionTable = 
	world2BeliefTransitionTable = 
	"""

	#reward(s,a)
	rewardWorld1 = {(3, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(3, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 4): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 1): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(2, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(4, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(2, 4): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(4, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 1): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(3, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(4, 4): {(1, 0): -100,(0, 1): -100,(-1, 0): -100,(0, -1): -100,(0, 0): -100},(2, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 4): {(1, 0): 9, (0, 1): 9, (-1, 0): 9, (0, -1): 9, (0, 0): 9.9},(4, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(2, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(3, 4): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1}}
	rewardWorld2 = {(3, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(3, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 4): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 1): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(2, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(4, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(2, 4): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(4, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(1, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 1): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(3, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(4, 4): {(1, 0): 9, (0, 1): 9, (-1, 0): 9, (0, -1): 9, (0, 0): 9.9},(2, 0): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 4): {(1, 0): -100,(0, 1): -100,(-1, 0): -100,(0, -1): -100,(0, 0): -100},(4, 3): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(2, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(3, 4): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1},(0, 2): {(1, 0): -1, (0, 1): -1, (-1, 0): -1, (0, -1): -1, (0, 0): -0.1}}

	#belief reward
	"""	
	YOUR CODE HERE: 
	getRewardBelief = 
	world1BeliefReward = 
	world2BeliefReward = 
	"""

	#perform value iteration
	world1ValueTable = {state:0 for state in world1BeliefTransitionTable.keys()}
	world2ValueTable = {state:0 for state in world2BeliefTransitionTable.keys()}
	epsilon = 10e-7
	gamma = .9
	beta = .8
	##############################################
	######### Your Code Here #####################
	##############################################

	"""
	YOUR CODE HERE:
	policyWorld1 = 
	policyWorld2 = 
	"""

	return([policyWorld1, policyWorld2])

if __name__ == '__main__':
	main()








