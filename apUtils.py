import cv2 as cv
import numpy as np
import json
import glob
import datetime
import os
import argparse
import csv


class intialize:
    
    def __init__(self):
        ''' initialize command line parameters, create directories, set variables'''
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-d', '--directory_main', default='/Volumes/Untitled/',
            help='save single images when triggered')
        parser.add_argument(
            '-f', '--figures', default=False, action='store_true',
            help='generate output figures of detections across time')
        parser.add_argument(
            '-t', '--threshold', default=0.45,
            help='inclusion threshold as proportion out of 1, default: 0.45')
        parser.add_argument(
            '-v', '--videoSample', default=False, action='store_true',
            help='Run selected model across example video, creates new csv')
        parser.add_argument(
            '-b', '--binsize', default=300,
            help='Bin size to calculate detection rate')
        args = parser.parse_args()
        
        self.thresh = args.threshold
        self.getdir = args.directory_main
        self.writevid = args.videoSample
        self.detectRate = args.binsize
        self.genFig = args.figures
        


        # Getting CWD and making new folder for videos
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.org = (100, 100)
        self.fontScale = 4
        self.color = (255, 0, 0)
        self.bbxcolor = (195,100,100,100)
        self.thickness = 20 
        self.textthickness = 7
        self.vidCount = 0
        self.vidM = 0
        
        
        
    def mapDirectory(self):
        # Getting CWD and making new folder for videos
        basedir = os.getcwd()+'/APprocess/' 
        if not os.path.isdir(basedir):os.makedirs(basedir)
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

    def openim(self,impath):
        self.currimpath = impath
        self.currim = cv.imread(impath)

    def initializeCSV(self,dir1):
        '''Creating dictionary for detections that will be used to create CSV'''
        self.csvdict = {}
        self.csvdict['unitID'] = []
        self.csvdict['camID'] = []
        self.csvdict['datetime'] = []
        self.csvdict['date'] = []
        self.csvdict['time'] = []
        self.csvdict['timestamp'] = []
        self.csvdict['image_filepath'] = []
        self.csvdict['json_filepath'] = []
        self.csvdict['confidence'] = []
        self.csvdict['bbox'] = []
        
        
        # Assumption that AP_ID is the directory title before the "detection" folder 
        self.AP_ID = dir1.split('/')[-5]
        self.cam_ID = dir1.split('/')[-3]
        self.dir1 = dir1
        
    def initializeVidOut(self):
        '''Create video directory and video object to write to'''
        self.vidDir1 = os.getcwd()+'/APprocess/'+'APvideos/'+self.AP_ID+'/'+self.cam_ID+'/'
        if not os.path.isdir(self.vidDir1):os.makedirs(self.vidDir1)
        self.date1 = self.dir1.split('/')[-2]
        self.videoName = self.vidDir1+self.AP_ID+'-'+self.cam_ID+'-'+self.date1+'-%02d.avi'%self.vidM
        self.vidOut = cv.VideoWriter(self.videoName,cv.VideoWriter_fourcc('M','J','P','G'),30,(2592,1944))
    
    def csvCheck(self):
        self.csvDir = os.getcwd()+'/APprocess/'+'APcsv/'+self.AP_ID+'/'+self.cam_ID+'/'
        tempCSV = self.csvDir+self.AP_ID+'_'+self.cam_ID+'_'+self.dir1.split('/')[-2]+'.csv'
        self.csvfilename = tempCSV
        if not os.path.isdir(self.csvDir):os.makedirs(self.csvDir)
        lout = os.path.isfile(self.csvfilename)
        if lout:
            print('file already exists- skipping: '+self.csvfilename)
        else:
            print('Processing - '+self.csvfilename)
        return lout
    
    def addBbx(self,bbxes,inferenceOut):

        self.currim = cv.rectangle(self.currim, bbxes[0],bbxes[1], self.bbxcolor, self.thickness)
        org1 = (bbxes[0][0]-25,bbxes[0][1]-25)
        tP = str(np.round(inferenceOut[1],3))+'%'
        self.currim = cv.putText(self.currim, tP, org1, self.font,2, self.color, 2, cv.LINE_AA)
        
        
    def videoUpdate(self,lb):
        self.detection = lb
        tP = self.dir1.split('/')[-2]+' '+lb['meta']['datetime'].split(' ')[1]
        fullIm = cv.putText(self.currim, tP, self.org, self.font,self.fontScale, self.color, self.textthickness, cv.LINE_AA)
        if fullIm.shape == (1944,2592,3):
            self.vidOut.write(fullIm)
        
    def updateDict(self,jsonDir,allConf,allBbx,dtetime):
        self.csvdict['unitID'].append(self.AP_ID)
        self.csvdict['camID'].append(self.dir1.split('/')[-3])
        self.csvdict['datetime'].append(dtetime)
        self.csvdict['date'].append(dtetime.split(' ')[0])
        self.csvdict['time'].append(dtetime.split(' ')[1])
        self.csvdict['timestamp'].append(datetime.datetime.fromisoformat(dtetime).timestamp())
        self.csvdict['image_filepath'].append(self.currimpath)
        self.csvdict['json_filepath'].append(jsonDir)
        self.csvdict['confidence'].append(allConf)
        self.csvdict['bbox'].append(allBbx)
    
    def outputCSV(self):
        # Create list from dictionary 
        allValues = []
        for ind,ele in enumerate(self.csvdict['unitID']):
            tempK = []
            for nnmes in self.csvdict.keys():
                tempK.append(self.csvdict[nnmes][ind])
            allValues.append(tempK)
       #headers = ['unitID','camID','datetime','date','time','timestamp','image_filepath','json_filepath','confidence','bbox']
        headers = [ele for ele in self.csvdict.keys()]
        
        with open(self.csvfilename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for ele in allValues:
                writer.writerow(ele)
                
    def outputFig(self):
        from matplotlib import pyplot as plt
        # Getting CWD and making new folder for videos 
        figDir1 = os.getcwd()+'/APprocess/'+'APfigs/'+self.AP_ID+'/'+self.cam_ID+'/'
        self.figdir = figDir1
        if not os.path.isdir(figDir1):os.makedirs(figDir1)
        plt.figure(figsize=(6,3),dpi=200)
        
        tFirst = datetime.datetime.fromisoformat(self.csvdict['date'][0]+' 05:00').timestamp()
        tLast = datetime.datetime.fromisoformat(self.csvdict['date'][0]+' 22:00').timestamp()
        indx = np.arange(tFirst,tLast,60*30)
        indx2 = np.arange(tFirst,tLast,60*120)
        xll = ['%02d:%02d'%(datetime.datetime.fromtimestamp(ele).hour,datetime.datetime.fromtimestamp(ele).minute) for ele in indx2]
        plt.hist(self.csvdict['timestamp'],indx,color=(0.25,0.25,0.25,0.5))
        plt.xticks(np.arange(tFirst,tLast,60*120),xll)
        plt.ylabel('Count')
        tempPDF = self.figdir+self.AP_ID+'_'+self.cam_ID+'_'+self.dir1.split('/')[-2]+'.pdf'
        self.pdffilename = tempPDF
        plt.savefig(tempPDF,dpi=200)
        

    def mapCSV(self):
        # Getting CWD and making new folder for videos
        basedir = os.getcwd()+'/APprocess/Rates/'
        self.detectRateFile = basedir 
        if not os.path.isdir(basedir):os.makedirs(basedir)
        for ele in range(0,3):print('')
        print('Writing files to: '+os.getcwd()+'/APprocess/Rates/')
        for ele in range(0,2):print('')
        # Getting directories for a specific unit
        print('###########################')
        print('### Mapping directories ###')
        print('###########################')
        print('')
        print('Searching for CSVs within:')
        print(self.getdir)
        out = [x[0] for x in os.walk(self.getdir) \
            if (x[0].find('csv')!= -1) \
                and x[0].find('_4')!=-1]
        for ele in range(0,1):print('')
        print('    Done mapping    ')
        print('    '+str(len(out))+' directories found')
        for ele in range(0,1):print('')
        return out
