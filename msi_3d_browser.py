import streamlit as st

import numpy as np
import pandas as pd
import json

from msi.msi_3d_image_data import MSI3DImageData
from msi_browser import MSI2DBrowser

class MSI3DBrowser(MSI2DBrowser):



    def load_csv_file(self, data_path):
        print("loading csv data")
        return pd.read_csv(data_path)    

    def check_for_correct_format(self):
        selection = str(self.uploaded_file.name)
        length = len(selection)
        start = length - 4
        if selection[start:length] == ".csv":
            return True
        return False

    def LoadData(self):
        self.msiImageData = None
        if self.uploaded_file is not None: 
            if self.check_for_correct_format() == True:
                xyzi_data = self.load_csv_file(self.uploaded_file)  
                if(xyzi_data.empty == False):
                    self.msiImageData = MSI3DImageData()             
                    self.msiImageData.LoadCachedData(xyzi_data)  
                    return True              
                else:
                    st.error("Null data loaded")     
                            #st.write(selection + " selected")  
            else:
                st.error("Load 3d CSV file")                              
        else:
            st.error("MSI data not found : ")
        return False

    def PlotData(self):
        if self.msiImageData is not None:
            alpha = 1
            if int(self.aplha_slider) > 0:
                print("slider = " + str(self.aplha_slider))
                alpha = float( int(self.aplha_slider) / 100)
            fig = self.msiImageData.PlotImage(int(self.number), float(self.thresh_slider), alpha)
            if( fig != None):
                st.plotly_chart(fig) 
                st.subheader("XiC Data Channel " + str(self.number))
                
            else:
                st.error("Plot data failure")

    def RenderSideBarWidgets(self):        
        self.RenderCommonSideBarWidgets()

    def RenderPage(self):
        self.title = 'msi 3d viewer v0.0.2'
        st.title(self.title)
        self.RenderFileUploader()
        self.RenderSideBarWidgets()
        self.LoadData()
        self.PlotData()
        
                
        