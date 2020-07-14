import matplotlib.pyplot as plt
import copy
import graphClass as gc
import numpy as np

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 4
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# how large would you like the center hole to be:
sideOfSmallSquares = 1/4
# what n's would you like to analyze (where the carpets analyzed are 1xn and the distance between the boundary points
# is n
nValues = [1/8, 1/6, 1/4, 1/2]
nValues.sort()

# the above two are the only parameters, since sideOfCenterHole + 2*sideOfSmallSquares = 1 must be true
sideOfCenterHole = 1 - sideOfSmallSquares * 2

# building the level 0 carpet
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
# variables for plotting
countingList = []
listOfResistances = []

# making the 1x1 carpet
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

'''# calculating the resistance of the 1xn carpets
for n in nValues:
    print("calculating resistance of 1x" + str(n))
    countingList.append(n.__round__(3))
    stretchedACn = copy.deepcopy(aCn_plus_one)
    for v in stretchedACn.vertices:
        stretchedACn.vertices[v][1] = np.multiply(stretchedACn.vertices[v][1], [n, 1])
    stretchedACn.apply_harmonic_function_affine(stretchFactor=n)
    listOfResistances.append(stretchedACn.resistance_of_graph())'''

# calculating rho of the 1xn carpets
for n in nValues:
    print("calculating rho of 1x" + str(n))
    countingList.append(n.__round__(3))
    stretchedACn = copy.deepcopy(aCn)
    stretchedACn_plus_one = copy.deepcopy(aCn_plus_one)
    for v in stretchedACn.vertices:
        stretchedACn.vertices[v][1] = np.multiply(stretchedACn.vertices[v][1], [n, 1])
    for v in stretchedACn_plus_one.vertices:
        stretchedACn_plus_one.vertices[v][1] = np.multiply(stretchedACn_plus_one.vertices[v][1], [n, 1])
    stretchedACn.apply_harmonic_function_affine()
    stretchedACn_plus_one.apply_harmonic_function_affine()
    listOfResistances.append(stretchedACn_plus_one.resistance_of_graph() / stretchedACn.resistance_of_graph())

# placing plot points
plt.plot(countingList, listOfResistances, "bo")

# adding text to plot
plt.xlabel("Stretching Factor")
plt.ylabel("Resistance of Graph")
plt.xticks(nValues)
plt.yticks(list(range(int(max(listOfResistances) + 3))))
for r in listOfResistances:
    plt.text(nValues[listOfResistances.index(r)], r + .1, r.__round__(3))

# parts that depend on if + or x
if kindOfGraph == '+':
    plt.title("Rho of the Stretched Level " + str(precarpet_level) + " " + str(sideOfSmallSquares.__round__(3)) +
              "-Affine Crosswire Graph")
    plt.savefig("stretched" + str(sideOfSmallSquares.__round__(3)) + "AffineCrosswireResistanceToLevel" +
                str(precarpet_level) + ".pdf")
elif kindOfGraph == 'x':
    plt.title("Rho of the Stretched Level " + str(precarpet_level) + " " + str(sideOfSmallSquares) +
              "-Affine X Graph")
    plt.savefig("stretched" + str(sideOfSmallSquares) + "AffineXResistanceToLevel" + str(precarpet_level) + ".pdf")

plt.show()
