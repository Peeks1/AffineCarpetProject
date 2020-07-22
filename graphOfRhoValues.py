import matplotlib.pyplot as plt
import os.path as p

#  INPUT HERE
# what level affine carpets would you like rhos for:
precarpet_levels = [1, 2, 3, 4]
# how large would you like the small squares to be:
sideOfSmallSquares = 1/3
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# how stretched would you like the carpet to be (this will be how far the 0 boundary will be from the 1 boundary
stretchFactor = 1

# other important variable calculated from above variables
sideOfCenterHole = 1 - sideOfSmallSquares * 2
precarpet_levels.sort()

# file naming variables
kogString = ''
typeOfCarpet = str(sideOfSmallSquares.__round__(3)) + "affineCarpet1x" + str(stretchFactor.__round__(3))
if kindOfGraph == '+':
    kogString = 'crossGraphData'
elif kindOfGraph == 'x':
    kogString = 'xGraphData'
else:
    exit()

# get files ready for reading data
files = []  # this is a list of lists, where the first element is the file and the second is the level of the carpet
for i in precarpet_levels:
    level = 'level' + str(i - 1)
    level2 = 'level' + str(i)
    if not level[-1] == '0':
        filePath = kogString + "/" + typeOfCarpet + "/" + level + 'resistance.txt'
        filePath2 = kogString + "/" + typeOfCarpet + "/" + level2 + 'resistance.txt'
        if not p.isfile(filePath):
            print('You need to calculate the resistance of the ' + level + 'carpet using resistanceSaver.py')
            exit()
        elif not p.isfile(filePath2):
            print('You need to calculate the resistance of the ' + level2 + 'carpet using resistanceSaver.py')
            exit()
        if not open(filePath, "r") in files:
            files.append([open(filePath, "r"), i - 1])
        if not open(filePath2, 'r') in files:
            files.append([open(filePath2, 'r'), i])
    else:
        files.append([stretchFactor * 2, 0])

# get resistances from data
resistances = []
for file in files:
    if not file[1] == 0:
        data = file[0].readlines()
        resistance = data[1]
        resistance = float(resistance[14:])
        resistances.append([resistance, file[1]])
    else:
        resistances.append(file)

# calculate rho
rhos = []
for i in precarpet_levels:
    lowerResistance = 0
    higherResistance = 0
    for r in resistances:
        if r[1] == i:
            higherResistance = r
        elif r[1] == i - 1:
            lowerResistance = r[0]
    rhos.append([higherResistance[0]/lowerResistance, higherResistance[1]])

# plot
plt.plot(precarpet_levels, [f[0] for f in rhos], "bo")
plt.xticks(range(0, precarpet_levels[-1] + 1))
plt.yticks(range(0, 3))
plt.xlabel("Precarpet Level")
plt.ylabel("Rho of Graph")
for j in rhos:
    plt.text(j[1], j[0] + .05, j[0].__round__(3))

# title
stretchStr = str(stretchFactor.__round__(5))
smallSquareStr = str(sideOfSmallSquares.__round__(3))
plt.title("Rho of the 1x" + stretchStr + " " + smallSquareStr + "-Affine Carpet")

saveFileAs = kogString + "/" + typeOfCarpet + "/" + "rhoValues.pdf"
if p.isfile(saveFileAs):
    print('You already have rho data. Press y if you would like to overwrite this data.')
    keypress = input()
    if keypress == 'y':
        plt.savefig(saveFileAs)
else:
    plt.savefig(saveFileAs)
plt.show()
