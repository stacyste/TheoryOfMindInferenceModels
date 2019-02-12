"""
Class: Stat232C
Project 1: Bayesian inference Answer Key
Name: Stephanie Stacy
Date: January 2019

"""

def normalizeDictionaryValues(unnormalizedDictionary):
    totalSum = sum(unnormalizedDictionary.values())
    normalizedDictionary = {originalKey: val/totalSum for originalKey, val in unnormalizedDictionary.items()}
    return(normalizedDictionary)

def getMarginalizedOutcomeProbability(outcome, jointPMF):
    probabilityOfOutcome = sum([jointPMF[(keyOne, keyTwo)] if (keyOne==outcome) or (keyTwo==outcome)  else 0 for (keyOne, keyTwo) in jointPMF.keys()])
    return(probabilityOfOutcome)

def calculateOutcomePosterier(priorOfA, priorOfB, likelihood, aEvent, bEvent):
    posterior = priorOfA[aEvent]*priorOfB[bEvent]*likelihood[(aEvent, bEvent)]
    return(posterior)


def getPosterior(priorOfA, priorOfB, likelihood):
    unnormalizedJointPosterior = {(aEvent, bEvent): calculateOutcomePosterier(normalizedPriorOfA, normalizedPriorOfB, likelihood, aEvent, bEvent) \
                      for aEvent, bEvent in likelihood.keys()}
    jointPosterior = normalizeDictionaryValues(unnormalizedJointPosterior)
    
    marginalOfA = {keyOfA : getMarginalizedOutcomeProbability(keyOfA, jointPosterior) for keyOfA in normalizedPriorOfA.keys()}
    marginalOfB = {keyOfB : getMarginalizedOutcomeProbability(keyOfB, jointPosterior) for keyOfB in normalizedPriorOfB.keys()}
    return([marginalOfA, marginalOfB])



def main():
    exampleOnePriorofA = {'a0': .5, 'a1': .5}
    exampleOnePriorofB = {'b0': .25, 'b1': .75}
    exampleOneLikelihood = {('a0', 'b0'): 0.42, ('a0', 'b1'): 0.12, ('a1', 'b0'): 0.07, ('a1', 'b1'): 0.02}
    print(getPosterior(exampleOnePriorofA, exampleOnePriorofB, exampleOneLikelihood))

    exampleTwoPriorofA = {'red': 1/10 , 'blue': 4/10, 'green': 2/10, 'purple': 3/10}
    exampleTwoPriorofB = {'x': 1/5, 'y': 2/5, 'z': 2/5}
    exampleTwoLikelihood = {('red', 'x'): 0.2, ('red', 'y'): 0.3, ('red', 'z'): 0.4, ('blue', 'x'): 0.08, ('blue', 'y'): 0.12, ('blue', 'z'): 0.16, ('green', 'x'): 0.24, ('green', 'y'): 0.36, ('green', 'z'): 0.48, ('purple', 'x'): 0.32, ('purple', 'y'): 0.48, ('purple', 'z'): 0.64}
    print(getPosterior(exampleTwoPriorofA, exampleTwoPriorofB, exampleTwoLikelihood))



if __name__ == '__main__':
	main()