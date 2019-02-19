import itertools
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def visualizeEnvironment(gridWidth, gridHeight, states, goalStates, trajectory = []):
    #grid height/width
    gridAdjust = .5
    gridScale = 1.5
    arrowScale = .7
    
    plt.rcParams["figure.figsize"] = [gridWidth*gridScale,gridHeight*gridScale]
    ax = plt.gca(frameon=False, xticks = range(-1, gridWidth+1), yticks = range(-1, gridHeight+1))

    #goal and trap coloring 
    for (goalx,goaly, goalName) in goalStates:
        ax.add_patch(Rectangle((goalx-gridAdjust, goaly-gridAdjust), 1, 1, fill=True, color='green', alpha=.1))
        ax.text(goalx-.15, goaly-.15, goalName, fontsize = 35)
    
    #gridline drawing
    for (statex, statey) in states:
        ax.add_patch(Rectangle((statex-gridAdjust, statey-gridAdjust), 1, 1, fill=False, color='black', alpha=1))

    #trajectory path coloring
    for indx, (statex, statey) in enumerate(trajectory):
        ax.add_patch(Rectangle((statex-gridAdjust, statey-gridAdjust), 1, 1, fill=True, color='blue', alpha=.1))
        ax.text(statex-.1, statey-.1, str(indx), fontsize = 25)
    plt.show()
    
levelsReward  = ["state", "action", "next state", "reward"]
levelsSAReward = ["state", "action", "reward"]
levelsTransition  = ["state", "action", "next state", "probability"]

def viewDictionaryStructure(d, levels, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(levels[indent]) + ": "+ str(key))
        if isinstance(value, dict):
            viewDictionaryStructure(value, levels, indent+1)
        else:
            print('\t' * (indent+1) + str(levels[indent+1])+ ": " + str(value))