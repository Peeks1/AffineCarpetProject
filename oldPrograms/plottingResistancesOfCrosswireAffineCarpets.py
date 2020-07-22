import matplotlib.pyplot as plt
import copy
import graphClass as gc
import numpy as np
from fractions import Fraction

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 3
# how large would you like the center hole to be:
sideOfCenterHole = 1/3


# the above two are the only parameters, since sideOfCenterHole + 2*sideOfSmallSquares = 1 must be true
sideOfSmallSquares = (1 - sideOfCenterHole) / 2

# building the level 0 cross carpet
aC0 = gc.Graph()
aC0.add_vertex("a", np.array([0, 0.5]))
aC0.add_vertex("b", np.array([0.5, 1]))
aC0.add_vertex("c", np.array([1, 0.5]))
aC0.add_vertex("d", np.array([0.5, 0]))
aC0.add_vertex("e", np.array([0.5, 0.5]))
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

# making carpets and storing their resistances
for k in range(precarpet_level):
    print("making level", k + 1)
    countingList.append(k + 1)
    aCn = copy.deepcopy(aCn_plus_one)
    aCn_plus_one = gc.Graph()
    for i in range(0, 8):
        copyOfACn = copy.deepcopy(aCn)
        copyOfACn.update_all_vertices_names(str(i))
        copyOfACn.contract_graph_affine(listOfContractionParameters[i][0], listOfContractionParameters[i][1],
                                        listOfContractionParameters[i][2])
        aCn_plus_one.add_graph(copyOfACn)
    aCn_plus_one.remove_redundancies()
    aCn_plus_one.apply_harmonic_function_affine()
    listOfResistances.append(aCn_plus_one.resistance_of_graph())
print("done constructing")

# placing plot points
plt.plot(countingList, listOfResistances, "bo")
coefficients = np.polyfit(countingList, listOfResistances, 1)
linearization = np.poly1d(coefficients)
plt.plot(countingList, linearization(countingList), "r--")

# adding text to plot
plt.title("Resistances of the " + str(Fraction(sideOfSmallSquares)) + "-Affine Crosswire Graph")
plt.xlabel("Fractal Level")
plt.ylabel("Resistance of Graph")
plt.xticks(list(range(0, precarpet_level + 2)))
plt.yticks(list(range(0, precarpet_level + 3)))
for r in listOfResistances:
    plt.text(listOfResistances.index(r) + 1 - .1, r + .1, r.__round__(3))

# save and show plot
plt.savefig(str(sideOfSmallSquares) + "affineCrosswireResistanceToLevel" + str(precarpet_level) + ".pdf")
plt.show()

