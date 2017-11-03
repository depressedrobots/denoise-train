import helpers
import cv2
import numpy as np
import sys
from scipy.signal import argrelextrema

PATH = './frames'
NOISE_THRESHOLD = 4

filenames = helpers.getFilesInDir(PATH)

if len(filenames) == 0:
        sys.exit("no files in ".append(PATH))

prevImgBW = np.zeros((480,640)).astype('int')
prevDiff = np.full((480,640), 255).astype('int')

for filename in filenames:
    filepath = PATH + '/' + filename
    print('processing image' + filename)
    currImg = cv2.imread(filepath)
    currImgBW = cv2.cvtColor(currImg, cv2.COLOR_BGR2GRAY).astype('int')

    currDiff = abs(currImgBW - prevImgBW)
    # denoise diff
    noiseMask = currDiff <= NOISE_THRESHOLD
    
    currDiff[noiseMask] = 0
    currImgBW[noiseMask] = prevImgBW[noiseMask]
    #localMaxima = argrelextrema(currDiff, np.greater)
    writeOutImgBW = np.copy(currImg)
    writeOutImgBW[noiseMask] = [0, 0, 255]
    #writeOutImgBW[localMaxima] = [0, 0, 255]
    
    newFilename = 'masked-' + filename
    cv2.imwrite(newFilename, writeOutImgBW)

    #newFilename = 'bw-' + filename
    #cv2.imwrite(newFilename, writeOutImgBw)

    prevDiff = currDiff
    prevImgBW = currImgBW

