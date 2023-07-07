# Generating images in a new folder on desktop to preview bbxes and images
# TODO: Potential to zip and transfer folder with other metrics over ssh

import cv2 as cv
import numpy as np
import json
import glob
import datetime
import os

font = cv.FONT_HERSHEY_SIMPLEX
fldFind = datetime.datetime.now()
fldFind2 = str(fldFind.year)[2:]+'%02d'%fldFind.month+'%02d'%fldFind.day
# org
org = (100, 100)
fontScale = 4
color = (255, 0, 0)
thickness = 7
   
# Using cv2.putText() method

xBlock = [(0,2592),(0,2592),(2592,5184),(2592,5184)]
yBlock = [(0,1944),(1944,3888),(0,1944),(1944,3888)]

vidOut = cv.VideoWriter('/Users/matt/Desktop/test.avi',cv.VideoWriter_fourcc('M','J','P','G'),30,(2592,1944))
f1 = glob.glob('/Volumes/Untitled/detections/*/')
f1 = ['/Volumes/Untitled/detections/1_3_1_4/']
for cam1 in f1:
    if cam1.split('/')[-2].find('1_') != -1:
        getDays = glob.glob(cam1+'*/')
        for day1 in getDays:
            if day1.find(fldFind2) != -1:
                bigIm = np.zeros((3888,5184,3))
                allIms = glob.glob(day1+'*.json')
                allIms.sort()
                #grab4 = np.append([-1],np.squeeze(np.floor(np.random.rand(1,3)*len(allIms))))
                grab4 = np.arange(0,len(allIms))
                #grab4 = np.arange(0,35)
                for seq1,image1 in enumerate(grab4.astype(np.int)):
                    ob = open(allIms[image1],'r')
                    lb = json.load(ob)
                    ob.close()
                    if lb.get('meta') == None:
                        print('no meta')
                        continue
                    tempName = lb['meta']['still_filename']
                    tempName2 = cam1.split('detection')[0]+tempName.split('data/')[1]
                    fullIm = cv.imread(tempName2)
                    if lb['meta']['bboxes'] == []:
                        continue
                    bboxI = np.squeeze(lb['meta']['bboxes'])
                    #bboxI = lb['meta']['bboxes'][0][0]
                    oH = False
                    for bbx in bboxI:
                        bbx = np.squeeze(bbx)
                        if len(np.shape(bbx)) == 2:
                            for bbx2 in bbx:
                                if bbx2[1] < 0.45:
                                    break
                                pt1 = (int(bbx2[2][0]*1944),int(bbx2[2][1]*2592))
                                pt2 = (int(bbx2[2][2]*1944),int(bbx2[2][3]*2592))
                                pt1 = (int(bbx2[2][1]*(2592)),int(bbx2[2][0]*(1944)))
                                pt2 = (int(bbx2[2][3]*(2592)),int(bbx2[2][2]*(1944)))
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
                            if bbx[1] < 0.45:
                                break
                            pt1 = (int(bbx[2][0]*1944),int(bbx[2][1]*2592))
                            pt2 = (int(bbx[2][2]*1944),int(bbx[2][3]*2592))
                            pt1 = (int(bbx[2][1]*(2592)),int(bbx[2][0]*(1944)))
                            pt2 = (int(bbx[2][3]*(2592)),int(bbx[2][2]*(1944)))

                            clr = (195,100,100,100)
                            thickness= 20
                            fullIm = cv.rectangle(fullIm, pt1, pt2, clr, thickness)
                            org1 = (pt1[0]-25,pt1[1]-25)
                            tP = str(np.round(bbx[1],3))+'%'
                            fullIm = cv.putText(fullIm, tP, org1, font,2, color, 2, cv.LINE_AA)
                            if oH:
                                continue
                    tP = cam1.split('/')[-2]+' '+lb['meta']['datetime'].split(' ')[1]
                    fullIm = cv.putText(fullIm, tP, org, font,fontScale, color, thickness, cv.LINE_AA)
                    vidOut.write(fullIm)
                break
                    #bigIm[yBlock[seq1][0]:yBlock[seq1][1],xBlock[seq1][0]:xBlock[seq1][1],:] = fullIm
                #if os.path.isdir('/home/pi/Desktop/sampleIms/') == False:
                #    os.mkdir('/home/pi/Desktop/sampleIms/')
                #tempName = '/home/pi/Desktop/sampleIms/'+cam1.split('/')[-2]+'.jpg'
                #cv.imwrite(tempName,bigIm)
vidOut.release()
