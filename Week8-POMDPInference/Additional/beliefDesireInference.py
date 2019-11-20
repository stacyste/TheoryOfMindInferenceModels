# Environment
stateSet = [(0, 0),(1, 3),(3, 0),(0, 2),(2, 1),(2, 3),(1, 0),(0, 3),(4, 0),(0, 1),(1, 2),(3, 3),(3, 1),(2, 0),(4, 3),(4, 1),(1, 1)]
actionSet = [(1,0), (0,1), (-1,0), (0,-1), (0,0)]

truck1Location = (0,0)
truck2Location = (4,3)

allWorlds = ['KL', 'KM', 'LK', 'LM', 'MK', 'ML']

#Rewards
mostDesiredFood = 100
middleDesiredFood = 75
leastDesiredFood = 50
actionCost = -1
stayCost = -.1

#Parameters for Value Iteration
convergenceTolerance =10e-7
gamma = .99
beta = .8

# Example 1
beliefAtTime0 = (.17,.17,.17,.17,.17,.17)
example1World = ("LK")
example1PositionTrajectory = [(4, 1),(3, 1),(2, 1),(1, 1),(1, 2),(1, 3),(0, 3),(0, 2),(0, 1),(0, 0)]

#Example 2
beliefAtTime0 = (.17,.17,.17,.17,.17,.17)
example2World = ("LM")
example2PositionTrajectory = [(4, 1), (3, 1), (3, 0), (2, 0), (1, 0), (0, 0)]

#Example 3
beliefAtTime0 = (.17,.17,.17,.17,.17,.17)
example3World = ("LM")
example3PositionTrajectory = [(4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)]