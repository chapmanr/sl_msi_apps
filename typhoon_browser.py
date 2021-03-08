
from typhoon_data import TyphoonData
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import json

class TyphoonBrowser:

    def __init__(self):
        self.title = "Typhoon Data Explorer"

    def check_for_correct_format(self):
        selection = str(self.uploaded_file.name)
        length = len(selection)
        start = length - 5
        if selection[start:length] == ".json":
            return True
        return False

    def load_json_data(self, json_data):
        return json.load(json_data)

    def load_json_file(self, data_path):
        print("loading json data")        
        with open(data_path) as json_data:
            return self.load_json_data(json_data)        
        return None

    def LoadData(self):
        self.msiImageData = None
        if self.uploaded_file is not None: 
            if self.check_for_correct_format() == True:               
                self.typhoonData = TyphoonData() 
                data = self.load_json_data(self.uploaded_file)
                self.typhoonData.LoadCachedData(data)
                return True
        return False

    def PlotData(self):
        if( self.typhoonData is not None):   
            pr = self.typhoonData.PlotData(str(self.data_selectbox))
            st_profile_report(pr)            
        else:
            st.write("Null data loaded")   
    
    def RenderFileUploader(self):
        self.uploaded_file = st.sidebar.file_uploader("Upload Files",type=['json','txt', 'csv'])
        self.add_selectbox=None

    def LoadDataHeaders(self):
        return ["Scans"]

    def RenderSideBarWidgets(self):
        self.data_selectbox = st.sidebar.selectbox("Data Extraction", self.LoadDataHeaders())

    def RenderPage(self):
        st.title(self.title)
        self.RenderFileUploader()
        self.RenderSideBarWidgets()
        if self.LoadData() == True:              
            self.PlotData()
        else :
            if self.uploaded_file is not None:
                st.error("Load correct data format e.g. /data/example_typhoon_ms_inst_data.json")
            else :
                st.error("Load a file first")
