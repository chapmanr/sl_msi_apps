import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import json
import os


from msi.msi_image_data import MSIImageData


import plotly.express as px



class MSI2DBrowser:

    def __init__(self):
        self.title = 'msi 2D viewer v0.0.2'
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

    

    def get_alpha(self):
        alpha = 0
        if int(self.aplha_slider) > 0:
            alpha = float(100 / int(self.aplha_slider))
        return alpha

    def check_for_correct_format(self):
        selection = str(self.uploaded_file.name)
        length = len(selection)
        start = length - 5
        if selection[start:length] == ".json":
            return True
        return False

    def LoadData(self):
        self.msiImageData = None
        if self.uploaded_file is not None: 
            if self.check_for_correct_format() == True:
                xyzi_data = self.load_json_data(self.uploaded_file)
                self.msiImageData = MSIImageData() 
                self.msiImageData.LoadCachedData(xyzi_data)   
                return True
        return False


    def PlotData(self):
        if( self.msiImageData is not None):   
            fig, iy = self.msiImageData.PlotImage(str(self.cmap_selectbox), int(self.number), float(self.thresh_slider), self.get_alpha())
            if( fig != None):
                st.write(fig)  
                st.subheader("XiC Data Channel " + str(self.number))
                chart_data = pd.DataFrame(iy,  columns=['xic']) 
                st.area_chart(chart_data)
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


        #self.get_preselected
        self.RenderFileUploader()
        self.RenderSideBarWidgets()
        if self.LoadData() == True:              
            self.PlotData()
        else :
            if self.uploaded_file is not None:
                st.error("Load correct data format e.g. /data/example_2d_data.json")
            else :
                st.error("Load a file first")



if __name__ == "__main__":
    msi2d = MSI2DBrowser()
    msi2d.RenderPage()


    
