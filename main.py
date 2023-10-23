import streamlit as st
import pandas as pd
from io import StringIO
import os
from PIL import Image, ImageDraw, ImageFont
import functions as fx
import ui as ui

st.title('App to combine images and plots into one figure')
st.subheader('Developed by Daniel Rockel 2023')

background_color = ui.select_background_color

big_image_output=st.toggle('Export final image in full size (could end up in huge files)')
#st.write(f'{big_image_output}')    


st.divider()


st.divider()


current_dir = os.path.dirname(__file__)

images_dir = os.path.join(current_dir, "images")
os.makedirs(images_dir, exist_ok=True)

uploaded_files = st.file_uploader("Upload Files", type=["jpg", "png", "jpeg", "tif"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        with open(os.path.join(images_dir, file.name), "wb") as f:
            f.write(file.read())
        st.write(f"Saved file: {file.name}")

#Either number_of_rows or number_of_columns must be 0
number_of_rows = 0
number_of_columns = 1
#folder path
folder_path = './images/'

#Labeling
label_position_ver = 0
label_position_hor = 0
background_on=0
background_color = (
    255, 255, 255, 0
)

 #(width, length) in this case in realtion to the font_size
#(0,0,0,255)=black, (255,255,255,255)=white, for everything else check RGBA coloring
x_percent = 0
y_percent = 0
font_size = 60
font = ImageFont.truetype("./fonts/arial.ttf", font_size)
font_color = (0, 0, 0, 255)
square_size = (int(round(font_size * 1.5, 0)), (int(round(font_size * 1.5, 0))))

image_background=(255,255,255,255)
#To scale down final picture (give width in pixels, 7inches at 300dpi is 2100)
reduced_width=1050

#if 1, the program saves the big file without any loss in compression. Might take very long.
non_reduced_image=0

label_info = (label_position_ver, label_position_hor, background_on, background_color,
                x_percent, y_percent, font_size, font, font_color, square_size)
len_label_info = len(label_info)

############################################
#### No more editing beyond this point #####
############################################

### Functions




############################################
########### Main programm start ############
############################################

#Getting list of image names

if st.button('Build figure'):
    st.write("Loading images...")
    image_list, filename_list = fx.load_images_from_folder(folder_path)

    st.write('Calculating rows and columns...')
    length = len(filename_list)
    st.write(f'Found {length} images in the folder')

    number_of_rows, number_of_columns = fx.calc_row_column(filename_list,
                                                        number_of_rows,
                                                        number_of_columns)


    st.write(
        f'label_info contains the following information {label_info} which is a length of {len_label_info}'
    )
    labeled_images = fx.label_images(image_list, label_info)
    row_list, column_list = fx.drawing_setup(labeled_images, number_of_rows,
                                        number_of_columns)
    #st.write(f'ROWS ARE: {row_list}')
    #st.write(f'COLOUMNS ARE: {column_list}')
    max_heights, max_widths, total_height, total_width = fx.get_dimensions(
        row_list, column_list)
    final_image = fx.arange_images(row_list, max_heights, max_widths, total_height, total_width, image_background)
    st.write('final image arranged...')
    st.write('creating reduced image...')
    small_image=fx.resize(final_image, reduced_width)
    small_image.save('small_image.tif')
    st.write('saved reduced image...')
    if non_reduced_image==1:
        st.write('saving original image')
        final_image.save('final_image.tif')
        st.write('file saved with orignal size')
    st.write("run complete!")

with open("small_image.tif", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="small_image.tif",
            mime="image/tif"
          )