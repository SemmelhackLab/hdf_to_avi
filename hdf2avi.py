import numpy as np
import h5py
import pandas as pd
import cv2
import os
import re
from matplotlib import pyplot as plt
import winsound

experiment = 'E067'
exptyp = '2deg_3deg'
date = '08 FEB 2019'
dir_input = 'E:\\Semmelhack lab\\001 DATA\\2019\\01 behavioral in cyt' \
            '\\FEBRUARY\\' + date +'\\' + experiment + '\\2dotsdiff_'+exptyp +'\\'
dir_out = 'E:\\Semmelhack lab\\002 ANALYSIS\\Two dots\\Different sizes\\'+ exptyp+'\\'

dir_input = 'D:\\2p\\'
dir_out = dir_input
fishIDs = list()

fishIDs += [f for f in os.listdir(dir_input)]

for fish in fishIDs:

    files = []
    for file in os.listdir(dir_input + fish + '\\'):  # read files with .csv then store the filename to files
        if file.endswith(".h5"):
            files.append(file)

    for h5 in files:
        print "PROCESSING: ", h5
        filename, file_extension = os.path.splitext(h5)
        vid = h5py.File(dir_input + fish + '\\' + filename + file_extension, 'r')
        keys = vid.keys()
        images = []
        dotstop = ''
        for i in keys:
            ind = re.findall('\d+', i) # get only the numbers
            images.append(int(ind[0]))
            if '_stop' in i:
                dotstop = '_s@' + str(ind[0])
        images = sorted(images)
        #images = sorted([int(i) for i in images])
        video_name = filename + dotstop + '.avi'
        height, width = vid[vid.keys()[0]][:].shape # get the shape of the first frame
        dir_output = dir_out + experiment + '-' + fish + '\\'
        if not os.path.exists(dir_output):  # create an output directory
            os.makedirs(dir_output)

        video = cv2.VideoWriter(dir_output + video_name, 0, 300, (width, height), isColor=False)

        for im in images:
            img = vid[str(im)][:]
            video.write(img)

        cv2.destroyAllWindows()
        video.release()
        print 'DONE'

print 'FINISHED CONVERTING ALL FILES'
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 5000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)
