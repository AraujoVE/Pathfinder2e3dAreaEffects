import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir


def createImage(csvPath,imgPath):

    tab = pd.read_csv(csvPath,header=None)

    maxVal = 1
    for i in tab.values:
        for j in i:
            if j != "-" and int(j) > maxVal:
                maxVal = int(j)

    colorArray = [[((int(j)/(1.5*maxVal),1 - int(j)/maxVal,1 - int(j)/(2*maxVal),0.5) if j != "-" else (0,0,0,0))for j in i] for i in tab.values]
    cellsNo = len(tab)
    figSize = 10
    cellRatio = 8
    cellsSize = figSize/(len(tab)*cellRatio)
    fig, ax = plt.subplots(figsize=(figSize,figSize))
    ytable = ax.table(cellText=tab.values, loc='center', cellLoc="center",cellColours=colorArray)

    cellDict = ytable.get_celld()
    for i in range(cellsNo):
        for j in range(cellsNo):
            cellDict[i,j].set_height(cellsSize)
            cellDict[i,j].set_width(cellsSize)
            cellDict[i,j]

    ytable.set_fontsize(25)
    ax.axis('off')
    ax.axis('off')
    fig.patch.set_visible(False)
    plt.box(False)
    ax.set(frame_on=False)
    plt.savefig(imgPath)


for f in listdir('./areas3d/'):
    if f.endswith('.csv'):
        createImage('./areas3d/'+f,'./imagesToCrop/images/'+f.split(".csv")[0] + ".png")
