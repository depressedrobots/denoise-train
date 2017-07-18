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

diffValues = np.zeros(256)

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
        diff = currImgYUVInt.copy()
        diff[:479] = currImgYUVInt[:479] - lastImgYUVInt[:479]
        diff = abs(diff)

        #for x in np.nditer(diff):
         #   diffValues[x] += 1

        # where diff < thresh, overwrite new pixel with former pixel 
        currImgYUV[diff<thresh] = lastImgYUV[diff<thresh]

        recentImgBGR = cv2.cvtColor(currImgYUV, cv2.COLOR_YUV2BGR_I420)
        newFilename = './output/' + format(i, '06') + '.png'
        cv2.imwrite(newFilename, recentImgBGR)
    
    lastImgYUV = currImgYUV
    lastImgYUVInt = lastImgYUV.astype('int')    

#np.savetxt('diffvalues.txt', diffValues)
