
import plotly.express as px
import pandas as pd
import json

class MSI3DImageData:

    def LoadData(self, filename):
        print("loading data")    

        length = len(filename)
        start = length - 4 
        if filename[start:length] == ".csv":  
            #if(exists_file(filename)):
            print("loading 3D data") 
            self.LoadCachedData(pd.read_csv(filename))
        else:
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

    def PlotImage(self, imgIndex, thresh, alpha):        
        if self.dataLoaded == True:
            df = self.xyzi_data
            strImageIndex = "m" + str(imgIndex + 1)
            if strImageIndex in df.columns:
                todrop = df[df[strImageIndex]<thresh].index
                df.drop(todrop,inplace=True)                
                fig = px.scatter_3d(df, x='x', y='y', z='z', color='m1', opacity=alpha)        
                return fig
            else:
                print("Image Index out of range  " + str(imgIndex))
        else:
            print("Data not loaded")
        return None
