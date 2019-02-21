"""
Class: Stat232C
Project 1: Bayesian inference Solution
Name: Stephanie Stacy
Date: January 2019

"""

def getPosterior(priorOfA, priorOfB, likelihood):
    unnormalizedJointPosterior = {(aEvent, bEvent): calculateOutcomePosterier(priorOfA, priorOfB, likelihood, aEvent, bEvent) \
                      for aEvent, bEvent in likelihood.keys()}
    jointPosterior = normalizeDictionaryValues(unnormalizedJointPosterior)
    
    marginalOfA = {keyOfA : getMarginalizedOutcomeProbability(keyOfA, jointPosterior) for keyOfA in priorOfA.keys()}
    marginalOfB = {keyOfB : getMarginalizedOutcomeProbability(keyOfB, jointPosterior) for keyOfB in priorOfB.keys()}
    return([marginalOfA, marginalOfB])

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


def main():
    exampleOnePriorofA = {'a0': .5, 'a1': .5}
    exampleOnePriorofB = {'b0': .25, 'b1': .75}
    exampleOneLikelihood = {('a0', 'b0'): 0.42, ('a0', 'b1'): 0.12, ('a1', 'b0'): 0.07, ('a1', 'b1'): 0.02}
    print(getPosterior(exampleOnePriorofA, exampleOnePriorofB, exampleOneLikelihood))

    exampleTwoPriorofA = {'red': 1/10 , 'blue': 4/10, 'green': 2/10, 'purple': 3/10}
    exampleTwoPriorofB = {'x': 1/5, 'y': 2/5, 'z': 2/5}
    exampleTwoLikelihood = {('red', 'x'): 0.2, ('red', 'y'): 0.3, ('red', 'z'): 0.4, ('blue', 'x'): 0.08, ('blue', 'y'): 0.12, ('blue', 'z'): 0.16, ('green', 'x'): 0.24, ('green', 'y'): 0.36, ('green', 'z'): 0.48, ('purple', 'x'): 0.32, ('purple', 'y'): 0.48, ('purple', 'z'): 0.64}
    print(getPosterior(exampleTwoPriorofA, exampleTwoPriorofB, exampleTwoLikelihood))

    from setUpBayesianInference import setUpBayesianInference
    exampleOnePriorA, exampleOnePriorB, exampleOneLikelihood = setUpBayesianInference(5, 10, 100)
    print(getPosterior(exampleOnePriorA, exampleOnePriorB, exampleOneLikelihood))
    
    exampleTwoPriorA = {'gold': 3/6, 'silver': 1/6, 'bronze': 2/6}
    exampleTwoPriorB = {'samoas': 3/20, 'tagalogs':2/20, 'mintthins': 14/20, 'lemondrops':1/20}
    exampleTwoLikelihood = exampleThreeLikelihood = {('gold', 'samoas'): 0.4, ('gold', 'tagalogs'): 0.3, ('gold', 'mintthins'): 0.25, ('gold', 'lemondrops'): 0.05, ('silver', 'samoas'): 0.72, ('silver', 'tagalogs'): 0.54, ('silver', 'mintthins'): 0.45, ('silver', 'lemondrops'): 0.09, ('bronze', 'samoas'): 0.16, ('bronze', 'tagalogs'): 0.12, ('bronze', 'mintthins'): 0.1, ('bronze', 'lemondrops'): 0.02}
    print(getPosterior(exampleTwoPriorA, exampleTwoPriorB, exampleTwoLikelihood))


if __name__ == '__main__':
	main()