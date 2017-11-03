import helpers
import cv2
import numpy as np
import sys
import os
from scipy.signal import argrelextrema

PATH = './frames'
OUTPUT_DIR = './frames/diff'

filenames = helpers.getFilesInDir(PATH)

if len(filenames) == 0:
        sys.exit("no files in ".append(PATH))

# create output directory
if False == os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# keep the last image after each iteration to create the diff
# start with a black image for the first diff
prevImg = np.zeros((480, 640, 3)).astype('int16')

counter = 0
for filename in filenames:
    # include only png files 
    if False == filename.endswith('.png'):
        continue

    filepath = PATH + '/' + filename
    print('processing image ' + str(counter) + ' of ' + str(len(filenames)))

    # compute rgb diff
    currImg = cv2.imread(filepath).astype('int16')
    diff = (currImg - prevImg)
    
    # write diff to .npy binary file
    outputFilename = OUTPUT_DIR + '/diff-' + filename
    np.save(outputFilename, diff)

    prevImg = currImg
    counter += 1
