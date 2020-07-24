import matplotlib.pyplot as plt
import os.path as p
import os

#  INPUT HERE
# what level affine carpet would you like rhos for:
precarpet_level = 5
# how large would you like the small squares to be:
sideOfSmallSquares = 1 / 4
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "+"
# what stretches would you like to compute
stretchFactors = [1, 1/2, 1/4, 1/8]

# other important variable calculated from above variables
sideOfCenterHole = 1 - sideOfSmallSquares * 2
stretchFactors.sort()

# file naming variables
kogString = ''
typeOfCarpet = str(sideOfSmallSquares.__round__(3)) + "affineCarpetStretchedRhoData"
level = 'level' + str(precarpet_level)
if kindOfGraph == '+':
    kogString = 'crossGraphData'
elif kindOfGraph == 'x':
    kogString = 'xGraphData'
else:
    exit()
saveFileAs = kogString + '/' + typeOfCarpet + '/' + level + '.pdf'
if not p.isdir(kogString + '/' + typeOfCarpet):
    os.makedirs(kogString + '/' + typeOfCarpet)

# get files ready for reading data
files = []  # this is a list of lists, where the two elements are the files containing the resistances needed for the
for i in stretchFactors:
    resistanceFolder = str(sideOfSmallSquares.__round__(3)) + 'affineCarpet1x' + str(i.__round__(3))
    level = 'level' + str(precarpet_level - 1)
    level2 = 'level' + str(precarpet_level)
    filePath = kogString + "/" + resistanceFolder + "/" + level + 'resistance.txt'
    filePath2 = kogString + "/" + resistanceFolder + "/" + level2 + 'resistance.txt'
    if not p.isfile(filePath):
        print('You need to calculate the resistance of the ' + level + ' ' + '1x' + str(i.__round__(3)) +
              ' carpet using resistanceSaver.py')
        exit()
    elif not p.isfile(filePath2):
        print('You need to calculate the resistance of the ' + level2 + ' ' + '1x' + str(i.__round__(3)) +
              ' carpet using resistanceSaver.py')
        exit()
    files.append([open(filePath, 'r'), open(filePath2, 'r')])

# calculate rho
rhos = []
for f in files:
    lowerResistanceFile = f[0]
    higherResistanceFile = f[1]
    lowerResistanceLines = lowerResistanceFile.readlines()
    lowerResistance = lowerResistanceLines[1]
    lowerResistance = float(lowerResistance[14:])
    higherResistanceLines = higherResistanceFile.readlines()
    higherResistance = higherResistanceLines[1]
    higherResistance = float(higherResistance[14:])
    rhos.append(higherResistance/lowerResistance)

# plot
plt.rcParams.update({'font.size': 15})
plt.scatter(stretchFactors, rhos)
plt.xticks(stretchFactors)
plt.yticks(range(0, 3))
plt.xlabel("Amount of Stretch")
plt.ylabel("Rho of Graph")
for j in range(len(rhos)):
    plt.text(stretchFactors[j], rhos[j] + .05, rhos[j].__round__(3))

# title
levelTitle = "Level " + str(precarpet_level) + " "
smallSquareStr = str(sideOfSmallSquares.__round__(3))
plt.title("Rho of " + levelTitle + smallSquareStr + "-Affine Cross Carpets")

# save
stretchesStr = ''
for stretch in stretchesStr:
    stretchesStr += str(stretch.__round__(2)) + ","

if p.isfile(saveFileAs):
    print('You already have rho data for this level. Press y if you would like to overwrite this data.')
    keypress = input()
    if keypress == 'y':
        plt.savefig(saveFileAs)
else:
    plt.savefig(saveFileAs)
plt.show()

