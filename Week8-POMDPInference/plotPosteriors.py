import matplotlib.pyplot as plt

def plotPosteriors(posteriors, title="", labels=['KLM', 'KML', 'LKM', 'LMK', 'MKL', 'MLK'], subplotRowNumber = 2, subplotColNumber = 3, figDim = (10,5)):
    x, y  = posteriors.shape
    fig, ax = plt.subplots(nrows=subplotRowNumber, ncols=subplotColNumber, figsize = figDim)
    colors = plt.cm.viridis(np.linspace(0,1,y))
    plotIndex = 0 
    for row in ax:
        for col in row:
            col.plot(range(x), posteriors[:,plotIndex], color = colors[plotIndex], label = labels[plotIndex])
            col.legend()
            plotIndex += 1
    fig.suptitle(title)
    plt.show()