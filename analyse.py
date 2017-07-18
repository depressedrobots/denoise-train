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

diffValuesY = np.zeros(256).astype('uint32')
diffValuesU = np.zeros(256).astype('uint32')
diffValuesV = np.zeros(256).astype('uint32')

thresh = 50
lastImgYUV = None
lastImgYUVInt = None
for i, filename in enumerate(filenames):
    print('processing ' + str(i+1) + '/' + str(len(filenames)))

    filepath = path + '/' + filename
    currImg = cv2.imread(filepath)
    currImgYUV = cv2.cvtColor(currImg, cv2.COLOR_BGR2YUV_I420)

    # special case: idx 0, can't compare with previous frame
    if i != 0:
        currImgYUVInt = currImgYUV.astype('int')
        diff = currImgYUVInt - lastImgYUVInt
        diff = abs(diff)

        for x in np.nditer(diff[:479]):
            diffValuesY[x] += 1

        for x in np.nditer(diff[480:599]):
            diffValuesU[x] += 1

        for x in np.nditer(diff[600:]):
            diffValuesV[x] += 1
    
    lastImgYUV = currImgYUV
    lastImgYUVInt = lastImgYUV.astype('int')    

np.savetxt('diffvaluesY.txt', diffValuesY)
np.savetxt('diffvaluesU.txt', diffValuesU)
np.savetxt('diffvaluesV.txt', diffValuesV)
