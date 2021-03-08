import json
import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt



class MSIImageData:
    def __init__(self):
        self.dataLoaded = False          


    
    def LoadCachedData(self, cachedData):
        self.xyzi_data= cachedData

    def XYZArray(self):
        return self.xyzi_data

    def NumImages(self):
        return len(self.xyzi_data[0]['I']) if len(self.xyzi_data) > 0 else 0

    def GetIMap(self, imgIndex, thresh):
        if len(self.xyzi_data) > 0:
            X = []
            Y = []
            Iy = []
            for i in range(0, len(self.xyzi_data)):
                xyz = self.xyzi_data[i]
                if float(xyz['I'][imgIndex]) > thresh:
                    X.append(xyz['X'])
                    Y.append(xyz['Y'])
                    Iy.append(xyz['I'][imgIndex])
            return X, Y, Iy
        return None

    def GetI3DMap(self, imgIndex, thresh):
        if(self.dataLoaded == True):
            X=[]
            Y=[]
            Z=[]
            I=[]
            zCount = 0
            prevScanNum = 0
            iterIndex = imgIndex + 4
            for i in range(len(self.xyzi_data)) : 
                scanNum = self.xyzi_data.iloc[i, 0]
                if scanNum < prevScanNum:
                    zCount = zCount + 1
                iy = self.xyzi_data.iloc[i, iterIndex]
                if iy > thresh:
                    X.append(self.xyzi_data.iloc[i, 1])
                    Y.append(self.xyzi_data.iloc[i, 2])
                    Z.append(zCount)               
                    I.append(iy)
                prevScanNum = scanNum
                 
            return X,Y,Z,I
        return None 
            
    def PlotImage(self, cmap_name, imgIndex, thresh, alpha):
        lenI = len(self.xyzi_data[0]['I'])
        print(str(lenI) + " intensity points")
        if(imgIndex < lenI):            
            x, y, iy = self.GetIMap(imgIndex, thresh)            
            fig, axes = plt.subplots(1, 1)
            axes.set_facecolor('xkcd:black')
            axes.scatter(x=x, y=y, c=iy, cmap = cmap_name, marker='s', alpha=alpha, s=6)            
            return fig, iy
        else:
            print("Image Index out of range  " + str(imgIndex))
        return None


