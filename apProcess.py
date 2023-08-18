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



# Reading command line prompts / creating variables
init_base = apUtils.intialize()

# Map out directories within "detections" that have .json files
out = init_base.mapDirectory()

# For each day directory populataed with detection data
for day1 in out:
    day1+='/'
    
    # Checking that the directory is for a camera 
    if day1.split('/')[-3].find('1_') != -1:
        init_base.initializeCSV(day1)
        chkCSV = init_base.csvCheck()
        if chkCSV:continue
        
        allIms = glob.glob(day1+'*.json')
        allIms.sort()
        grab4 = np.arange(0,len(allIms))
        
        # If writing video then prepare the file to write to
        if init_base.writevid:
            init_base.initializeVidOut()
            
        # For all images in a specific unit / camera / day
        for seq1,image1 in enumerate(grab4):
            
            ob = open(allIms[image1],'r')
            try:
                lb = json.load(ob)
            except:
                ob.close()
                continue
            ob.close()
            
            if lb.get('meta') == None:
                print('no meta')
                continue
            tempName = lb['meta']['still_filename']
            if tempName.find('data/')== -1:continue
            tempName2 = day1.split('detection')[0]+tempName.split('data/')[1]
            if lb['meta']['bboxes'] == []:
                continue
            bboxI = np.squeeze(lb['meta']['bboxes'])
            oH = False
            allConf = []
            allBbx = []
            writeIM = False
            init_base.openim(tempName2)
            
            for bbx in bboxI:
                bbx = np.squeeze(bbx)
                # Boxes have inconsistent sizes
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
                            init_base.addBbx((pt1,pt2),bbx)
 
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
                        init_base.addBbx((pt1,pt2),bbx)

                    if oH:
                        continue
            # If writing videos, check length and create new if over set limit of frames
            if writeIM:
                if init_base.writevid:
                    init_base.videoUpdate(lb)
                    
                    init_base.vidCount+=1
                    if init_base.vidCount >= 400:
                        init_base.vidM+=1
                        init_base.vidCount = 0
                        init_base.vidOut.release()
                        init_base.initializeVidOut()

                init_base.updateDict(allIms[image1],allConf,allBbx)
        if len(init_base.csvdict['unitID']) > 0:
            init_base.outputCSV()
            init_base.outputFig()

            
    if init_base.writevid:
        init_base.vidOut.release()

