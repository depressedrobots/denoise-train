import os
import cv2
import helpers

PATH = './frames'
OUTPUT_DIR = './smallframes'

filenames = helpers.getFilesInDir(PATH)

if len(filenames) == 0:
    sys.exit("no files in ".append(PATH))

# create output directory
if False == os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

counter = 0
for filename in filenames:
    filepath = PATH + '/' + filename
    print('processing image ' + str(counter) + ' of ' + str(len(filenames)))

    # include only png files 
    if False == filename.endswith('.png'):
        continue

    img = cv2.imread(filepath)
    img = cv2.resize(img, (40, 30))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite(OUTPUT_DIR + '/small_' + filename, img)
    counter += 1
