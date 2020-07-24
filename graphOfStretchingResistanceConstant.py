import matplotlib.pyplot as plt
import os.path as p
import os

#  INPUT HERE
# what level affine carpet would you like rhos for:
precarpet_level = 6
# how large would you like the small squares to be:
sideOfSmallSquares = 1 / 4
# would you like a cross or X-graph (input "+" or "x"):
kindOfGraph = "x"
# what stretches would you like to compute
stretchFactors = [1/8, 1/4, 1/2, 1, 2, 4, 8]

# other important variable calculated from above variables
sideOfCenterHole = 1 - sideOfSmallSquares * 2
stretchFactors.sort()

# file naming variables
kogString = ''
typeOfCarpet = str(sideOfSmallSquares.__round__(3)) + "affineCarpetSRRatioData"
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

# extract base resistance
baseFolder = str(sideOfSmallSquares.__round__(3)) + 'affineCarpet1x' + str(1)
prevLevel = 'level' + str(precarpet_level - 1)
prevFile = kogString + "/" + baseFolder + "/" + prevLevel + 'resistance.txt'
# for some reason the below code just doesn't work
'''if not p.isdir(prevFile):
    print('You need to calculate the resistance of the ' + prevLevel + ' ' + '1x1 carpet using resistanceSaver.py')
    exit()'''
baseFile = open(prevFile, 'r')
baseFileData = baseFile.readlines()
baseResistance = float(baseFileData[1][14:])

# list of the S values (stretched resistance of n)
stretechedResistances = []
for i in stretchFactors:
    resistanceFolder = str(sideOfSmallSquares.__round__(3)) + 'affineCarpet1x' + str(i.__round__(3))
    level = 'level' + str(precarpet_level)
    filePath = kogString + "/" + resistanceFolder + "/" + level + 'resistance.txt'
    if not p.isfile(filePath):
        print('You need to calculate the resistance of the ' + level + ' ' + '1x' + str(i.__round__(3)) +
              ' carpet using resistanceSaver.py')
        exit()
    file = open(filePath, 'r')
    fileData = file.readlines()
    stretechedResistances.append(float(fileData[1][14:]))

# calculate rho
rhos = []
for f in stretechedResistances:
    rhos.append(f/baseResistance)

# plot
plt.scatter(stretchFactors, rhos)
plt.xticks(stretchFactors)
plt.yticks(range(0, 3))
plt.xlabel("Amount of Stretch")
plt.ylabel("Rho of Graph")
for j in range(len(rhos)):
    plt.text(stretchFactors[j], rhos[j] + .05, rhos[j].__round__(3))

# title
levelTitle = "level " + str(precarpet_level) + " "
smallSquareStr = str(sideOfSmallSquares.__round__(3))
plt.title("Resistance of the Stretched " + levelTitle + smallSquareStr + "Affine Carpet Divided by the Previous Level's "
                                                                         "Unstretched Resistance")

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

