import numpy as np
import itertools

def setUpBayesianInference(eventAMeanSampleSpaceSize, eventBMeanSampleSpaceSize, randomSeed, isPriorUniform=False):
    np.random.seed(randomSeed)
    aProbabilities = constructRandomPMF(eventAMeanSampleSpaceSize, 'a')
    bProbabilities = constructRandomPMF(eventBMeanSampleSpaceSize, 'b')
    jointProbabilities = getJointPMFOfTwoEvents(aProbabilities, bProbabilities)
    
    sampleSpaceANames = list(aProbabilities.keys())
    sampleSpaceBNames = list(bProbabilities.keys())
    
    aPrior = constructPrior(sampleSpaceANames,isPriorUniform)
    bPrior = constructPrior(sampleSpaceBNames,isPriorUniform)
    
    likelihood = generateLikelihood(jointProbabilities)
    
    return([jointProbabilities,  aPrior,  bPrior, likelihood])


def normalizeDictionaryValues(unnormalizedDictionary):
    totalSum = sum(unnormalizedDictionary.values())
    normalizedDictionary = {originalKey: val/totalSum for originalKey, val in unnormalizedDictionary.items()}
    return(normalizedDictionary)

def constructRandomPMF(meanSampleSpaceSize, eventIDString):
    sampleSpaceSize = np.maximum(2, np.random.poisson(meanSampleSpaceSize))
    outcomeNames = [eventIDString+str(outcomeIndex) for outcomeIndex in range(sampleSpaceSize)]
    unnormalizedProbabilities = {outcome: np.random.random() for outcome in outcomeNames}
    eventPMF = normalizeDictionaryValues(unnormalizedProbabilities)
    return(eventPMF)

def getJointPMFOfTwoEvents(eventAPMF, eventBPMF):
    jointPMF = {(keya, keyb):eventAPMF[keya]*eventBPMF[keyb] for keya, keyb in itertools.product(eventAPMF.keys(), eventBPMF.keys())}
    return(jointPMF)

def generateLikelihood(jointDistribution):
    likelihood = {jointKey: np.random.random() for jointKey in jointDistribution.keys()}
    return(likelihood)

def constructPrior(namesOfAllOutcomes, isUniform = False):
    if isUniform:
        prior = {a: 1/len(namesOfAllOutcomes) for a in namesOfAllOutcomes}
    else:
        unnormalizedPrior = {outcome: np.random.random() for outcome in namesOfAllOutcomes}
        prior = normalizeDictionaryValues(unnormalizedPrior)
    return(prior)


def main():
	generativeDistribution, priorA, priorB, likelihood = setUpBayesianInference(5, 5, 2)
	print(generativeDistribution)
	print(priorA)
	print(priorB)
	print(likelihood)

if __name__ == '__main__':
	main()