import cv2 as cv
import numpy as np
import json
import glob
import datetime
import os
import argparse
import csv
from matplotlib import pyplot as plt

class intialize:
    
    ## interpret command line flags ##
    def cmdline_run():
 
        return args

    def __init__(self):
        self.csvDir = os.getcwd()+'/APprocess/'+'APcsv/'
        # Grab any command line flags
        #args = cmdline_run()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-d', '--directory_main', default='/Volumes/Untitled/',
            help='save single images when triggered')
        parser.add_argument(
            '-r', '--resolution', default='small',
            help='set camera resolution "small" default, options: small, medium, medium2, large')
        parser.add_argument(
            '-t', '--threshold', default=0.45,
            help='inclusion threshold as proportion out of 1, default: 0.45')
        parser.add_argument(
            '-v', '--videoSample', default=False, action='store_true',
            help='Run selected model across example video, creates new csv')
        args = parser.parse_args()
        
        self.thresh = args.threshold
        self.getdir = args.directory_main
        self.writevid = args.videoSample

    def mapDirectory(self):
        # Getting CWD and making new folder for videos 
        csvDir1 = self.csvDir
        if not os.path.isdir(csvDir1):os.makedirs(csvDir1)
        for ele in range(0,3):print('')
        print('Writing files to: '+os.getcwd()+'/APprocess/')
        for ele in range(0,2):print('')
        # Getting directories for a specific unit
        print('###########################')
        print('### Mapping directories ###')
        print('###########################')

        out = [x[0] for x in os.walk(self.getdir) \
            if (x[0].find('detections')!= -1 \
            and x[0].find('.Trash') == -1 \
            and x[0].find('_4/2') != -1)]
        for ele in range(0,1):print('')
        print('    Done mapping    ')
        print('    '+str(len(out))+' directories found')
        for ele in range(0,1):print('')
        return out


    