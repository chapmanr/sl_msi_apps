import streamlit as st
import numpy as np


known_pages={}

def paginator(label, items, items_per_page=10, on_sidebar=True):
    
    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1#//is the floor function
    key_list = list(known_pages.keys())
    page_format_func = lambda i: str(key_list[i])
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)



from msi_browser import MSI2DBrowser
from msi_3d_browser import MSI3DBrowser
from msi_umap_browser import MSIUmapBrowser
from typhoon_browser import TyphoonBrowser
from msi_analyte_browser import MSIAnalyteBrowser

def load_known_pages():
    known_pages["2D Imaging"]     = MSI2DBrowser()
    known_pages["3D Imaging"]     = MSI3DBrowser()   
    known_pages["UMAP Imaging"]   = MSIUmapBrowser()
    known_pages["MaldiChrom Browser"] = MSIAnalyteBrowser()
    known_pages["Typhoon Data Browser"]    = TyphoonBrowser()
    return known_pages.keys()

def get_page_renderer(page_key):
    return known_pages[page_key]
  

def render_pages(pages_to_render):
    for apage in pages_to_render:
        get_page_renderer(apage).RenderPage()

def main_page():
    page_list = load_known_pages()
    page_list_to_render = []
    for i, apage in paginator("Select Processing Page", page_list, items_per_page=1,on_sidebar=True):
        page_list_to_render.append(apage)
    render_pages(page_list_to_render)

if __name__ == '__main__':
    main_page()


