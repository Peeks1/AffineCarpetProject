import numpy as np
import copy
import time


class Graph:
    # an object that is simply a dictionary of vertices
    # the key is the name of the vertex and refers to a list
    # index 0 is a list of strings referring to the keys of the vertex's neighbors
    # index 1 is a numpy array of 2 values referring to the x and y coordinates of the vertex, respectively
    # index 2 is the harmonicValue of the point
    def __init__(self):
        self.vertices = {}

    def __deepcopy__(self, memodict={}):
        theCopy = Graph()
        for v in self.vertices:
            theCopy.vertices[v] = copy.deepcopy(self.vertices[v])
        return theCopy

    def add_vertex(self, name, xyCoordinates):
        # allows you to add vertices to a graph
        # adds a new key to the vertices dictionary that refers to the list corresponding to the vertex
        # the key is the string input for name, the position input should be a list and is transformed into an np.array
        # and 0 is put as a placeholder harmonic value
        self.vertices[name] = [[], np.array(xyCoordinates), 0]

    def add_edge(self, u, v):
        # allows you to add edges to vertices in a graph
        # input is 2 strings, function makes sure the strings are both keys in the vertices dictionary and then adds
        #   each string to each other's neighbor lists
        if u in self.vertices and v in self.vertices:
            self.vertices[v][0].append(u)
            self.vertices[u][0].append(v)

    def contract_graph(self, scale, fixedPoint):
        # contracts a graph by a scale towards a fixed point
        # since position and fixedPoint are numpy arrays, the formula written works
        for v in self.vertices:
            self.vertices[v][1] = scale * (self.vertices[v][1] - fixedPoint) + fixedPoint

    def contract_graph_affine(self, scaleX, scaleY, fixedPoint):
        scaleMatrix = np.array([scaleX, scaleY])
        for v in self.vertices:
            self.vertices[v][1] = np.multiply((self.vertices[v][1] - fixedPoint), scaleMatrix) + fixedPoint

    def update_all_vertices_names(self, update):
        self.vertices = {key + update: value for key, value in self.vertices.items()}
        for v in self.vertices:
            self.vertices[v][0] = [n + update for n in self.vertices[v][0]]

    def add_graph(self, gr):
        # copies all the Vertex objects from a graph to another graph
        grCopy = copy.deepcopy(gr)
        self.vertices.update(grCopy.vertices)

    def combine_vertices(self, listOfVerts):
        listOfVerts.sort()
        keptPoint = listOfVerts[0]
        listOfVerts.remove(listOfVerts[0])
        for v in listOfVerts:
            self.vertices[keptPoint][0].extend(self.vertices[v][0])
            for n in self.vertices[v][0]:
                self.vertices[n][0].remove(v)
                self.vertices[n][0].append(keptPoint)
            self.vertices.pop(v)

    def remove_redundancies(self):
        # combines any points with the same position
        dictOfPositions = {}
        dictOfDuplicatePositions = {}
        for v in self.vertices:
            posV = tuple(np.round(self.vertices[v][1], 10))
            if posV in dictOfPositions:
                if posV in dictOfDuplicatePositions:
                    dictOfDuplicatePositions[posV].append(v)
                else:
                    dictOfDuplicatePositions[posV] = [dictOfPositions[posV], v]
            else:
                dictOfPositions[posV] = v
        for key in dictOfDuplicatePositions:
            self.combine_vertices(dictOfDuplicatePositions[key])

    def apply_harmonic_function_affine(self, stretchFactor=1, numRuns=2000, setInitialValues=True, updateFrequency=50):
        starttime = time.time()
        vWithMoreThanOneN = set()
        vWithOneN = set()
        if setInitialValues:
            for v in self.vertices:
                self.vertices[v][2] = self.vertices[v][1][0]/stretchFactor  # starts with the function f(x, y)=x/stretch
                if not (self.vertices[v][2] == 0 or self.vertices[v][2] == 1):  # keeps from looping through boundary
                    if not len(self.vertices[v][0]) == 1:
                        vWithMoreThanOneN.add(v)
                    else:
                        vWithOneN.add(v)
        else:
            for v in self.vertices:
                if not (self.vertices[v][2] == 0 or self.vertices[v][2] == 1):  # keeps from looping through boundary
                    if not len(self.vertices[v][0]) == 1:
                        vWithMoreThanOneN.add(v)
                    else:
                        vWithOneN.add(v)
        for i in range(numRuns):
            if i % updateFrequency == 0:
                print("On relaxation", i, "Been applying harmonic for", time.time() - starttime)
            for u in vWithMoreThanOneN:
                sumOfWeights = 0
                sumOfWeightedHarmonicValues = 0
                for n in self.vertices[u][0]:
                    if n in vWithOneN:
                        self.vertices[n][2] = self.vertices[u][2]
                    distanceToNeighbor = np.linalg.norm(self.vertices[u][1] - self.vertices[n][1])
                    sumOfWeights += 1 / distanceToNeighbor
                    sumOfWeightedHarmonicValues += self.vertices[n][2] / distanceToNeighbor
                self.vertices[u][2] = sumOfWeightedHarmonicValues / sumOfWeights
        print("Applying harmonic took", time.time() - starttime)

    def resistance_of_graph(self):
        totalOfSquaredDifferences = 0
        for v in self.vertices:
            for n in self.vertices[v][0]:
                distance = np.linalg.norm(self.vertices[v][1] - self.vertices[n][1])
                totalOfSquaredDifferences += ((self.vertices[v][2] - self.vertices[n][2]) ** 2) / distance
        return 1 / (totalOfSquaredDifferences / 2)

    def print_graph(self):
        for v in self.vertices:
            print(v, "has neighbors:")
            for n in self.vertices[v][0]:
                print(n)
            print("and is in position:")
            print(self.vertices[v][1])
            print("and has a harmonic function value of:")
            print(self.vertices[v][2])
            print()

    def print_vertices_x_y_f(self):
        for v in self.vertices:
            print(v, self.vertices[v][1], self.vertices[v][2])


# test code
'''
g = Graph()
g.add_vertex("a", [0, 0])
g.add_vertex("b", [1, 0])
g.add_vertex("c", [1, 1])
g.add_vertex("d", [1, 0])
g.add_edge("a", "b")
g.add_edge("c", "d")
g.contract_graph(1/2, [.5, .5])
g.remove_redundancies()
g.print_graph()
g.print_vertices_x_y_f()'''
