import matplotlib.pyplot as plt
import copy
import graphClass as gc
import numpy as np
from fractions import Fraction

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 2
# how large would you like the center hole to be:
sideOfCenterHole = 1/2

# the above two are the only parameters, since sideOfCenterHole + 2*sideOfSmallSquares = 1 must be true
sideOfSmallSquares = (1 - sideOfCenterHole) / 2

# CODE FOR THE CROSSWIRE
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
listOfCrossResistances = []

# making crosswire carpets and storing their resistances
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
    listOfCrossResistances.append(aCn_plus_one.resistance_of_graph())
print("done constructing crosswire")

# CODE FOR THE X CARPET
# building the level 0 X carpet
aX0 = gc.Graph()
aX0.add_vertex("a", np.array([0, 0]))
aX0.add_vertex("b", np.array([0, 1]))
aX0.add_vertex("c", np.array([1, 1]))
aX0.add_vertex("d", np.array([1, 0]))
aX0.add_vertex("e", np.array([0.5, 0.5]))
aX0.add_edge("a", "e")
aX0.add_edge('b', 'e')
aX0.add_edge('c', 'e')
aX0.add_edge('d', 'e')

# variables needed for the for loop that builds the precarpet
aXn = gc.Graph()
aXn_plus_one = aX0
copyOfAXn = gc.Graph()

# storing resistance of X
listOfXResistances = []

# making carpets and storing their resistances
for k in range(precarpet_level):
    print("making level", k + 1)
    aXn = copy.deepcopy(aXn_plus_one)
    aXn_plus_one = gc.Graph()
    for i in range(0, 8):
        copyOfAXn = copy.deepcopy(aXn)
        copyOfAXn.update_all_vertices_names(str(i))
        copyOfAXn.contract_graph_affine(listOfContractionParameters[i][0], listOfContractionParameters[i][1],
                                        listOfContractionParameters[i][2])
        aXn_plus_one.add_graph(copyOfAXn)
    aXn_plus_one.remove_redundancies()
    aXn_plus_one.apply_harmonic_function_affine()
    listOfXResistances.append(aXn_plus_one.resistance_of_graph())
aXn_plus_one.print_vertices_x_y_f()
print("done constructing X")

# placing plot points for cross
crossLegend, = plt.plot(countingList, listOfCrossResistances, "bo", label='Crosswire Graph Resistance')
coefficientsCross = np.polyfit(countingList, listOfCrossResistances, 1)
linearizationCross = np.poly1d(coefficientsCross)
plt.plot(countingList, linearizationCross(countingList), "b--")

# placing plot points for X
xLegend, = plt.plot(countingList, listOfXResistances, "ro", label='X Graph Resistance')
coefficientsX = np.polyfit(countingList, listOfXResistances, 1)
linearizationX = np.poly1d(coefficientsX)
plt.plot(countingList, linearizationX(countingList), "r--")

# adding text to plot
plt.title("Resistances of the " + str(Fraction(sideOfSmallSquares)) + "-Affine Crosswire and X Graphs")
plt.xlabel("Fractal Level")
plt.ylabel("Resistance of Graph")
plt.xticks(list(range(0, precarpet_level + 2)))
plt.yticks(list(range(0, precarpet_level + 3)))
plt.legend(handles=[crossLegend, xLegend])
for r in listOfCrossResistances:
    plt.text(listOfCrossResistances.index(r) + 1 - .1, r + .1, r.__round__(3))
for r in listOfXResistances:
    plt.text(listOfXResistances.index(r) + 1 - .1, r + .1, r.__round__(3))

# save and show plot
plt.savefig(str(sideOfSmallSquares) + "affineXAndCrosswireResistanceToLevel" + str(precarpet_level) + ".pdf")
plt.show()

