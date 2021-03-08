import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import json
import os


from msi.msi_analyte_data import MSIAnalyteData


class MSIAnalyteBrowser:

    def __init__(self):
        self.title = 'msi Analyte browser v0.0.2'
        self.data_file_url = "datafiles.txt"
        
   
    
    def load_cmaps(self):
        cmap_labels = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        return cmap_labels
    
    def load_json_data(self, json_data):
        jdata = json.load(json_data)
        xyzi_data = []
        for item in jdata:
            xyz = {"X":None, "Y":None, "Z":None, "I":None}
            xyz['X'] = item['X']
            xyz['Y'] = item['Y']
            xyz['Z'] = item['Z']
            xyz['I'] = item['I']
            xyzi_data.append(xyz)
        return xyzi_data

    def load_json_file(self, data_path):
        print("loading json data")        
        with open(data_path) as json_data:
            return self.load_json_data(json_data)        
        return None

    def select_dataset_file(self):
        dataset_dir = './data'
        filenames = os.listdir(dataset_dir)
        # dropdown menu displaying all the files in dataset directory
        selected_dataset = st.selectbox("",filenames)
        return os.path.join(dataset_dir, selected_dataset)

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
                self.msiAnalyte = MSIAnalyteData()
                self.msiAnalyte.LoadCachedData(mz, data)   
                return True
        return False


    def PlotData(self):
        if( self.msiAnalyte is not None):   
            fig = self.msiAnalyte.PlotImage(str(self.cmap_selectbox), self.get_alpha())            
            if( fig != None):
                st.pyplot(fig)                   
            else:
                st.write("Plot data failure")
        else:
            st.write("Null data loaded")   
    
    def RenderFileUploader(self):
        self.uploaded_file = st.sidebar.file_uploader("Upload Files",type=['json','txt', 'csv'])
        self.add_selectbox=None
        
                       
    def RenderCommonSideBarWidgets(self):        
        #threshold = st.sidebar.slider        
        self.aplha_slider = st.sidebar.slider("Opacity setting", 0, 100, 90)


    def RenderSideBarWidgets(self):        
        self.cmap_selectbox = st.sidebar.selectbox("color mapping", self.load_cmaps())
        self.RenderCommonSideBarWidgets()


    def RenderPage(self):
        st.title(self.title)
        #self.get_preselected()
        self.RenderFileUploader()
        self.RenderSideBarWidgets()
        if self.LoadData() == True:              
            self.PlotData()
        else :
            if self.uploaded_file is not None:
                st.error("Load correct data format e.g. /data/example_2d_data.json")
            else :
                st.error("Load a file first")



    
