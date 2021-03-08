
import pandas as pd

import numpy as np
from sklearn.decomposition import PCA
import umap.umap_ as umap
import matplotlib.pyplot as plt

class MSIUMapData:

    def LoadCachedData(self, mz, data):
        self.mz = mz
        self.data = data
        self.Xpixels    = self.data[1].tolist()
        self.Ypixels    = self.data[2].tolist()
        
        last       = self.data.columns[-1]
        self.data       = self.data.drop(self.data.columns[[0, 1, 2,last-1,last]], axis=1)
        self.ScanNum    = self.data.index.tolist()
        self.TotalScan  = len(self.ScanNum)
        
        self.mzlabs     = self.mz.loc[0,:].values.tolist()
        self.data.columns=self.mzlabs
        self.data = self.data.reindex(sorted(self.data.columns), axis=1)
        self.mzlabs.sort()
        self.peakNum=len(self.mzlabs)

        # Work out pixel dimensions- need to do try/ catch here 
        a=self.Xpixels[1]
        self.Ypix=self.Xpixels.count(a)

        self.Xpix=np.round(self.TotalScan/self.Ypix)

        print(self.Ypix)
        print(self.Xpix)
        self.CleanDataBackgroundLipid()


    def CleanDataBackgroundLipid(self):
        #data_new = self.data.div(self.data.sum(axis=1), axis=0)

        # This is a crude method for clearing background pixels based on lipid vs non-lipid 

        low1=int(self.peakNum/10)
        low2=int(self.peakNum/2)
        high2=int(self.peakNum)
        D1=self.data.iloc[:,0:low1]
        D2=self.data.iloc[:,low2:high2]
        D1s = D1.sum(axis=1)
        D2s = D2.sum(axis=1)

        Ratio=D2s/D1s
        Ratio.tolist()


        # This may be possible to do with only one copy of the data 
        data2=self.data
        data2.loc[Ratio<3,:]=0
        self.data3=data2.loc[~(data2==0).all(axis=1)]
        self.clean_data = self.data3.div(self.data3.sum(axis=1), axis=0)
        self.clean_data =self.clean_data.fillna(0)


    def PCAReduce(self):
        # Do PCA data reduction 
        self.reduced_data=PCA(n_components=10).fit_transform(self.clean_data)

        # Perform the UMAP - these paramaters will be adjustable
        #use UMAP as a drop in replacement for t-SNE and other dimension reduction classes
        reducer     = umap.UMAP(n_neighbors=10,min_dist=0.1,n_components=2,metric='euclidean')
        embedding   = reducer.fit_transform(self.reduced_data)
        print(embedding.shape)

        #plt.scatter(embedding[:, 0], embedding[:, 1])
        #plt.savefig("kidney.jpg")
        return embedding


    #def 

    def PlotImage(self, cmap_name, imgIndex, thresh, alpha):
        embedding = self.PCAReduce()
        x2 = embedding[:, 0]
        y2 = embedding[:, 1] 

        YY=int(self.Ypix)
        XX=int(self.Xpix)

        CX=[]
        for y in range(YY):
            for x in range(XX):
                CX.append(x)
            
        CY=[]

        for y in range(YY):
            for x in range(XX):
                CY.append(y)
            
            
            
        idx=self.data3.index

        CX2 = [CX[i] for i in idx]
        CY2 = [CY[i] for i in idx]

        
        #minimum removed from the array
        x3 = x2-np.min(x2)
        y3 = y2-np.min(y2)

        #scan number stuff
        scannum= np.arange(0,self.TotalScan).tolist()
        spectra=scannum

        spectra2 = [spectra[i] for i in idx]

        #scaling of the values in the reduced data -> 255 
        ColX=(x3/np.max(x3))*255
        ColY=(y3/np.max(y3))*255

        CV1 = ["#%02x%02x%02x" % (int(r), int(g), 0) for r, g in zip(ColX, ColY)]
        CV2 = ["#%02x%02x%02x" % (0, int(r), int(g)) for r, g in zip(ColX, ColY)]
        CV3 = ["#%02x%02x%02x" % (int(r), 0, int(g)) for r, g in zip(ColX, ColY)]


        #Data Sources:
        Mean1=np.mean(self.data3) #.iloc[1,:] 

        Blank=[0]*len(CX2)
        BlankMap = ["#%02x%02x%02x" % (0, 0, 0) for r in(ColX)]

        CompData=Mean1/Mean1
        Ssource = dict(x=self.mzlabs,y=Mean1)
        
        Dsource = dict(x=x2, y=y2, cordsX=CX2,cordsY=CY2,CV=CV1,spectra=spectra2)

        Csource = dict(x=self.mzlabs,Region1=Mean1,Region2=Mean1,y=CompData)
        Isource = dict(cordsX=CX2,cordsY=CY2,Region1=Blank,Region2=Blank,Map=Blank)
        

        fig, (ax1, ax2) = plt.subplots(1, 2)

        #fig, ax = plt.subplots()

        ax1.scatter(x=x2,y=y2,c=CV1)
        #cordsX=CX2,cordsY=CY2
        ax2.scatter(x=CX2, y=CY2, c=CV1)
        return fig
        
