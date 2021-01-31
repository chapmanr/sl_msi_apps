import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import json

from msi.dir_func import *
from msi.msi_image_data import MSIImageData
from msi.msi_defs import *


DEBUG = True

data_file_url = "datafiles.txt"
if DEBUG == True:
    data_file_url = "testdatafiles.txt"

st.title('msi viewer v0.0.1')

def load_data_urls(filename):
    data_urls = []
    if exists_file(filename):
        f = open(filename, "r")
        for x in f:
            data_urls.append(x.rstrip())
    return data_urls


uploaded_file = st.sidebar.file_uploader("Upload Files",type=['json','txt', 'csv'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

add_selectbox = st.sidebar.selectbox(
    "pre-selected data",
    load_data_urls(data_file_url))


def load_cmaps():
    cmap_labels = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
    return cmap_labels

cmap_selectbox = st.sidebar.selectbox("color mapping", load_cmaps())

number = st.sidebar.number_input('Select XiC', 0, 32)
#threshold = st.sidebar.slider


@st.cache
def load_json_data(json_data):
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

@st.cache
def load_json_file(data_path):
    print("loading json data")        
    with open(data_path) as json_data:
        return load_json_data(json_data)        
    return None

thresh_slider = st.sidebar.slider("Threshold data", 0, 250, 10)
aplha_slider = st.sidebar.slider("Aplha setting", 0, 100, 90)

def get_preselected():
    selection = str(add_selectbox).rstrip()   
    st.write("selection = " + selection)
    length = len(selection)
    start = length - 5  
    if selection[start:length] == ".json":   
        if(exists_file(selection)):
            return selection    
    return None


def get_alpha():
    alpha = 0
    if int(aplha_slider) > 0:
        alpha = float(100 / int(aplha_slider))
    return alpha

def plot_data():
    xyzi_data = None
    msiImageData = MSIImageData()    
    if uploaded_file is None:     
            selection = get_preselected()
            if selection != None:
                xyzi_data = load_json_file(selection)                     
            else:
                st.write("MSI data not found : ")
    else:
        xyzi_data = load_json_data(uploaded_file)

    if( xyzi_data != None):                   
        msiImageData.LoadCachedData(xyzi_data)  
        fig, iy = msiImageData.PlotImage(str(cmap_selectbox), int(number), float(thresh_slider), get_alpha())
        if( fig != None):
            st.write(fig)  
            st.subheader("XiC Data Channel " + str(number))
            chart_data = pd.DataFrame(iy,  columns=['xic']) 
            st.area_chart(chart_data)
        else:
            st.write("Plot data failure")
    else:
        st.write("Null data loaded")   
    

    

plot_data()



    #else:
    #   st.write(add_selectbox + "  this file does not exist")


    
