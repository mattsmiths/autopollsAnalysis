'''
Main script for obtaining potential directories, generating CSVs, figures, and videoss
'''
import cv2 as cv
import numpy as np
import json
import glob
import datetime
import os
import argparse
import csv
from matplotlib import pyplot as plt
import apUtils




init_base = apUtils.intialize()
out = init_base.mapDirectory()




# For each day directory populataed with detection data
for day1 in out:
    day1+='/'
    
    # Checking that the directory is for a camera 
    if day1.split('/')[-3].find('1_') != -1:
        tempKey = {}
        tempKey['unitID'] = []
        tempKey['camID'] = []
        tempKey['datetime'] = []
        tempKey['date'] = []
        tempKey['time'] = []
        tempKey['timestamp'] = []
        tempKey['image_filepath'] = []
        tempKey['json_filepath'] = []
        tempKey['confidence'] = []
        tempKey['bbox'] = []
        
        allIms = glob.glob(day1+'*.json')
        allIms.sort()
        grab4 = np.arange(0,len(allIms))

        # Assumption that AP_ID is the directory title before the "detection" folder 
        AP_ID = day1.split('/')[-5]
        
        # If writing video then prepare the file to write to
        if init_base.writevid:
            font = cv.FONT_HERSHEY_SIMPLEX
            org = (100, 100)
            fontScale = 4
            color = (255, 0, 0)
            thickness = 7
        
            # Getting CWD and making new folder for videos 
            vidDir1 = os.getcwd()+'/APprocess/'+'APvideos/'
            vidCount = 0
            vidM = 0
            if not os.path.isdir(vidDir1):os.makedirs(vidDir1)
            
            vidOut = cv.VideoWriter(vidDir1+AP_ID+'_00.avi',cv.VideoWriter_fourcc('M','J','P','G'),30,(2592,1944))
        
        # For all images in a specific unit / camera / day
        for seq1,image1 in enumerate(grab4.astype(np.int)):
            
            ob = open(allIms[image1],'r')
            lb = json.load(ob)
            ob.close()
            if lb.get('meta') == None:
                print('no meta')
                continue
            tempName = lb['meta']['still_filename']
            tempName2 = day1.split('detection')[0]+tempName.split('data/')[1]
            fullIm = cv.imread(tempName2)
            if lb['meta']['bboxes'] == []:
                continue
            bboxI = np.squeeze(lb['meta']['bboxes'])
            oH = False
            allConf = []
            allBbx = []
            writeIM = False
            for bbx in bboxI:
                bbx = np.squeeze(bbx)
                if len(np.shape(bbx)) == 2:
                    for bbx2 in bbx:
                        if bbx2[1] < float(init_base.thresh):
                            break
                        
                        # Append to list of high confidence detections, write image to vid if applicable
                        allConf.append(bbx2[1])
                        writeIM = True
                        
                        pt1 = (int(bbx2[2][1]*(2592)),int(bbx2[2][0]*(1944)))
                        pt2 = (int(bbx2[2][3]*(2592)),int(bbx2[2][2]*(1944)))
                        allBbx.append([pt1[0],pt1[1],pt2[0],pt2[1]])
                        if init_base.writevid:
                            clr = (195,100,100,100)
                            thickness= 20
                            fullIm = cv.rectangle(fullIm, pt1, pt2, clr, thickness)
                            org1 = (pt1[0]-25,pt1[1]-25)
                            tP = str(np.round(bbx[1],3))+'%'
                            fullIm = cv.putText(fullIm, tP, org1, font,2, color, 2, cv.LINE_AA)
                else:
                    if np.shape(bboxI) == (3,) and np.shape(bbx) == ():
                        bbx = bboxI
                        oH = True
                    if bbx[1] < float(init_base.thresh):
                        break
                    
                    allConf.append(bbx[1])
                    writeIM = True
                    
                    pt1 = (int(bbx[2][1]*(2592)),int(bbx[2][0]*(1944)))
                    pt2 = (int(bbx[2][3]*(2592)),int(bbx[2][2]*(1944)))
                    allBbx.append([pt1[0],pt1[1],pt2[0],pt2[1]])
                    
                    if init_base.writevid:
                        clr = (195,100,100,100)
                        thickness= 20
                        fullIm = cv.rectangle(fullIm, pt1, pt2, clr, thickness)
                        org1 = (pt1[0]-25,pt1[1]-25)
                        tP = str(np.round(bbx[1],3))+'%'
                        fullIm = cv.putText(fullIm, tP, org1, font,2, color, 2, cv.LINE_AA)

                    if oH:
                        continue
            if writeIM:
                if init_base.writevid:
                    tP = day1.split('/')[-2]+' '+lb['meta']['datetime'].split(' ')[1]
                    fullIm = cv.putText(fullIm, tP, org, font,fontScale, color, thickness, cv.LINE_AA)
                    vidOut.write(fullIm)
                    vidCount+=1
                    if vidCount >= 400:
                        vidM+=1
                        vidCount = 0
                        vidOut.release()
                        vidOut = cv.VideoWriter(vidDir1+AP_ID+'_%02d.avi'%vidM,cv.VideoWriter_fourcc('M','J','P','G'),30,(2592,1944))
            
            
                tempKey['unitID'].append(AP_ID)
                tempKey['camID'].append(day1.split('/')[-3])
                tempKey['datetime'].append(lb['meta']['datetime'])
                tempKey['date'].append(lb['meta']['datetime'].split(' ')[0])
                tempKey['time'].append(lb['meta']['datetime'].split(' ')[1])
                tempKey['timestamp'].append(datetime.datetime.fromisoformat(lb['meta']['datetime']).timestamp())
                tempKey['image_filepath'].append(tempName2)
                tempKey['json_filepath'].append(allIms[image1])
                tempKey['confidence'].append(allConf)
                tempKey['bbox'].append(allBbx)
        
        # Create list from dictionary 
        allValues = []
        for ind,ele in enumerate(tempKey['unitID']):
            tempK = []
            for nnmes in tempKey.keys():
                tempK.append(tempKey[nnmes][ind])
            allValues.append(tempK)
        headers = ['unitID','camID','datetime','date','time','timestamp','image_filepath','json_filepath','confidence','bbox']

        tempCSV = init_base.csvDir+day1.split('/')[-5]+'_'+day1.split('/')[-3]+'_'+day1.split('/')[-2]+'.csv'
        with open(tempCSV, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for ele in allValues:
                writer.writerow(ele)
                
        # Getting CWD and making new folder for videos 
        figDir1 = os.getcwd()+'/APprocess/'+'APfigs/'
        if not os.path.isdir(figDir1):os.makedirs(figDir1)
        plt.figure(figsize=(6,3),dpi=200)
        
        tFirst = datetime.datetime.fromisoformat(tempKey['date'][0]+' 05:00').timestamp()
        tLast = datetime.datetime.fromisoformat(tempKey['date'][0]+' 22:00').timestamp()
        indx = np.arange(tFirst,tLast,60*30)
        indx2 = np.arange(tFirst,tLast,60*120)
        xll = ['%02d:%02d'%(datetime.datetime.fromtimestamp(ele).hour,datetime.datetime.fromtimestamp(ele).minute) for ele in indx2]
        plt.hist(tempKey['timestamp'],indx,color=(0.25,0.25,0.25,0.5))
        plt.xticks(np.arange(tFirst,tLast,60*120),xll)
        plt.ylabel('Count')
        plt.savefig(figDir1+tempCSV.split('/')[-1].split('.')[0]+'.pdf',dpi=200)
            
if init_base.writevid:
    vidOut.release()

