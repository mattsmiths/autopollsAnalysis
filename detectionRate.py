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

# Looks for processed CSVs
csvList = init_base.mapCSV()
detectRate = float(init_base.detectRate)
thresh = float(init_base.thresh)

# For each directory within apCSV
for filez in csvList:
    
    # List actual CSVs
    getFiles = glob.glob(filez+'/*.csv')
    for file1 in getFiles:
        
        # if it is a CSV
        if file1.find('.csv') != -1:
            in1 = open(file1,'r')
            getData = in1.readlines()

            baseRate = datetime.datetime.fromisoformat(getData[1].split(',')[3] + ' 05:00:00').timestamp()
            topRate = datetime.datetime.fromisoformat(getData[1].split(',')[3] + ' 23:00:00').timestamp()       
            bins = np.arange(baseRate,topRate,detectRate)
            numBins = len(bins)
            rateCount = np.zeros((numBins))
                      
            for instc in getData[1:]:
                
                tempStamp = datetime.datetime.fromisoformat(instc.split(',')[2]).timestamp()
                binAdd = int((tempStamp-baseRate)//detectRate)
                
                if instc.split(',')[8][-1] != ']': 
                    confs = [float(ele2) for ele2 in instc.split('"')[1][1:-1].split(',')]
                    for conf in confs:
                        if conf > thresh:
                            rateCount[binAdd]+=1
                else:
                    if float(instc.split(',')[8][1:-1]) > thresh:
                        rateCount[binAdd]+=1

            tempCSV = {}
            tempCSV['detectionRate'] = rateCount
            tempCSV['time'] = []
            tempCSV['date'] = []
            tempCSV['timestamp'] = []
            tempCSV['datetime'] = []
            for tt in bins:
                lg3 = datetime.datetime.fromtimestamp(tt).isoformat().split('T')
                tempCSV['time'].append(lg3[1])
                tempCSV['date'].append(lg3[0])
                tempCSV['timestamp'].append(tt)
                tempCSV['datetime'].append(lg3[0]+' '+lg3[1])
            
            
            # Create list from dictionary 
            allValues = []
            for ind,ele in enumerate(tempCSV['time']):
                tempK = []
                for nnmes in tempCSV.keys():
                    tempK.append(tempCSV[nnmes][ind])
                allValues.append(tempK)
            #headers = ['detectionRate','unitID','camID','datetime','date','time','timestamp']
            headers = [ele for ele in tempCSV.keys()]
            tempsave = init_base.detectRateFile+file1.split('/')[-1]
            
            with open(tempsave, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                for ele in allValues:
                    writer.writerow(ele)