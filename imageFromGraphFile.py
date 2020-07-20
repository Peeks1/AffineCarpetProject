import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import graphClass as gc
import os.path as p

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 4
# how large would you like the small squares to be:
sideOfSmallSquares = 1 / 4
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"

# file naming variables
kogString = ''
typeOfCarpet = str(sideOfSmallSquares.__round__(3)) + "affineCarpet"
level = 'level' + str(precarpet_level)
if kindOfGraph == '+':
    kogString = 'crossGraph'
elif kindOfGraph == 'x':
    kogString = 'xGraph'
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
aCn.remove_redundancies()
aCn.apply_harmonic_function_affine(setInitialValues=False, numRuns=200)
# build picture
x = []
y = []
f = []
for v in aCn.vertices:
    x.append(aCn.vertices[v][1][0])
    y.append(aCn.vertices[v][1][1])
    f.append(aCn.vertices[v][2])

fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlabel('x')
ax.set_ylabel('y')

cm = plt.get_cmap('winter')
scalarMap = cmx.ScalarMappable(cmap=cm)

ax.scatter(x, y, f, c=scalarMap.to_rgba(f), s=10, depthshade=False)
ax.view_init(azim=224)

# parts that depend on if + or x
if kindOfGraph == '+':
    kogTitle = 'Crosswire'
else:
    kogTitle = 'X'
plt.title("Harmonic Function On Level " + str(precarpet_level) + " " + str(sideOfSmallSquares.__round__(3)) +
          "-Affine " + kogTitle + " Graph")
plt.savefig(kogString + "/" + typeOfCarpet + "/" + level + ".pdf")
plt.show()
