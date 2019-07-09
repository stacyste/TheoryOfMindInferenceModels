import numpy as np
import itertools

def setUpBayesianInference(eventAMeanSampleSpaceSize, eventBMeanSampleSpaceSize, randomSeed, isPriorUniform=False):
    np.random.seed(randomSeed)
    
    aLikelihood = constructRandomLikelihood(eventAMeanSampleSpaceSize, 'a')
    bLikelihood = constructRandomLikelihood(eventBMeanSampleSpaceSize, 'b')
    
    jointLikelihood = getJointLikelihood(aLikelihood, bLikelihood)
    
    sampleSpaceANames = list(aLikelihood.keys())
    sampleSpaceBNames = list(bLikelihood.keys())
    
    aPrior = constructPrior(sampleSpaceANames,isPriorUniform)
    bPrior = constructPrior(sampleSpaceBNames,isPriorUniform)
    
    return([aPrior,  bPrior, jointLikelihood])


def constructRandomLikelihood(meanSampleSpaceSize, eventIDString):
    sampleSpaceSize = np.maximum(2, np.random.poisson(meanSampleSpaceSize))
    outcomeNames = [eventIDString+str(outcomeIndex) for outcomeIndex in range(sampleSpaceSize)]
    likelihood = {outcome: np.random.random() for outcome in outcomeNames}
    return(likelihood)

def getJointLikelihood(eventAPMF, eventBPMF):
    jointPMF = {(keya, keyb):eventAPMF[keya]*eventBPMF[keyb] for keya, keyb in itertools.product(eventAPMF.keys(), eventBPMF.keys())}
    return(jointPMF)

def constructPrior(namesOfAllOutcomes, isUniform = False):
    if isUniform:
        prior = {a: 1/len(namesOfAllOutcomes) for a in namesOfAllOutcomes}
    else:
        unnormalizedPrior = {outcome: np.random.random() for outcome in namesOfAllOutcomes}
        prior = normalizeDictionaryValues(unnormalizedPrior)
    return(prior)

def normalizeDictionaryValues(unnormalizedDictionary):
    totalSum = sum(unnormalizedDictionary.values())
    normalizedDictionary = {originalKey: val/totalSum for originalKey, val in unnormalizedDictionary.items()}
    return(normalizedDictionary)


def main():
	priorA, priorB, likelihood = setUpBayesianInference(5, 5, 2)
	print(priorA)
	print(priorB)
	print(likelihood)

if __name__ == '__main__':
	main()