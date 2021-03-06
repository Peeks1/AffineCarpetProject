import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import copy
import graphClass as gc
import numpy as np

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 4
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# how large would you like the center hole to be:
sideOfCenterHole = 1/2
# how much do you want to stretch the carpet
stretchFactor = 8


# the above two are the only parameters, since sideOfCenterHole + 2*sideOfSmallSquares = 1 must be true
sideOfSmallSquares = (1 - sideOfCenterHole) / 2

# building the level 0 cross carpet
aC0 = gc.Graph()
if kindOfGraph == "+":
    aC0.add_vertex("a", np.array([0, 0.5]))
    aC0.add_vertex("b", np.array([0.5, 1]))
    aC0.add_vertex("c", np.array([1, 0.5]))
    aC0.add_vertex("d", np.array([0.5, 0]))
    aC0.add_vertex("e", np.array([0.5, 0.5]))
elif kindOfGraph == "x":
    aC0.add_vertex("a", np.array([0, 0]))
    aC0.add_vertex("b", np.array([0, 1]))
    aC0.add_vertex("c", np.array([1, 1]))
    aC0.add_vertex("d", np.array([1, 0]))
    aC0.add_vertex("e", np.array([0.5, 0.5]))
else:
    print("You need to input '+' or 'x' for kindOfGraph")
    exit()

aC0.add_edge("a", "e")
aC0.add_edge('b', 'e')
aC0.add_edge('c', 'e')
aC0.add_edge('d', 'e')

# variables needed for the for loop that builds the precarpet
aCn = gc.Graph()
aCn_plus_one = aC0
copyOfACn = gc.Graph()
# listOfContractionParameters[i][0] is the scaleX
# listOfContractionParameters[i][1] is scaleY
# listOfContractionParameters[i][2] is fixedPoint
listOfContractionParameters = [[sideOfSmallSquares, sideOfSmallSquares, np.array([0, 0])],  # q0
                               [sideOfCenterHole, sideOfSmallSquares, np.array([0.5, 0])],  # q1
                               [sideOfSmallSquares, sideOfSmallSquares, np.array([1, 0])],  # q2
                               [sideOfSmallSquares, sideOfCenterHole, np.array([1, 0.5])],  # q3
                               [sideOfSmallSquares, sideOfSmallSquares, np.array([1, 1])],  # q4
                               [sideOfCenterHole, sideOfSmallSquares, np.array([0.5, 1])],  # q5
                               [sideOfSmallSquares, sideOfSmallSquares, np.array([0, 1])],  # q6
                               [sideOfSmallSquares, sideOfCenterHole, np.array([0, 0.5])]]  # q7

# making carpets and storing their resistances
for k in range(precarpet_level):
    print("making level", k + 1)
    aCn = copy.deepcopy(aCn_plus_one)
    aCn_plus_one = gc.Graph()
    for i in range(0, 8):
        copyOfACn = copy.deepcopy(aCn)
        copyOfACn.update_all_vertices_names(str(i))
        copyOfACn.contract_graph_affine(listOfContractionParameters[i][0], listOfContractionParameters[i][1],
                                        listOfContractionParameters[i][2])
        aCn_plus_one.add_graph(copyOfACn)
    aCn_plus_one.remove_redundancies()
print("done constructing")

# stetching and applying harmonic
for v in aCn_plus_one.vertices:
    aCn_plus_one.vertices[v][1] = np.multiply(aCn_plus_one.vertices[v][1], [stretchFactor, 1])
aCn_plus_one.apply_harmonic_function_affine(numRuns=1000, stretchFactor=stretchFactor)

# plotting
x = []
y = []
f = []
for v in aCn_plus_one.vertices:
    x.append(aCn_plus_one.vertices[v][1][0])
    y.append(aCn_plus_one.vertices[v][1][1])
    f.append(aCn_plus_one.vertices[v][2])

fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlabel('x')
ax.set_ylabel('y')

cm = plt.get_cmap('plasma')
scalarMap = cmx.ScalarMappable(cmap=cm)

ax.scatter(x, y, f, c=scalarMap.to_rgba(f))
ax.view_init(azim=224)

# parts that depend on if + or x
if kindOfGraph == '+':
    plt.title("Harmonic Function On Level " + str(precarpet_level) + " " + str(sideOfSmallSquares.__round__(3)) +
              "-Affine Crosswire 1x" + str(stretchFactor) + "Graph ")
    plt.savefig(str(sideOfSmallSquares.__round__(3)) + "affine1x" + str(stretchFactor) + "CrosswireHarmonicOnLevel" +
                str(precarpet_level) + ".pdf")
elif kindOfGraph == 'x':
    plt.title("Harmonic Function On Level " + str(precarpet_level) + " " + str(sideOfSmallSquares.__round__(3)) +
              "-Affine X 1x" + str(stretchFactor) + "Graph")
    plt.savefig(str(sideOfSmallSquares.__round__(3)) + "affine1x" + str(stretchFactor) + "XHarmonicOnLevel" +
                str(precarpet_level) + ".pdf")

plt.show()
