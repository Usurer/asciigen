#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Usurer
#
# Created:     12/06/2013
# Copyright:   (c) Usurer 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
from PIL import Image, ImageFont, ImageDraw, ImageWin

def main():
     #An image to convert to ascii
    bwGoat = Image.open("goat.jpg")
    #Making it black-n-white
    bwGoat = bwGoat.convert('L');
##    bwGoat.save("bwGoat.jpg")

    sd = getSymbolsDensityArray()

    goatPixels = bwGoat.load()
    w = bwGoat.size[0]
    h = bwGoat.size[1]

    imageDensity = []
    #Goat image is 600x400. I use 2x1 pieces as a single slice to be changed whith ascii symbol
    for row in range(0, 199):
        densityRow = []
        for col in range(0, 599):
            d = calculateSliceWeight(goatPixels, [row*2, col*1])
            densityRow.append(d)
##            sys.stdout.write(str(d) + ' ')
        imageDensity.append(densityRow)
##        sys.stdout.write('\n')

    #Now I want to get a 'step', a level of discretization for image pixels
    #To make convertion better I should convert 'em to ascii in accordance
    #with ascii symbols' density distribution
    allVals = []
    for row in imageDensity:
        for col in row:
            allVals.append(col)
    minMax = getMaxMin(allVals)
    deltaRange = minMax[1] - minMax[0]
    delta = deltaRange / 26
##    print minMax, delta

    normalizedDensities = []
    for row in imageDensity:
        tempRow = []
        for col in row:
            tmp = (col - minMax[0]) // delta
            tempRow.append(tmp)
            ##sys.stdout.write(str(tmp) + ' ')
        normalizedDensities.append(tempRow)
        ##sys.stdout.write('\n')

    f = open('result.txt', 'w')
    for row in normalizedDensities:
        for col in row:
            f.write(sd[0][col-1])
        f.write('\n')
    pass

#Returns an array of [[symbols],[densities] sorted by density
def getSymbolsDensityArray():
    symbolDensityTuples = []
    densities = []
    symbols = []

    for i in range(65, 91):
        image = Image.new("L", (20, 20))
        draw = ImageDraw.Draw(image)
        f = ImageFont.truetype("cour.ttf", 20)
        draw.text((0, 0), str(chr(i)), 100, f)
        symbolDensityTuples.append((chr(i), calculateSymbolWeight(image)))

    for t in symbolDensityTuples:
        densities.append(t[1])
    densities.sort()

    for d in densities:
        for t in symbolDensityTuples:
            if t[1] == d:
                symbols.append(t[0])
                break

    return [symbols, densities]


#A sum of all pixels' values. White is 255, black is zero.
#While we print with black symbols, now white, this weight should be inverted later
def calculateSymbolWeight(image):
    val = 0
    for i in range (0, 19):
        for j in range(0, 19):
            val = val + image.getpixel((i, j))
    return val

#A weight of all pixels in a piece of an image
def calculateSliceWeight(pixArr, sliceTuple):
    res = 0
    for row in range (sliceTuple[1], sliceTuple[1] + 2):
        for col in range (sliceTuple[0], sliceTuple[0] + 1):
            try:
                res = res + (255 - pixArr[row, col])
            except (IndexError):
                print "ERROR: " + str(row) + ';' + str(col)
##        sys.stdout.write(str(res))
##    sys.stdout.write(str(pixArr[300, 300]))
    return res

#[min, max] values of array
def getMaxMin(arr):
    min = arr[0]
    max = arr[1]
    for a in arr:
        if a > max:
            max = a
        if a < min:
            min = a
    return [min, max]

if __name__ == '__main__':
    main()

