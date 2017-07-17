import cv2
import numpy as np
import sys
import os
from os import walk

# get list of files in /frames
path = "./frames"
if False == os.path.exists(path):
    sys.exit("/frames dir not present")

(_, _, filenames) = walk(path).next()

if len(filenames) == 0:
    sys.exit("no files in /frames")

lastImgGrayInt = None
for i, filename in enumerate(filenames):
    print('processing ' + str(i+1) + '/' + str(len(filenames)))

    filepath = path + '/' + filename
    currImg = cv2.imread(filepath)
    currImgGray = cv2.cvtColor(currImg, cv2.COLOR_BGR2GRAY)
    currImgGrayInt = currImgGray.astype('int')

    # special case: idx 0
    if i != 0:
       diff = currImgGrayInt - lastImgGrayInt
       diff = abs(diff)
       diffUInt = diff.astype('uint8')
       newFilename = 'output/' + format(i, '06') + '.png'
       cv2.imwrite(newFilename, diffUInt)
    
    lastImgGrayInt = currImgGrayInt
    
