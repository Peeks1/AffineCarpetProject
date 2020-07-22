import matplotlib.pyplot as plt
import copy
import graphClass as gc
import numpy as np

#  INPUT HERE
# what level affine carpets would you like:
precarpet_level = [1, 2]  # enter a list of sequential integers to avoid the program breaking
# how large would you like the small squares to be:
sideOfSmallSquares = 1/4
# how many runs
numRuns = 100000
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# how stretched would you like the carpet to be (this will be how far the 0 boundary will be from the 1 boundary
stretchFactor = 1

# other important variable calculated from above variables
sideOfCenterHole = 1 - sideOfSmallSquares * 2
precarpet_level.sort()

# file naming variables
kogString = ''
typeOfCarpet = str(sideOfSmallSquares.__round__(3)) + "affineCarpet1x" + str(stretchFactor.__round__(3))
level = 'level' + str(precarpet_level)
if kindOfGraph == '+':
    kogString = 'crossGraphData'
elif kindOfGraph == 'x':
    kogString = 'xGraphData'
else:
    exit()

# get files ready for reading data
files = []
for i in precarpet_level:
    filePath = kogString + "/" + typeOfCarpet + "/" + level + '.txt'
    files.append(open(filePath, "r"))

# build the carpets requested
carpets = []

