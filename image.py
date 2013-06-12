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
    a = ImageFont.load_default()
    image = Image.new("L", (1000, 1000))

##    a = pixels[1]
##    sys.stdout.write('sd')
##    sys.stdout.write(str(a))
##    for i in range(0, 99):
##        for j in range(0, 99):
##            sys.stdout.write(str(pixels[i * 100 + j]))
##        sys.stdout.write('\n')
##    sys.stdout.write('\n')
    s = ''
    for i in range(65, 91):
        s = s + chr(i)

    draw = ImageDraw.Draw(image)
    f = ImageFont.truetype("cour.ttf", 20)
    draw.text((0, 0), s, 100, f)

    pixels = list(image.getdata())
##    for i in range(0, 19):
##        for j in range(0, 19):
##            sys.stdout.write(str(pixels[i * 20 + j]) + ' ')
##        sys.stdout.write('\n')

    image.save('a.bmp')
    pass

if __name__ == '__main__':
    main()
