import sys
from PIL import Image, ImageFont, ImageDraw, ImageWin


def main():
     #An image to convert to ascii
    bwGoat = Image.open("goat.jpg")
    #Making it black-n-white
    bwGoat = bwGoat.convert('L')
##    bwGoat.save("bwGoat.jpg")

    sd = getSymbolsDensityArray()

    goatPixels = bwGoat.load()
    w = bwGoat.size[0]
    h = bwGoat.size[1]

    imageDensity = []
    #Goat image is 600x400. I use 2x1 pieces as a single slice to be changed with ascii symbol
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

    discreteArray = getDiscreteArray(sd[1])
    print discreteArray

    allVals = []
    for row in imageDensity:
        for col in row:
            allVals.append(col)
    minMax = getMaxMin(allVals)
    deltaRange = minMax[1] - minMax[0]
    delta = float(deltaRange) / len(discreteArray)
    print 'Delta is ' + str(delta)

    normalizedDensities = []
    for row in imageDensity:
        tempRow = []
        for col in row:
            tmp = int((col - minMax[0]) // delta)
            tempRow.append(tmp)
        normalizedDensities.append(tempRow)

    print sd[0]
    print sd[1]

    f = open('result_2.txt', 'w')
    for row in normalizedDensities:
        for col in row:
            symb = getSymbolByDensity(sd, discreteArray[col])
            f.write(symb)
        f.write('\n')

    print 'Conversion finished!'
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


#Returns a symbol of known density from [symbols, densities] type of array.
def getSymbolByDensity(symbolDensityArray, density):
    result = None
    for i in range(0, len(symbolDensityArray[1])):
        if symbolDensityArray[1][i] == density:
            result = symbolDensityArray[0][i]
            break
    return result


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


def getMinDeltaOfArray(arr):
    delta = abs(arr[0] - arr[1])
    for i in arr:
        for j in arr:
            if i != j:
                if abs(i - j) < delta:
                    delta = abs(i - j)
    return delta


#Used to convert array of symbol densities to array of ranges.
#For example if we have [1, 3, 10], the result should be [1, 1, 3, 3, 3, 3, 10] or... well.. kinda like that )
def getDiscreteArray(arr):
    delta = getMinDeltaOfArray(arr)
    minVal = getMaxMin(arr)[0]
    maxVal = getMaxMin(arr)[1]
    arrayRange = maxVal - minVal
    cellsAmount = arrayRange // delta + 1  # It should be Math.Ceil here, but I don't want import it yet
    tmpArr = []
    arrayIterator = 0
    for i in range(0, cellsAmount):
        if (minVal + delta * i) > arr[arrayIterator]:
            arrayIterator += 1
        tmpArr.append(arr[arrayIterator])
    return tmpArr


if __name__ == '__main__':
    main()

