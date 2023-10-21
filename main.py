import streamlit as st
import pandas as pd
from io import StringIO
import os
from PIL import Image, ImageDraw, ImageFont
import functions as fx

st.title('App to combine images and plots into one figure')
st.subheader('Developed by Daniel Rockel 2023')

background_color = None

background_color_radio = st.radio(
    "Background of labels",
    ["transparent", "black", "white"]
)

big_image_output=st.toggle('Export final image in full size (could end up in huge files)')
#st.write(f'{big_image_output}')    

if background_color_radio == 'transparent':
    background_color = (0,0,0,0)
    st.write(f'Selected Background is {background_color}')
    flag_background_color=0
elif background_color_radio == 'black':
    background_color = (0,0,0,255)
    st.write(f'Selected Background is {background_color}')
elif background_color_radio == 'white':
    background_color = (255,255,255,255)
    st.write(f'Selected Background is {background_color}')
else:
    flag_background_color=1


st.divider()

if flag_background_color==1:
    st.write('Fill in background color')

st.divider()

uploaded_files = st.file_uploader("Upload Files", type=["jpg", "png", "jpeg", "tif"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        with open(os.path.join("images", file.name), "wb") as f:
            f.write(file.read())
        st.write(f"Saved file: {file.name}")