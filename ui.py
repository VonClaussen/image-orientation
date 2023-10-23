import streamlit as st
import pandas as pd
from io import StringIO
import os
from PIL import Image, ImageDraw, ImageFont
import functions as fx
import ui as ui

def select_background_color():
    background_color_radio = st.radio(
        "Background of labels",
        ["transparent", "black", "white"]
    )
    if background_color_radio == 'transparent':
        return (0, 0, 0, 0)
    elif background_color_radio == 'black':
        return (0, 0, 0, 255)
    elif background_color_radio == 'white':
        return (255, 255, 255, 255)