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

width = 640
height = 480
thresh = 1.8
numBlocksPerAxis = 10
blockWidth = width / numBlocksPerAxis
blockHeight = height / numBlocksPerAxis
indexArray = np.arange(width*height).reshape(height,width)


lastImgGray = None
lastImgGrayLin = None
lastImgLin = None

for i, filename in enumerate(filenames):
    print('processing ' + str(i+1) + '/' + str(len(filenames)))

    filepath = path + '/' + filename
    currImg = cv2.imread(filepath)
    currImgGray = cv2.cvtColor(currImg, cv2.COLOR_BGR2GRAY)
    currImgGrayLin = currImgGray.reshape(width*height)
    currImgLin = currImg.reshape(width*height,3)

    if i != 0:
        currImgGrayIntLin = currImgGrayLin.astype('int')
        diff = currImgGrayIntLin - lastImgGrayIntLin
        diff = abs(diff)
        
        # compute the average of each block
        for by in np.arange(numBlocksPerAxis):
            for bx in np.arange(numBlocksPerAxis):
                startY = by * blockHeight
                startX = bx * blockWidth
                indeces = indexArray[startY:startY+blockHeight, startX:startX + blockWidth]
                block = diff[indeces]
                blockMean = np.mean(block)
                if blockMean < thresh:
                    currImgGrayLin[indeces] = lastImgGrayLin[indeces]
                    currImgLin[indeces] = lastImgLin[indeces]
                    print blockMean
        
        filenameFiltered = './outputMasked/' + str(i).zfill(6) + '.png'
        currImgNonLin = currImgLin.reshape(height, width,3)

        cv2.imwrite(filenameFiltered, currImgNonLin)
    
    lastImgGrayLin = currImgGrayLin
    lastImgGrayIntLin = lastImgGrayLin.astype('int')    
    lastImgLin = currImgLin
