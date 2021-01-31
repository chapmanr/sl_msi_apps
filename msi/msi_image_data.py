import json

import matplotlib.pyplot as plt 
import numpy as np 


class MSIImageData:

    def __init__(self):
        self.dataLoaded = False            
    
    def LoadData(self, json_filename):
        print("loading json data")        
        with open(json_filename) as json_data:
            self.jdata = json.load(json_data)
            self.xyzi_data = []
            for item in self.jdata:
                xyz = {"X":None, "Y":None, "Z":None, "I":None}
                xyz['X'] = item['X']
                xyz['Y'] = item['Y']
                xyz['Z'] = item['Z']
                xyz['I'] = item['I']
                self.xyzi_data.append(xyz)
            self.dataLoaded = True
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


    def PlotImage(self, cmap_name, imgIndex, thresh, alpha):
        if(self.dataLoaded == True):
            lenPoints = len(self.xyzi_data)
            if lenPoints > 0:
                print(str(lenPoints) + " xyz points")
                lenI = len(self.xyzi_data[0]['I'])
                print(str(lenI) + " intensity points")
                if(imgIndex < lenI):            
                    x, y, iy = self.GetIMap(imgIndex, thresh)            
                    fig, axes = plt.subplots(1, 1)
                    axes.set_facecolor('xkcd:black')
                    axes.scatter(x=x, y=y, c=iy, cmap = cmap_name, marker='s', alpha=alpha)            
                    return fig, iy
                else:
                    print("Image Index out of range  " + str(imgIndex))
        return None

if(__name__ == "__main__"):
    datapath = "../data/3D_mouse_area1_001.raw.json"
    #datapath=filedialog.askopenfilename()
    if(datapath!=""):
        msiImg = MSIImageData()
        msiImg.LoadData(datapath)
        print(str(len(msiImg.XYZArray())))