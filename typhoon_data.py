import pandas as pd
from pandas_profiling import ProfileReport

import json

class TyphoonData:

    def __init__(self):
        self.pr = None
        self.data = None
        self.scansdf = None

    def LoadCachedData(self, data):
        print("loading typhoon data " + str(type(data)))
        self.data=data

    def PlotData(self, selectedData):
        self.scansdf = pd.DataFrame(self.data[selectedData])
        self.pr = ProfileReport(self.scansdf , explorative=True)
        return self.pr

            #print(df.head())

    

