

import streamlit as st

import numpy as np
import pandas as pd
import json

from msi.umap_data import MSIUMapData
from msi_browser import MSI2DBrowser

import plotly.express as px

class MSIUmapBrowser:

    def __init__(self):
        self.title = 'msi UMAP viewer v0.0.2'
        
 
    def load_cmaps(self):
        cmap_labels = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        return cmap_labels
    
    

    

    def get_preselected(self):
        if self.add_selectbox is not None:
            selection = str(self.add_selectbox).rstrip()   
            st.write("selection = " + selection)
            length = len(selection)
            start = length - 4  
            if selection[start:length] == ".txt":   
                return selection    
        return None

    def get_alpha(self):
        alpha = 0
        if int(self.aplha_slider) > 0:
            alpha = float(100 / int(self.aplha_slider))
        return alpha

    def check_for_correct_format(self):
        selection = str(self.uploaded_file.name)
        length = len(selection)
        start = length - 4
        print("analyte filename = " + selection)
        if selection[start:length] == ".txt":
            return True
        return False

    def load_analyte_file(self, datapath):
        print("loading analyte data")        
        mz         = pd.read_csv(datapath, sep='\t', skiprows=(0,1,2),header=None, nrows=1)    
        mz         = mz.drop(columns=[0,1,2])
        data       = pd.read_csv(datapath, sep='\t', skiprows=(0,1,2,3),header=None)
        return mz, data

    def LoadData(self):
        self.msiImageData = None
        if self.uploaded_file is not None: 
            if self.check_for_correct_format() == True:
                mz, data = self.load_analyte_file(self.uploaded_file)
                self.msiImageData = MSIUMapData() 
                self.msiImageData.LoadCachedData(mz, data)   
                return True
        return False


    def PlotData(self):
        if( self.msiImageData is not None):   
            fig = self.msiImageData.PlotImage(str(self.cmap_selectbox), int(self.number), float(self.thresh_slider), self.get_alpha())
            if( fig != None):
                st.write(fig)  
                #st.subheader("XiC Data Channel " + str(self.number))
                #chart_data = pd.DataFrame(iy,  columns=['xic']) 
                #st.area_chart(chart_data)
            else:
                st.write("Plot data failure")
        else:
            st.write("Null data loaded")   
    
    def RenderFileUploader(self):
        self.uploaded_file = st.sidebar.file_uploader("Upload Files",type=['json','txt', 'csv'])
        self.add_selectbox=None        
                       
    def RenderCommonSideBarWidgets(self):
        self.number = st.sidebar.number_input('Select XiC', 0, 32)
        #threshold = st.sidebar.slider
        self.thresh_slider = st.sidebar.slider("Threshold data", 0, 100, 10)
        self.aplha_slider = st.sidebar.slider("Opacity setting", 0, 100, 90)


    def RenderSideBarWidgets(self):        
        self.cmap_selectbox = st.sidebar.selectbox("color mapping", self.load_cmaps())
        self.RenderCommonSideBarWidgets()


    def RenderPage(self):
        st.title(self.title)
        self.RenderFileUploader()
        self.RenderSideBarWidgets()
        if self.LoadData() == True:              
            self.PlotData()
        else :
            if self.uploaded_file is not None:
                st.error("Load correct data format e.g. /data/example_analyte 1_13.txt")
            else :
                st.error("Load a file first")


