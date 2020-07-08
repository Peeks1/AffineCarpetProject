import numpy as np
import graphClasses as gc
import copy

#  INPUT HERE what level precarpet would you like?
precarpet_level = 2

# building the level 0 cross carpet
sC0 = gc.Graph()
sC0.add_vertex("a", np.array([0, 0.5]))
sC0.add_vertex("b", np.array([0.5, 1]))
sC0.add_vertex("c", np.array([1, 0.5]))
sC0.add_vertex("d", np.array([0.5, 0]))
sC0.add_vertex("e", np.array([0.5, 0.5]))
sC0.add_edge("a", "e")
sC0.add_edge('b', 'e')
sC0.add_edge('c', 'e')
sC0.add_edge('d', 'e')

sCn = gc.Graph()
sCn_plus_one = sC0
copyOfSCn = gc.Graph()
scalingFactor = 1 / 3  # how much longer each graph connection is compared to its n+1 carpet counterpart
listOfFixedPoints = [np.array([0, 0]),  # q0
                     np.array([0.5, 0]),  # q1
                     np.array([1, 0]),  # q2
                     np.array([1, 0.5]),  # q3
                     np.array([1, 1]),  # q4
                     np.array([0.5, 1]),  # q5
                     np.array([0, 1]),  # q6
                     np.array([0, 0.5])]  # q7

for k in range(precarpet_level):
    print("making level", k + 1)
    sCn = copy.deepcopy(sCn_plus_one)
    sCn_plus_one = gc.Graph()
    for i in range(0, 8):
        copyOfSCn = copy.deepcopy(sCn)
        copyOfSCn.update_all_vertices_names(str(i))
        copyOfSCn.contract_graph(scalingFactor, listOfFixedPoints[i])
        sCn_plus_one.add_graph(copyOfSCn)
    sCn_plus_one.remove_redundancies()

print("done constructing")
sCn_plus_one.apply_harmonic_function()
# sCn_plus_one.print_graph()
# sCn_plus_one.print_vertices_x_y_f()
print("Resistance of the graph is", sCn_plus_one.resistance_of_graph())
