import matplotlib.pyplot as plt
import copy
import graphClass as gc
import numpy as np
from fractions import Fraction

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 2
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# what center holes would you like to calculate the resistance of
centerHoleCalculations = [1/4, 1/3, 1/2, 1/5]

# put list in decreasing order
centerHoleCalculations.sort(reverse=True)
# the above two are the only parameters, since sideOfCenterHole + 2*sideOfSmallSquares = 1 must be true
correspondingSmallSquares = [(1 - c)/2 for c in centerHoleCalculations]

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
aCn_plus_one = copy.deepcopy(aC0)
copyOfACn = gc.Graph()
# listOfContractionParameters[i][0] is the scaleX
# listOfContractionParameters[i][1] is scaleY
# listOfContractionParameters[i][2] is fixedPoint
listOfContractionParameters = [[correspondingSmallSquares, correspondingSmallSquares, np.array([0, 0])],  # q0
                               [centerHoleCalculations, correspondingSmallSquares, np.array([0.5, 0])],  # q1
                               [correspondingSmallSquares, correspondingSmallSquares, np.array([1, 0])],  # q2
                               [correspondingSmallSquares, centerHoleCalculations, np.array([1, 0.5])],  # q3
                               [correspondingSmallSquares, correspondingSmallSquares, np.array([1, 1])],  # q4
                               [centerHoleCalculations, correspondingSmallSquares, np.array([0.5, 1])],  # q5
                               [correspondingSmallSquares, correspondingSmallSquares, np.array([0, 1])],  # q6
                               [correspondingSmallSquares, centerHoleCalculations, np.array([0, 0.5])]]  # q7
# variables for plotting
countingList = []
listOfResistances = []

# making carpets and storing their resistances
for h in range(len(centerHoleCalculations)):
    aCn_plus_one = copy.deepcopy(aC0)
    countingList.append(correspondingSmallSquares[h])
    for k in range(precarpet_level):
        print("making level", k + 1)
        aCn = copy.deepcopy(aCn_plus_one)
        aCn_plus_one = gc.Graph()
        for i in range(0, 8):
            copyOfACn = copy.deepcopy(aCn)
            copyOfACn.update_all_vertices_names(str(i))
            copyOfACn.contract_graph_affine(listOfContractionParameters[i][0][h], listOfContractionParameters[i][1][h],
                                            listOfContractionParameters[i][2])
            aCn_plus_one.add_graph(copyOfACn)
        aCn_plus_one.remove_redundancies()
    aCn_plus_one.apply_harmonic_function_affine()
    listOfResistances.append(aCn_plus_one.resistance_of_graph())
    print("Finished with", correspondingSmallSquares[h])
print("done constructing")

# placing plot points
plt.plot(countingList, listOfResistances, "bo")
coefficients = np.polyfit(countingList, listOfResistances, 2)
linearization = np.poly1d(coefficients)
plt.plot(countingList, linearization(countingList), "r--")

# adding text to plot
plt.xlabel("Length of Small Squares' Sides")
plt.ylabel("Resistance of Graph")
plt.xticks([p.__round__(3) for p in countingList])
plt.yticks(list(range(0, precarpet_level + 3)))
for j in range(len(listOfResistances)):
    plt.text(countingList[j], listOfResistances[j] + .05, listOfResistances[j].__round__(3))

# saving and showing graph
titleStr = ""
for s in correspondingSmallSquares:
    titleStr = titleStr + str(Fraction(s).limit_denominator()) + ","
titleStr = titleStr.replace("/", "-")
if kindOfGraph == '+':
    plt.title("Resistances of Level " + str(precarpet_level) + " Affine Crosswire Graph \n of Various Proportions")
    plt.savefig(titleStr + "affineCrosswireResistancesOfLevel" + str(precarpet_level) + ".pdf")
elif kindOfGraph == 'x':
    plt.title("Resistances of Level " + str(precarpet_level) + " Affine X Graph \n of Various Proportions")
    plt.savefig(titleStr + "affineXResistancesOfLevel" + str(precarpet_level) + ".pdf")

plt.show()
