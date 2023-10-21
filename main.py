import streamlit as st

st.write('Hello, *World!* :sunglasses:')

background_color_radio = st.radio(
    "Background of labels",
    ["transparent", "black", "white"]
)
    
background_color = None

if background_color_radio == 'transparent':
    background_color = (0,0,0,0)
    st.write(f'Selected Background is {background_color}')
elif background_color_radio == 'black':
    background_color = (0,0,0,255)
    st.write(f'Selected Background is {background_color}')
elif background_color_radio == 'white':
    background_color = (255,255,255,255)
    st.write(f'Selected Background is {background_color}')
else:
    st.write('Please select background color')