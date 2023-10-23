import streamlit as st

background_color_radio = st.radio(
        "Background of labels",
        ["transparent", "black", "white"]
    )
if background_color_radio == 'transparent':
    background_color= (0, 0, 0, 0)
elif background_color_radio == 'black':
    background_color= (0, 0, 0, 255)
elif background_color_radio == 'white':
    background_color= (255, 255, 255, 255)