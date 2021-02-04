import streamlit as st
import numpy as np
import pandas as pd
import json

from msi.dir_func import *
from msi.msi_image_data import MSIImageData
from msi.msi_defs import *


@st.cache
def load_json_data(json_data):
    print(f"loading json data {json_data}")
    return json.load(json_data)


@st.cache
def load_json_file(data_path):
    print(f"loading json file {data_path}")
    with open(data_path) as json_data:
        return load_json_data(json_data)


def load_data_urls(filename):
    data_urls = []
    if exists_file(filename):
        f = open(filename, "r")
        for x in f:
            data_urls.append(x.rstrip())
    return data_urls


st.title('msi viewer v0.0.1')

uploaded_file = st.sidebar.file_uploader(
    "Upload Files", type=['json', 'txt', 'csv'])

file_selectbox = st.sidebar.selectbox(
    "pre-selected data", load_data_urls('testdatafiles.txt'))

cmap_selectbox = st.sidebar.selectbox(
    "color mapping", ['viridis', 'plasma', 'inferno', 'magma', 'cividis'])

xic_number = st.sidebar.number_input('Select XiC', 0, 32)
thresh_slider = st.sidebar.slider("Threshold data", 0, 250, 10)
aplha_slider = st.sidebar.slider("Aplha setting", 0, 100, 90)


def get_preselected():
    selection = str(file_selectbox).strip()
    if selection is not None and selection.endswith('.json') and exists_file(selection):
        return selection


def get_alpha():
    return 100.0 / int(aplha_slider) if int(aplha_slider) > 0 else 0.0


def plot_data():
    xyzi_data = None
    msiImageData = MSIImageData()
    if uploaded_file:
        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type,
                        "FileSize": uploaded_file.size}
        st.write(file_details)
        xyzi_data = load_json_data(uploaded_file)
    else:
        selection = get_preselected()
        if selection:
            st.write('Selection: ' + selection)
            xyzi_data = load_json_file(selection)
        else:
            st.write("MSI data not found")

    if xyzi_data:
        msiImageData.LoadCachedData(xyzi_data)
        fig, iy = msiImageData.PlotImage(
            str(cmap_selectbox),
            int(xic_number),
            float(thresh_slider),
            get_alpha())
        if fig:
            st.write(fig)
            st.subheader("XiC Data Channel " + str(xic_number))
            chart_data = pd.DataFrame(iy,  columns=['xic'])
            st.area_chart(chart_data)
        else:
            st.write("Plot data failure")
    else:
        st.write("Null data loaded")


plot_data()
