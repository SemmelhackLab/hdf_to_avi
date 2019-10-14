import os
import numpy as np
import h5py
import pandas as pd
import cv2
import re

fish = list()
mainfolder = 'D:\\Semmelhack lab\\001 DATA\\2P data\\'
date = ['28 AUG 2019', '29 AUG 2019']
expt = ['2P029', '2P030']
dir_out = 'D:\\Semmelhack lab\\002 ANALYSIS\\2p_2dots\\effect of target to competitor\\'
fish += [f for f in os.listdir(mainfolder)]
#dates = [dates[6]]

for count, d in enumerate(date):

    folder = mainfolder + d + '\\' + d + '\\' + expt[count] + '\\'
    print folder
    exp_subfolders = list()
    exp_subfolders = [f for f in os.listdir(folder)]

    for exp in exp_subfolders:

        exp_folder = folder + exp + '\\'
        fish_list = list()
        fish_list = [f for f in os.listdir(exp_folder)]
        for fish in fish_list:

            fish_folder = exp_folder + fish + '\\'
            files = []
            dir_output = dir_out + expt[count] + '-' + fish + '\\'

            if not os.path.exists(dir_output):  # create an output directory
                os.makedirs(dir_output)
            for file in os.listdir(fish_folder):  # read files with .csv then store the filename to files
                if file.endswith(".h5"):
                    print file
                    files.append(file)
            for h5 in files:
                print "PROCESSING: ", h5
                filename, file_extension = os.path.splitext(h5)
                vid = h5py.File(fish_folder + filename + file_extension, 'r')
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

                video = cv2.VideoWriter(dir_output + video_name, 0, 300, (width, height), isColor=False)
                for im in images:
                    img = vid[str(im)][:]
                    video.write(img)

                cv2.destroyAllWindows()
                video.release()
                print 'DONE'
