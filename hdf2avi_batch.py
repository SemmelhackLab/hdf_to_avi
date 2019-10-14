import numpy as np
import h5py
import pandas as pd
import cv2
import os
import re
from matplotlib import pyplot as plt
import winsound

dates = list()
mainfolder = 'D:\\Semmelhack lab\\001 DATA\\2P data\\'
dates += [f for f in os.listdir(mainfolder)]
dates = [dates[6]]

for d in dates:

    folder = mainfolder + d + '\\' + d + '\\'
    exp_subfolders = list()
    exp_subfolders = [f for f in os.listdir(folder)]

    for exp in exp_subfolders:

        exp_folder = folder + exp + '\\'
        exptyp_subfolders = list()
        exptyp_subfolders = [f for f in os.listdir(exp_folder)]
        for exptyp in exptyp_subfolders:

            fish_folder = exp_folder + exptyp + '\\'
            fish_subfolders = list()
            fish_subfolders = [f for f in os.listdir(fish_folder)]

            dir_out = 'D:\\Semmelhack lab\\002 ANALYSIS\\2p_2dots\\'+ exptyp + '\\'
            for fish in fish_subfolders:

                files = []
                for file in os.listdir(fish_folder + fish + '\\'):  # read files with .csv then store the filename to files
                    if file.endswith(".h5"):
                        files.append(file)
                for h5 in files:
                    print "PROCESSING: ", h5
                    filename, file_extension = os.path.splitext(h5)
                    vid = h5py.File(fish_folder + fish + '\\' + filename + file_extension, 'r')
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
                    dir_output = dir_out + exp + '-' + fish + '\\'
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
#frequency = 2500  # Set Frequency To 2500 Hertz
#duration = 5000  # Set Duration To 1000 ms == 1 second
#winsound.Beep(frequency, duration)
