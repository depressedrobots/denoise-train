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

thresh = 4
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
        mask = diff < thresh
        
        currImgBGR = cv2.cvtColor(currImgYUV, cv2.COLOR_YUV2BGR_I420)
        filenameUnfiltered = './outputUnFiltered/' + str(i).zfill(6) + '.png'
        cv2.imwrite(filenameUnfiltered, currImgBGR)

        currImgYUV[mask] = lastImgYUV[mask]
        currImgBGR = cv2.cvtColor(currImgYUV, cv2.COLOR_YUV2BGR_I420)
        filenameFiltered = './outputFiltered/' + str(i).zfill(6) + '.png'
        cv2.imwrite(filenameFiltered, currImgBGR)
    
    lastImgYUV = currImgYUV
    lastImgYUVInt = lastImgYUV.astype('int')    
