import numpy as np
import graphClass as gc
import copy
import os
import os.path as p
import time

#  INPUT HERE
# what level affine carpet would you like:
precarpet_level = 4
# how large would you like the small squares to be:
sideOfSmallSquares = 1/4
# how many runs
numRuns = 5000
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# how stretched would you like the carpet to be (this will be how far the 0 boundary will be from the 1 boundary
stretchFactor = 8

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

# get file ready for writing data
if precarpet_level < 1:
    exit()
filePath = kogString + "/" + typeOfCarpet + "/" + level + '.txt'
if p.isfile(filePath):
    print('You already have data for this carpet. Press y to confirm that you would like to overwrite this data.\n')
    keypress = input()
    if not keypress == 'y':
        exit()
if not p.isdir(kogString + '/' + typeOfCarpet):
    os.makedirs(kogString + '/' + typeOfCarpet)
file = open(filePath, "w+")

starttime = time.time()
# 2 cases: level 1 carpet or higher than level 1 carpet
# if level 1 carpet, use the old system of building the carpet and then applying relaxations
# if not, use data from the previous carpet (program will crash if it doesn't exist) to build a graph and apply
#   starting values
if precarpet_level == 1:
    # build the level 0 carpet
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
    # variables needed for the for loop that builds the precarpet to the desired level
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
    # carpet building loop
    for k in range(precarpet_level):
        aCn = copy.deepcopy(aCn_plus_one)
        aCn_plus_one = gc.Graph()
        for i in range(0, 8):
            copyOfACn = copy.deepcopy(aCn)
            copyOfACn.update_all_vertices_names(str(i))
            copyOfACn.contract_graph_affine(listOfContractionParameters[i][0], listOfContractionParameters[i][1],
                                            listOfContractionParameters[i][2])
            aCn_plus_one.add_graph(copyOfACn)
        aCn_plus_one.remove_redundancies()
    # applying harmonic function
    aCn_plus_one.apply_harmonic_function_affine(numRuns=numRuns)
    # writing file
    file.write(str(numRuns) + "runs\n")
    if kindOfGraph == '+':  # the cross graph data format
        for v in aCn_plus_one.vertices:
            if v[0] == 'e':
                # parameters are as follows: position, displacement, and harmonic values
                # position: where the center of the graph is
                # displacement: each center has 4 neighbors perpendicular to them, so the first value is top/bottom
                #   displacement and second is left/right
                # harmonic values: the harmonic values of the point above, below, left, and right neighbors of center
                savedParameters = [[None, None], [None, None], [None, None, None, None]]
                savedParameters[0][0] = str(aCn_plus_one.vertices[v][1][0])
                savedParameters[0][1] = str(aCn_plus_one.vertices[v][1][1])
                for n in aCn_plus_one.vertices[v][0]:
                    distance = aCn_plus_one.vertices[v][1] - aCn_plus_one.vertices[n][1]
                    if distance[0] == 0:  # must be top or bottom, as the x values were the same
                        if distance[1] < 0:  # must be top, as the neighbor has a higher y value
                            savedParameters[2][0] = str(aCn_plus_one.vertices[n][2])
                        elif distance[1] > 0:  # must be bottom, as the neighbor has a lower y value
                            savedParameters[1][0] = str(distance[1])
                            savedParameters[2][1] = str(aCn_plus_one.vertices[n][2])
                    elif distance[1] == 0:  # must be left or right, as the y values were the same
                        if distance[0] < 0:  # must be right, as the neighbor has a higher x value
                            savedParameters[2][3] = str(aCn_plus_one.vertices[n][2]) + '\n'
                        elif distance[0] > 0:  # must be left, as the neighbor has a lower x value
                            savedParameters[1][1] = str(distance[0])
                            savedParameters[2][2] = str(aCn_plus_one.vertices[n][2])
                listOfParameters = []
                seperator = '|'
                for parameter in savedParameters:
                    for e in parameter:
                        listOfParameters.append(e)
                file.write(seperator.join(listOfParameters))
    else:  # the x graph data format
        for v in aCn_plus_one.vertices:
            if v[0] == 'e':
                # parameters are as follows: position, displacement, and harmonic values
                # position: where the center of the graph is
                # displacement: how far each point is from the center (they're all the same displacement, just different
                #   signs in where; first number is horizontal, second is vertical
                # harmonic values: the harmonic values of the point top left, bottom left, bottom right, and top right
                #   neighbors of center
                savedParameters = [[None, None], [None, None], [None, None, None, None]]
                savedParameters[0][0] = str(aCn_plus_one.vertices[v][1][0])
                savedParameters[0][1] = str(aCn_plus_one.vertices[v][1][1])
                neigh = aCn_plus_one.vertices[v][0][0]  # doesn't matter which neighbor used
                distance = aCn_plus_one.vertices[v][1] - aCn_plus_one.vertices[neigh][1]
                savedParameters[1][0] = abs(distance[0])
                savedParameters[1][1] = abs(distance[1])
                for n in aCn_plus_one.vertices[v][0]:
                    disN = aCn_plus_one.vertices[n][1] - aCn_plus_one.vertices[v][1]
                    if disN[0] < 0:  # must be on left
                        if disN[1] > 0:  # must be top left
                            savedParameters[2][0] = aCn_plus_one.vertices[n][2]
                        else:  # bottom left
                            savedParameters[2][1] = aCn_plus_one.vertices[n][2]
                    else:  # must be on right
                        if disN[1] > 0:  # must be top right
                            savedParameters[2][3] = aCn_plus_one.vertices[n][2]
                        else:  # bottom right
                            savedParameters[2][2] = aCn_plus_one.vertices[n][2]
                listOfParameters = []
                seperator = '|'
                for parameter in savedParameters:
                    for e in parameter:
                        listOfParameters.append(str(e))
                listOfParameters[-1] = listOfParameters[-1] + '\n'
                file.write(seperator.join(listOfParameters))
