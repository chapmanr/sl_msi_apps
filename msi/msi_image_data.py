import json
import matplotlib.pyplot as plt
import numpy as np

class MSIImageData:
    def __init__(self):
        self.xyzi_data = []

    def LoadData(self, json_filename):
        with open(json_filename) as json_data:
            self.xyzi_data.extend(json.load(json_data))

    def LoadCachedData(self, cachedData):
        self.xyzi_data.extend(cachedData)

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

    def PlotImage(self, cmap_name, imgIndex, thresh, alpha):
        if len(self.xyzi_data) > 0:
            print(f"{len(self.xyzi_data)} xyz points")
            lenI = len(self.xyzi_data[0]['I'])
            print(f"{lenI} intensity points")
            if imgIndex < lenI:
                x, y, iy = self.GetIMap(imgIndex, thresh)
                fig, axes = plt.subplots(1, 1)
                axes.set_facecolor('xkcd:black')
                axes.scatter(x=x, y=y, c=iy, cmap=cmap_name,
                             marker='s', alpha=alpha)
                return fig, iy
            else:
                print(f"Image Index out of range {imgIndex}")
        return None


if(__name__ == "__main__"):
    datapath = "data/example_data.json"
    # datapath=filedialog.askopenfilename()
    if datapath:
        msiImg = MSIImageData()
        msiImg.LoadData(datapath)
        print(str(len(msiImg.XYZArray())))