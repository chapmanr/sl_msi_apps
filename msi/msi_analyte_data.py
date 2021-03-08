import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class MSIAnalyteData:

    def LoadCachedData(self, mz, data):
        self.mz = mz
        self.data = data
        self.Xpixels    = self.data[1].tolist()
        self.Ypixels    = self.data[2].tolist()

        last       = self.data.columns[-1]
        print("last =" + str(last))
        self.data       = self.data.drop(self.data.columns[[0, 1, 2,last-1,last]], axis=1)
        self.ScanNum    = self.data.index.tolist()
        self.TotalScans  = len(self.ScanNum)

        
        self.mzlabs         = self.mz.loc[0,:].values.tolist()
        self.data.columns   = self.mzlabs
        self.data           = self.data.reindex(sorted(self.data.columns), axis=1)
        self.mzlabs.sort()
        self.numPeaks       = len(self.mzlabs)

        return self.mzlabs, self.data

    def PlotImage(self, cmap_name, alpha):
        x = self.Xpixels
        y = self.Ypixels        
        fig, axes = plt.subplots(3, 3)# figsize=(15, 5))
        print(str(axes.shape))


        fig.suptitle('2D Imaging using maldichrom data and seaborn')

        for col in range(0,3):
            for row in range(0,3):
                indx = (col * 3) + row
                print("index " + str(indx))
                mdata = self.data.iloc[ : , indx + 1]
                ax = axes[row, col]
                #sns_axes = sns.scatterplot(ax=ax, x=x, y=y, hue=mdata, palette='viridis', marker='s', alpha=alpha, s=6, legend=False)
                #fig.set_facecolor('xkcd:black')
                ax.scatter(x=x, y=y, c=mdata, cmap = cmap_name, marker='s', alpha=alpha, s=6)    
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)

        #sns.set_theme(style="whitegrid")

        plt.axis('off')
        return fig