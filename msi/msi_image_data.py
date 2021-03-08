import json
import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt


class MSIImageData:

    def __init__(self):
        self.dataLoaded = False          

    
    def LoadData(self, filename):
        print("loading data")    
        length = len(filename)
        start = length - 5
        if filename[start:length] == ".json":   
            print("loading json data")
        #    if(exists_file(filename)):
            with open(filename) as json_data:
                self.jdata = json.load(json_data)
                self.xyzi_data = []
                for item in self.jdata:
                    xyz = {"X":None, "Y":None, "Z":None, "I":None}
                    xyz['X'] = item['X']
                    xyz['Y'] = item['Y']
                    xyz['Z'] = item['Z']
                    xyz['I'] = item['I']
                    self.xyzi_data.append(xyz)
                print("loading json data")
                self.LoadCachedData(self.xyzi_data)
            return len(self.xyzi_data)
        return 0

    def LoadCachedData(self, cachedData):
        self.xyzi_data = cachedData
        self.dataLoaded = True

    def XYZArray(self):
        return self.xyzi_data
    
    def NumImages(self):
        if(self.dataLoaded == True):
            return len(self.xyzi_data[0]['I'])  
        return 0
   

    def GetIMap(self, imgIndex, thresh):
        if(self.dataLoaded == True):
            X = []
            Y = []
            Iy = []
            for i in range(0, len(self.xyzi_data)):
                xyz = self.xyzi_data[i]                
                if(float(xyz['I'][imgIndex]) > thresh):
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


import tkinter.filedialog

def ToPDDF(X, Y, Z):
    d = {'X': X, 'Y': Y, 'Z' : Z}
    return pd.DataFrame(data = d, index=None)

if(__name__ == "__main__"):
    #datapath = "../data/3D_mouse_area1_001.raw.json"
    datapath=tkinter.filedialog.askopenfilename()
    if(datapath!=""):
        msiImg = MSIImageData()
        msiImg.LoadData(datapath)
        print("Got XYZ pts " + str(len(msiImg.XYZArray())))
        X, Y, Z, I = msiImg.GetI3DMap(0, 0)        

        #normalize everything for now
        nX = (X-min(X))/(max(X)-min(X))
        nY = (Y-min(Y))/(max(Y)-min(Y))

        norm = np.linalg.norm(Z)
        nZ   = Z/norm

        #nZ = (Z-min(Z))/(max(Z)-min(Z))

        pcd = ToPDDF(nX, nY, nZ)        
        pcd.to_csv(datapath + ".txt", index=None, sep=' ')
        #o3d.visualization.draw_geometries([pcd],zoom=0.3412,
        #                          front=[0.4257, -0.2125, -0.8795],
        #                          lookat=[2.6172, 2.0475, 1.532],
        #                          up=[-0.0694, -0.9768, 0.2024])

