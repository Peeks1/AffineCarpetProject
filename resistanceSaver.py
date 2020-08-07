import graphClass as gc
import numpy as np
import os.path as p

#  INPUT HERE
# what level affine carpets would you like:
precarpet_level = 3
# how large would you like the small squares to be:
sideOfSmallSquares = 1/3
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# how stretched would you like the carpet to be (this will be how far the 0 boundary will be from the 1 boundary
stretchFactor = 1
# how much would you like the resistance calculation to be scaled (if you want to calculate the resistance of larger
#   carpets, use this)
scalingFactor = 1

# how many runs of relaxations on the carpet built from the data (depreciated input)
numRuns = 0
# other important variable calculated from above variables
sideOfCenterHole = 1 - sideOfSmallSquares * 2

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

# get file ready for reading data
filePath = kogString + "/" + typeOfCarpet + "/" + level + '.txt'
if not p.isfile(filePath):
    print('You need to generate the carpet using saveHarmonicFunction.py')
    exit()
file = open(filePath, "r")

# get other file ready for writing data
filePathRes = kogString + "/" + typeOfCarpet + "/" + level + 'resistance.txt'
if p.isfile(filePathRes):
    keypress = input()
    if not keypress == 'y':
        exit()
fileRes = open(filePathRes, "w+")

# build the carpet requested
aCn = gc.Graph()
carpetData = file.readlines()
del carpetData[0]
i = 0
if kindOfGraph == '+':
    for line in carpetData:
        # make list of data from line
        parameters = list(line.split("|"))
        parameters = [float(j) for j in parameters]
        # data from line
        centerPosition = np.array(parameters[0:2])
        vertDisplacement = np.array([0, parameters[2]])
        horizontalDisplacement = np.array([parameters[3], 0])
        topHarmonic = parameters[4]
        bottHarmonic = parameters[5]
        leftHarmonic = parameters[6]
        rightHarmonic = parameters[7]
        avgHarmonic = ((parameters[4] + parameters[5]) * float(vertDisplacement[1]) + (parameters[6] + parameters[7])
                       * float(horizontalDisplacement[0])) / (2 * (float(vertDisplacement[1]) +
                                                                   float(horizontalDisplacement[0])))
        a = 'a' + str(i)
        b = 'b' + str(i)
        c = 'c' + str(i)
        d = 'd' + str(i)
        e = 'e' + str(i)
        aCn.add_vertex(a, centerPosition + vertDisplacement)
        aCn.vertices[a][2] = topHarmonic
        aCn.add_vertex(b, centerPosition - vertDisplacement)
        aCn.vertices[b][2] = bottHarmonic
        aCn.add_vertex(c, centerPosition + horizontalDisplacement)
        aCn.vertices[c][2] = rightHarmonic
        aCn.add_vertex(d, centerPosition - horizontalDisplacement)
        aCn.vertices[d][2] = leftHarmonic
        aCn.add_vertex(e, centerPosition)
        aCn.vertices[e][2] = avgHarmonic
        aCn.add_edge(a, e)
        aCn.add_edge(b, e)
        aCn.add_edge(c, e)
        aCn.add_edge(d, e)
        i += 1
else:
    for line in carpetData:
        # make list of data from line
        parameters = list(line.split("|"))
        parameters = [float(j) for j in parameters]
        # data from line
        centerPosition = np.array(parameters[0:2])
        vertDisplacement = np.array([0, parameters[3]])
        horizontalDisplacement = np.array([parameters[2], 0])
        tlHarmonic = parameters[4]
        blHarmonic = parameters[5]
        brHarmonic = parameters[6]
        trHarmonic = parameters[7]
        avgHarmonic = sum(parameters[4:]) / 4
        a = 'a' + str(i)
        b = 'b' + str(i)
        c = 'c' + str(i)
        d = 'd' + str(i)
        e = 'e' + str(i)
        aCn.add_vertex(a, centerPosition + vertDisplacement - horizontalDisplacement)
        aCn.vertices[a][2] = tlHarmonic
        aCn.add_vertex(b, centerPosition - vertDisplacement - horizontalDisplacement)
        aCn.vertices[b][2] = blHarmonic
        aCn.add_vertex(c, centerPosition + vertDisplacement + horizontalDisplacement)
        aCn.vertices[c][2] = trHarmonic
        aCn.add_vertex(d, centerPosition - vertDisplacement + horizontalDisplacement)
        aCn.vertices[d][2] = brHarmonic
        aCn.add_vertex(e, centerPosition)
        aCn.vertices[e][2] = avgHarmonic
        aCn.add_edge(a, e)
        aCn.add_edge(b, e)
        aCn.add_edge(c, e)
        aCn.add_edge(d, e)
        i += 1
aCn.remove_redundancies()
if numRuns > 0:
    aCn.apply_harmonic_function_affine(setInitialValues=False, numRuns=numRuns)

# calculate resistance
resistance = aCn.resistance_of_graph()

# write resistance to file
fileRes.write("Resistance scaled by " + str(scalingFactor.__round__(3)))
fileRes.write("Resistance is " + str(resistance) + "\n")
print("Resistance is " + str(resistance))
