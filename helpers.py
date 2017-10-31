import os
from os import walk

# get list of files in /frames
def getFilesInDir(pathToDir):
    files = []

    if True == os.path.exists(pathToDir):
        (_, _, files) = walk(pathToDir).next()

    return files
