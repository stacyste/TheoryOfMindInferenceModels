import unittest
from BayesianInference import getPosterior

class TestPosterior(unittest.TestCase):
    def setUp(self):
        
        self.PriorA = {'gold': 3/6, 'silver': 1/6, 'bronze': 2/6}
        self.PriorB = {'samoas': 3/20, 'tagalogs':2/20, 'mintthins': 14/20, 'lemondrops':1/20}
        self.Likelihood = {('gold', 'samoas'): 0.4, ('gold', 'tagalogs'): 0.3, ('gold', 'mintthins'): 0.25, ('gold', 'lemondrops'): 0.05, ('silver', 'samoas'): 0.72, ('silver', 'tagalogs'): 0.54, ('silver', 'mintthins'): 0.45, ('silver', 'lemondrops'): 0.09, ('bronze', 'samoas'): 0.16, ('bronze', 'tagalogs'): 0.12, ('bronze', 'mintthins'): 0.1, ('bronze', 'lemondrops'): 0.02}
        
    def testPosterior(self):
        
        roundingAllowance = 6
        truePosteriorA, truePosteriorB = [{'gold': 0.5357142857142856,'silver': 0.3214285714285714,'bronze': 0.14285714285714282},{'samoas': 0.22429906542056074,'tagalogs': 0.11214953271028037,'mintthins': 0.6542056074766355,'lemondrops': 0.009345794392523367}]
        testingPosteriorA, testingPosteriorB = getPosterior(self.PriorA, self.PriorB, self.Likelihood)
        
        roundedTruePosteriorA = {k:round(v, roundingAllowance) for k,v in truePosteriorA.items()}
        roundedTruePosteriorB = {k:round(v, roundingAllowance) for k,v in truePosteriorB.items()}

        roundedTestingPosteriorA = {k:round(v, roundingAllowance) for k,v in testingPosteriorA.items()}
        roundedTestingPosteriorB = {k:round(v, roundingAllowance) for k,v in testingPosteriorB.items()}

        self.assertDictEqual(roundedTruePosteriorA, roundedTestingPosteriorA)
        self.assertDictEqual(roundedTruePosteriorB, roundedTestingPosteriorB)
    
        
    def tearDown(self):
        pass