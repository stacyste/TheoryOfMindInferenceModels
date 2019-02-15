import unittest
from TransitionTableSetup import *

class TestEpsilonTransition(unittest.TestCase):
    def setUp(self):
        stateSpace = set(itertools.product(range(5), range(5)))
        cardinalActionSet = [(1,0), (0,1), (-1,0), (0,-1), (0,0)]
        cardinalWithDiagonalActionSet = [(1,0), (0,1), (-1,0), (0,-1), (0,0), (1,-1), (-1,1), (1, 1), (-1, -1)]
        
        getCardinalTransition = SetupEpsilonTransition(stateSpace, cardinalActionSet)
        getDiagonalTransition = SetupEpsilonTransition(stateSpace, cardinalWithDiagonalActionSet)

        self.cardinalDeterministicTransition = getCardinalTransition(0)
        self.cardinalProbabilisticTransition = getCardinalTransition(.5)

        self.diagonalDeterministicTransition = getDiagonalTransition(0)
        self.diagonalProbabilisticTransition = getDiagonalTransition(.5)


    def testInteriorAction(self):
        pass

    def testEdgeAction(self):
        pass
  
    def tearDown(self):
        pass


class TestTransitionSingleAgentCardinal(unittest.TestCase):
    def setUp(self):
        state_space = ((-5,5), (-5,5))
        self.transition = src.transition.Transition2dGridSingleAgentCardinal(state_space)
    
    def test_normal_actions(self):
        curr_state = ((0,0), (0,0))
        next_states = {ActionCardinal.UP: ((0,1) , (0,0)),
                       ActionCardinal.DOWN: ((0,-1), (0,0)),
                       ActionCardinal.LEFT: ((-1,0), (0,0)),
                       ActionCardinal.RIGHT: ((1,0) , (0,0)),
                       ActionCardinal.STAY: curr_state}
        for action in ActionCardinal:
            next_state = self.transition(curr_state, action)
            self.assertEqual(next_state, next_states[action])
        
    def test_out_of_bounds(self):
        curr_state = ((5,5), (0,0))
        next_states = {ActionCardinal.UP: curr_state,
                       ActionCardinal.DOWN: ((5,4), (0,0)),
                       ActionCardinal.LEFT: ((4,5), (0,0)),
                       ActionCardinal.RIGHT: curr_state,
                       ActionCardinal.STAY: curr_state}
        for action in ActionCardinal:
            next_state = self.transition(curr_state, action)
self.assertEqual(next_state, next_states[action])