else:
    # open data for carpet of lower level
    prevLevel = 'level' + str(precarpet_level - 1)
    prevFilePath = kogString + "/" + typeOfCarpet + "/" + prevLevel + '.txt'
    if not p.isfile(prevFilePath):
        print('You need to generate the carpet of the previous level first')
        exit()
    prevFile = open(prevFilePath, 'r')
    lowerCarpetData = prevFile.readlines()
    del lowerCarpetData[0]
    # iterate through the data and build the graph with correct harmonic functions
    aCn_plus_one = gc.Graph()
    i = 0
    if kindOfGraph == '+':
        for line in lowerCarpetData:
            # create graph and list of data
            aCn = gc.Graph()
            parameters = list(line.split("|"))
            parameters = [float(j) for j in parameters]
            # data from line
            centerPosition = np.array(parameters[0:2])
            vertDisplacement = parameters[2]
            horizontalDisplacement = parameters[3]
            topHarmonic = parameters[4]
            bottHarmonic = parameters[5]
            leftHarmonic = parameters[6]
            rightHarmonic = parameters[7]
            avgHarmonic = sum(parameters[4:]) / 4
            # convert to data for making graph
            # each point is in a certain vertical (v) and horizontal (h) file
            v1 = centerPosition[0] - (sideOfCenterHole + 2 * sideOfSmallSquares) * horizontalDisplacement
            v2 = centerPosition[0] - (sideOfCenterHole + sideOfSmallSquares) * horizontalDisplacement
            v3 = centerPosition[0] - sideOfCenterHole * horizontalDisplacement
            v4 = centerPosition[0]
            v5 = centerPosition[0] + sideOfCenterHole * horizontalDisplacement
            v6 = centerPosition[0] + (sideOfCenterHole + sideOfSmallSquares) * horizontalDisplacement
            v7 = centerPosition[0] + (sideOfCenterHole + 2 * sideOfSmallSquares) * horizontalDisplacement
            h1 = centerPosition[1] - (sideOfCenterHole + 2 * sideOfSmallSquares) * vertDisplacement
            h2 = centerPosition[1] - (sideOfCenterHole + sideOfSmallSquares) * vertDisplacement
            h3 = centerPosition[1] - sideOfCenterHole * vertDisplacement
            h4 = centerPosition[1]
            h5 = centerPosition[1] + sideOfCenterHole * vertDisplacement
            h6 = centerPosition[1] + (sideOfCenterHole + sideOfSmallSquares) * vertDisplacement
            h7 = centerPosition[1] + (sideOfCenterHole + 2 * sideOfSmallSquares) * vertDisplacement
            # building the graph; points are named from left to right, top to bottom
            p1 = 'a' + str(i)
            p2 = 'b' + str(i)
            p3 = 'c' + str(i)
            p4 = 'd' + str(i)
            p5 = 'e' + str(i)
            p6 = 'f' + str(i)
            p7 = 'g' + str(i)
            p8 = 'h' + str(i)
            p9 = 'i' + str(i)
            p10 = 'j' + str(i)
            p11 = 'k' + str(i)
            p12 = 'l' + str(i)
            p13 = 'm' + str(i)
            p14 = 'n' + str(i)
            p15 = 'o' + str(i)
            p16 = 'p' + str(i)
            p17 = 'q' + str(i)
            p18 = 'r' + str(i)
            p19 = 's' + str(i)
            p20 = 't' + str(i)
            p21 = 'u' + str(i)
            p22 = 'v' + str(i)
            p23 = 'w' + str(i)
            p24 = 'x' + str(i)
            p25 = 'y' + str(i)
            p26 = 'z' + str(i)
            p27 = 'A' + str(i)
            p28 = 'B' + str(i)
            p29 = 'C' + str(i)
            p30 = 'D' + str(i)
            p31 = 'E' + str(i)
            p32 = 'F' + str(i)
            aCn.add_vertex(p1, np.array([v2, h7]))
            aCn.add_vertex(p2, np.array([v4, h7]))
            aCn.add_vertex(p3, np.array([v6, h7]))
            aCn.add_vertex(p4, np.array([v1, h6]))
            aCn.add_vertex(p5, np.array([v2, h6]))
            aCn.add_vertex(p6, np.array([v3, h6]))
            aCn.add_vertex(p7, np.array([v4, h6]))
            aCn.add_vertex(p8, np.array([v5, h6]))
            aCn.add_vertex(p9, np.array([v6, h6]))
            aCn.add_vertex(p10, np.array([v7, h6]))
            aCn.add_vertex(p11, np.array([v2, h5]))
            aCn.add_vertex(p12, np.array([v4, h5]))
            aCn.add_vertex(p13, np.array([v6, h5]))
            aCn.add_vertex(p14, np.array([v1, h4]))
            aCn.add_vertex(p15, np.array([v2, h4]))
            aCn.add_vertex(p16, np.array([v3, h4]))
            aCn.add_vertex(p17, np.array([v5, h4]))
            aCn.add_vertex(p18, np.array([v6, h4]))
            aCn.add_vertex(p19, np.array([v7, h4]))
            aCn.add_vertex(p20, np.array([v2, h3]))
            aCn.add_vertex(p21, np.array([v4, h3]))
            aCn.add_vertex(p22, np.array([v6, h3]))
            aCn.add_vertex(p23, np.array([v1, h2]))
            aCn.add_vertex(p24, np.array([v2, h2]))
            aCn.add_vertex(p25, np.array([v3, h2]))
            aCn.add_vertex(p26, np.array([v4, h2]))
            aCn.add_vertex(p27, np.array([v5, h2]))
            aCn.add_vertex(p28, np.array([v6, h2]))
            aCn.add_vertex(p29, np.array([v7, h2]))
            aCn.add_vertex(p30, np.array([v2, h1]))
            aCn.add_vertex(p31, np.array([v4, h1]))
            aCn.add_vertex(p32, np.array([v6, h1]))
            aCn.add_edge(p1, p5)
            aCn.add_edge(p2, p7)
            aCn.add_edge(p3, p9)
            aCn.add_edge(p4, p5)
            aCn.add_edge(p5, p6)
            aCn.add_edge(p5, p11)
            aCn.add_edge(p6, p7)
            aCn.add_edge(p7, p8)
            aCn.add_edge(p7, p12)
            aCn.add_edge(p8, p9)
            aCn.add_edge(p9, p10)
            aCn.add_edge(p9, p13)
            aCn.add_edge(p11, p15)
            aCn.add_edge(p13, p18)
            aCn.add_edge(p14, p15)
            aCn.add_edge(p15, p16)
            aCn.add_edge(p17, p18)
            aCn.add_edge(p18, p19)
            aCn.add_edge(p15, p20)
            aCn.add_edge(p18, p22)
            aCn.add_edge(p20, p24)
            aCn.add_edge(p22, p28)
            aCn.add_edge(p23, p24)
            aCn.add_edge(p24, p25)
            aCn.add_edge(p24, p30)
            aCn.add_edge(p25, p26)
            aCn.add_edge(p21, p26)
            aCn.add_edge(p26, p31)
            aCn.add_edge(p26, p27)
            aCn.add_edge(p27, p28)
            aCn.add_edge(p28, p29)
            aCn.add_edge(p28, p32)
            # applying harmonic
            # this part could be hard coded if it causes performance issues
            for v in aCn.vertices:
                xpos = aCn.vertices[v][1][0]
                ypos = aCn.vertices[v][1][1]
                if ypos == h7:
                    aCn.vertices[v][2] = topHarmonic
                elif ypos == h1:
                    aCn.vertices[v][2] = bottHarmonic
                elif xpos == v1:
                    aCn.vertices[v][2] = leftHarmonic
                elif xpos == v7:
                    aCn.vertices[v][2] = rightHarmonic
                else:
                    aCn.vertices[v][2] = avgHarmonic
            # add created graph to the final graph
            aCn_plus_one.add_graph(aCn)
            i += 1
        # remove redundancies and apply harmonic
        aCn_plus_one.remove_redundancies()
        aCn_plus_one.apply_harmonic_function_affine(numRuns=numRuns, setInitialValues=False)
        file.write(str(numRuns) + "runs\n")
        for v in aCn_plus_one.vertices:
            if len(aCn_plus_one.vertices[v][0]) == 4:
                # parameters are as follows: position, displacement, and harmonic values
                # position: where the center of the graph is
                # displacement: each center has 4 neighbors perpendicular to them, so the first value is top/bottom
                #   displacement and second is left/right
                # harmonic values: the harmonic values of the point above, below, left, and right neighbors of center
                savedParameters = [[None, None], [None, None], [None, None, None, None]]
                savedParameters[0][0] = str(aCn_plus_one.vertices[v][1][0])
                savedParameters[0][1] = str(aCn_plus_one.vertices[v][1][1])
                for n in aCn_plus_one.vertices[v][0]:
                    distance = aCn_plus_one.vertices[v][1] - aCn_plus_one.vertices[n][1]
                    if np.isclose(distance[0], 0.0):
                        distance[0] = 0.0
                    if np.isclose(distance[1], 0.0):
                        distance[1] = 0.0
                    if distance[0] == 0:  # must be top or bottom, as the x values were the same
                        if distance[1] < 0:  # must be top, as the neighbor has a higher y value
                            savedParameters[2][0] = str(aCn_plus_one.vertices[n][2])
                        elif distance[1] > 0:  # must be bottom, as the neighbor has a lower y value
                            savedParameters[1][0] = str(distance[1])
                            savedParameters[2][1] = str(aCn_plus_one.vertices[n][2])
                    elif distance[1] == 0:  # must be left or right, as the y values were the same
                        if distance[0] < 0:  # must be right, as the neighbor has a higher x value
                            savedParameters[2][3] = str(aCn_plus_one.vertices[n][2]) + '\n'
                        elif distance[0] > 0:  # must be left, as the neighbor has a lower x value
                            savedParameters[1][1] = str(distance[0])
                            savedParameters[2][2] = str(aCn_plus_one.vertices[n][2])
                listOfParameters = []
                seperator = '|'
                for parameter in savedParameters:
                    for e in parameter:
                        listOfParameters.append(e)
                file.write(seperator.join(listOfParameters))
    else:  # code for x graph
        for line in lowerCarpetData:
            # create graph and list of data
            aCn = gc.Graph()
            parameters = list(line.split("|"))
            parameters = [float(j) for j in parameters]
            # data from line
            centerPosition = np.array(parameters[0:2])
            vertDisplacement = parameters[3]
            horizontalDisplacement = parameters[2]
            tlHarmonic = parameters[4]
            blHarmonic = parameters[5]
            brHarmonic = parameters[6]
            trHarmonic = parameters[7]
            avgHarmonic = sum(parameters[4:]) / 4
            tHarmonic = (tlHarmonic + trHarmonic)/2
            bHarmonic = (blHarmonic + brHarmonic)/2
            rHarmonic = (trHarmonic + brHarmonic)/2
            lHarmonic = (tlHarmonic + blHarmonic)/2
            # convert to data for making graph
            # each point is in a certain vertical (v) and horizontal (h) file
            v1 = centerPosition[0] - (sideOfCenterHole + 2 * sideOfSmallSquares) * horizontalDisplacement
            v2 = centerPosition[0] - (sideOfCenterHole + sideOfSmallSquares) * horizontalDisplacement
            v3 = centerPosition[0] - sideOfCenterHole * horizontalDisplacement
            v4 = centerPosition[0]
            v5 = centerPosition[0] + sideOfCenterHole * horizontalDisplacement
            v6 = centerPosition[0] + (sideOfCenterHole + sideOfSmallSquares) * horizontalDisplacement
            v7 = centerPosition[0] + (sideOfCenterHole + 2 * sideOfSmallSquares) * horizontalDisplacement
            h1 = centerPosition[1] - (sideOfCenterHole + 2 * sideOfSmallSquares) * vertDisplacement
            h2 = centerPosition[1] - (sideOfCenterHole + sideOfSmallSquares) * vertDisplacement
            h3 = centerPosition[1] - sideOfCenterHole * vertDisplacement
            h4 = centerPosition[1]
            h5 = centerPosition[1] + sideOfCenterHole * vertDisplacement
            h6 = centerPosition[1] + (sideOfCenterHole + sideOfSmallSquares) * vertDisplacement
            h7 = centerPosition[1] + (sideOfCenterHole + 2 * sideOfSmallSquares) * vertDisplacement
            # building the graph
            a = 'a' + str(i)
            b = 'b' + str(i)
            c = 'c' + str(i)
            d = 'd' + str(i)
            e = 'ec' + str(i)
            f = 'fc' + str(i)
            g = 'gc' + str(i)
            h = 'h' + str(i)
            ii = 'i' + str(i)
            j = 'j' + str(i)
            k = 'k' + str(i)
            l = 'lc' + str(i)
            m = 'mc' + str(i)
            n = 'n' + str(i)
            o = 'o' + str(i)
            p = 'p' + str(i)
            q = 'q' + str(i)
            r = 'rc' + str(i)
            s = 'sc' + str(i)
            t = 'tc' + str(i)
            u = 'u' + str(i)
            v = 'v' + str(i)
            w = 'w' + str(i)
            x = 'x' + str(i)
            aCn.add_vertex(a, np.array([v1, h7]))
            aCn.add_vertex(b, np.array([v3, h7]))
            aCn.add_vertex(c, np.array([v5, h7]))
            aCn.add_vertex(d, np.array([v7, h7]))
            aCn.add_vertex(e, np.array([v2, h6]))
            aCn.add_vertex(f, np.array([v4, h6]))
            aCn.add_vertex(g, np.array([v6, h6]))
            aCn.add_vertex(h, np.array([v1, h5]))
            aCn.add_vertex(ii, np.array([v3, h5]))
            aCn.add_vertex(j, np.array([v5, h5]))
            aCn.add_vertex(k, np.array([v7, h5]))
            aCn.add_vertex(l, np.array([v2, h4]))
            aCn.add_vertex(m, np.array([v6, h4]))
            aCn.add_vertex(n, np.array([v1, h3]))
            aCn.add_vertex(o, np.array([v3, h3]))
            aCn.add_vertex(p, np.array([v5, h3]))
            aCn.add_vertex(q, np.array([v7, h3]))
            aCn.add_vertex(r, np.array([v2, h2]))
            aCn.add_vertex(s, np.array([v4, h2]))
            aCn.add_vertex(t, np.array([v6, h2]))
            aCn.add_vertex(u, np.array([v1, h1]))
            aCn.add_vertex(v, np.array([v3, h1]))
            aCn.add_vertex(w, np.array([v5, h1]))
            aCn.add_vertex(x, np.array([v7, h1]))
            aCn.add_edge(a, e)
            aCn.add_edge(b, e)
            aCn.add_edge(h, e)
            aCn.add_edge(ii, e)
            aCn.add_edge(b, f)
            aCn.add_edge(c, f)
            aCn.add_edge(ii, f)
            aCn.add_edge(j, f)
            aCn.add_edge(c, g)
            aCn.add_edge(d, g)
            aCn.add_edge(j, g)
            aCn.add_edge(k, g)
            aCn.add_edge(h, l)
            aCn.add_edge(ii, l)
            aCn.add_edge(n, l)
            aCn.add_edge(o, l)
            aCn.add_edge(j, m)
            aCn.add_edge(k, m)
            aCn.add_edge(p, m)
            aCn.add_edge(q, m)
            aCn.add_edge(n, r)
            aCn.add_edge(o, r)
            aCn.add_edge(u, r)
            aCn.add_edge(v, r)
            aCn.add_edge(o, s)
            aCn.add_edge(v, s)
            aCn.add_edge(p, s)
            aCn.add_edge(w, s)
            aCn.add_edge(p, t)
            aCn.add_edge(w, t)
            aCn.add_edge(q, t)
            aCn.add_edge(x, t)
            # applying harmonic
            # this part could be hard coded if it causes performance issues
            for v in aCn.vertices:
                xpos = aCn.vertices[v][1][0]
                ypos = aCn.vertices[v][1][1]
                if ypos == h7:
                    if xpos == v1:
                        aCn.vertices[v][2] = tlHarmonic
                    elif xpos == v7:
                        aCn.vertices[v][2] = trHarmonic
                    else:
                        aCn.vertices[v][2] = tHarmonic
                elif ypos == h1:
                    if xpos == v1:
                        aCn.vertices[v][2] = blHarmonic
                    elif xpos == v7:
                        aCn.vertices[v][2] = brHarmonic
                    else:
                        aCn.vertices[v][2] = bHarmonic
                elif xpos == v1:
                    aCn.vertices[v][2] = lHarmonic
                elif xpos == v7:
                    aCn.vertices[v][2] = rHarmonic
                else:
                    aCn.vertices[v][2] = avgHarmonic
            # add created graph to the final graph
            aCn_plus_one.add_graph(aCn)
            i += 1
        # remove redundancies and apply harmonic
        aCn_plus_one.remove_redundancies()
        aCn_plus_one.apply_harmonic_function_affine(numRuns=numRuns, setInitialValues=False)
        file.write(str(numRuns) + "runs\n")
        for v in aCn_plus_one.vertices:
            if v[1] == 'c':
                # parameters are as follows: position, displacement, and harmonic values
                # position: where the center of the graph is
                # displacement: how far each point is from the center (they're all the same displacement, just different
                #   signs in where; first number is horizontal, second is vertical
                # harmonic values: the harmonic values of the point top left, bottom left, bottom right, and top right
                #   neighbors of center
                savedParameters = [[None, None], [None, None], [None, None, None, None]]
                savedParameters[0][0] = str(aCn_plus_one.vertices[v][1][0])
                savedParameters[0][1] = str(aCn_plus_one.vertices[v][1][1])
                neigh = aCn_plus_one.vertices[v][0][0]  # doesn't matter which neighbor used
                distance = aCn_plus_one.vertices[v][1] - aCn_plus_one.vertices[neigh][1]
                savedParameters[1][0] = abs(distance[0])
                savedParameters[1][1] = abs(distance[1])
                for n in aCn_plus_one.vertices[v][0]:
                    disN = aCn_plus_one.vertices[n][1] - aCn_plus_one.vertices[v][1]
                    if np.isclose(disN[0], 0.0):
                        disN[0] = 0.0
                    if np.isclose(disN[1], 0.0):
                        disN[1] = 0.0
                    if disN[0] < 0:  # must be on left
                        if disN[1] > 0:  # must be top left
                            savedParameters[2][0] = aCn_plus_one.vertices[n][2]
                        else:  # bottom left
                            savedParameters[2][1] = aCn_plus_one.vertices[n][2]
                    else:  # must be on right
                        if disN[1] > 0:  # must be top right
                            savedParameters[2][3] = aCn_plus_one.vertices[n][2]
                        else:  # bottom right
                            savedParameters[2][2] = aCn_plus_one.vertices[n][2]
                listOfParameters = []
                seperator = '|'
                for parameter in savedParameters:
                    for e in parameter:
                        listOfParameters.append(str(e))
                listOfParameters[-1] = listOfParameters[-1] + '\n'
                file.write(seperator.join(listOfParameters))

print("Program took ", time.time() - starttime)