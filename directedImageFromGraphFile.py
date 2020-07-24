import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import os.path as p
import graphClass as gc

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 4
# how large would you like the small squares to be:
sideOfSmallSquares = 1/3
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "x"
# how far would you like to stretch the carpet
stretchFactor = 1


# DEPRECIATED how many relaxations
numRuns = 0

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

# open file for reading
filePath = kogString + "/" + typeOfCarpet + "/" + level + '.txt'
if not p.isfile(filePath):
    print('You need to generate the carpet using saveHarmonicFunction.py')
    exit()
file = open(filePath, "r")

# build carpet from data
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
        avgHarmonic = sum(parameters[4:]) / 4
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


# Chris's code to build the graph
fig = plt.figure()
ax = Axes3D(fig)

thegraph = aCn
graphlen = len(thegraph.vertices)

p1list = []
p2list = []

for vertx in thegraph.vertices:
    vertx = thegraph.vertices[vertx]
    for nghbrstr in vertx[0]:
        nghbr = thegraph.vertices[nghbrstr]
        if nghbr[1][0] > vertx[1][0]:
            cpoint = [vertx[1][0], vertx[1][1], vertx[2]]
            npoint = [nghbr[1][0], nghbr[1][1], nghbr[2]]
            p1list.append(cpoint.copy())
            p2list.append(npoint.copy())
        elif nghbr[1][0] == vertx[1][0] and nghbr[1][1] > vertx[1][1]:
            cpoint = [vertx[1][0], vertx[1][1], vertx[2]]
            npoint = [nghbr[1][0], nghbr[1][1], nghbr[2]]
            p1list.append(cpoint.copy())
            p2list.append(npoint.copy())
        else:
            pass

segmentlist = []
for i in range(len(p1list)):
    segmentlist.append([p1list[i], p2list[i]])

print("length is " + str(len(segmentlist)))
for line in range(len(segmentlist)):
    x = [segmentlist[line][0][0], segmentlist[line][1][0]]
    y = [segmentlist[line][0][1], segmentlist[line][1][1]]
    z = [segmentlist[line][0][2], segmentlist[line][1][2]]
    ax.plot(x, y, z, color='b', linewidth=.5)

ax.view_init(azim=224)
if kindOfGraph == '+':
    kogTitle = 'Crosswire'
else:
    kogTitle = 'X'
plt.title("Harmonic Function On Level " + str(precarpet_level) + " " + str(sideOfSmallSquares.__round__(3)) +
          "-Affine " + kogTitle + " Graph")
plt.savefig(kogString + "/" + typeOfCarpet + "/" + level + "lineGraph.pdf")
plt.show()

