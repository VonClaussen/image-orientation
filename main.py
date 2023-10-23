import streamlit as st
import pandas as pd
from io import StringIO
import os
from PIL import Image, ImageDraw, ImageFont
import functions as fx


st.title('App to combine images and plots into one figure')
st.subheader('Developed by Daniel Rockel 2023')

background_color_options = {
    "transparent": (0, 0, 0, 0),
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255)
}

background_color_radio = st.radio(
    "Color of the figure background",
    list(background_color_options.keys())
)

background_color = background_color_options.get(background_color_radio, (0, 0, 0, 0))

label_color_options = {
    "transparent": (0, 0, 0, 0),
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255)
}

label_color_radio = st.radio(
    "Color of the label",
    list(label_color_options.keys())
)
label_color = label_color_options.get(label_color_radio, (0, 0, 0, 0))  

font_size = int(round(st.number_input('Insert the font size (1-200)', step=1, value=60, min_value=1, max_value=200)))

label_scaling=st.radio('Choose if the label size is determined absolute by a number of pixels or relative to the font size', ["Relative to the font size (recomended)","Absolute by pixels"])
if label_scaling.startswith('Absolute'):
    label_size_x=int(round(st.number_input('Size in X direction', step=1, value=120, min_value=1, max_value=1000)))
    label_size_y=int(round(st.number_input('Size in Y direction', step=1, value=120, min_value=1, max_value=1000)))
elif label_scaling.startswith('Relative'):
    label_relative_x=st.number_input('Scaling in X direction (1 equals the font size)', step=0.01, value=1.5, min_value=0.01, max_value=10.0)
    label_relative_y=st.number_input('Scaling in Y direction (1 equals the font size, 1.5 recomended)', step=0.01, value=1.5, min_value=0.01, max_value=10.0)
    label_size_x=font_size*label_relative_x
    label_size_y=font_size*label_relative_y

x_percent = int(round(st.number_input('Insert the shift of the label in X-direction in percent (0-100)', step=1, value=0, min_value=0, max_value=100)))
y_percent = int(round(st.number_input('Insert the shift of the label in Y-direction in percent (0-100)', step=1, value=0, min_value=0, max_value=100)))

font_color_options = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255)
}

font_color_radio = st.radio(
    "Color of the font in the label",
    list(font_color_options.keys())
)

font_color = font_color_options.get(font_color_radio, (0, 0, 0, 255))

flag_block_rows=0
flag_block_columns=1

row_column_switch=st.radio('Decide if the layout is calculated from rows or columns', ['row','column'])

if row_column_switch=='row':
    flag_block_rows=0
    flag_block_columns=1
    number_of_rows = int(round(st.number_input('Number of Rows', step=1, value=1, min_value=0, max_value=100, disabled=flag_block_rows)))
    number_of_columns = 0
elif row_column_switch=='column':
    flag_block_rows=1
    flag_block_columns=0
    number_of_columns = int(round(st.number_input('Number of Columns', step=1, value=0, min_value=0, max_value=100, disabled=flag_block_columns)))
    number_of_rows=0

radio_letter_shift=st.toggle('Shift letters in the label without shifting the label background')
if radio_letter_shift==True:
    letter_shift_x = int(round(st.number_input('Shift letter in x direction', step=1, value=0, min_value=0, max_value=100)))
    letter_shift_y = int(round(st.number_input('shift letter in y direction', step=1, value=0, min_value=0, max_value=100)))
else:
    letter_shift_x=0
    letter_shift_y=0

input_reduced_width=st.number_input('Determine the width of your figure output in inches (3.5 or 7 recomended for publications, 300dpi is chosen)', step=0.1, value=3.5, min_value=0.1, max_value=14.0)
reduced_width=int(round(300*input_reduced_width))


non_reduced_output=st.toggle('Export final image in full size (could end up in huge files)')



st.divider()

st.write(f'Background color: {background_color_radio}{background_color}')
st.write(f'Label color: {label_color_radio}{label_color}')
if background_color!=(0,0,0,0):
    st.write('Background is not transparent')
st.write(f'Font size is ', font_size)
st.write('X-Shift of label is:', x_percent)
st.write('Y-Shift of label is:', y_percent)
if radio_letter_shift==False:
    st.write('Letter in the label is not shifted')
else:
    st.write(f'Letter in the label is shifted by {letter_shift_x} in X direction and {letter_shift_y} in Y direction')
if row_column_switch=='row':
    st.write('Number of rows set to', number_of_rows)
    st.write('Number of columns will be calculated')
elif row_column_switch=='column':
    st.write('Number of columns set to', number_of_columns)
    st.write('Number of columns will be calculated')
st.write('figure is scaled to width of', reduced_width,'pixels')



font = ImageFont.truetype("./fonts/arial.ttf", font_size)

label_size = (int(round(label_size_x)), int(round(label_size_y)))

#To scale down final picture (give width in pixels, 7inches at 300dpi is 2100)


label_info = (letter_shift_x, letter_shift_y, background_color, label_color,
                x_percent, y_percent, font, font_color, label_size)

len_label_info = len(label_info)



if non_reduced_output==1:
  st.write('CAREFUL you are exporting the image in full size which could end up in very big files')

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

#folder path
folder_path = './images/'


############################################
#### No more editing beyond this point #####
############################################






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
    final_image = fx.arange_images(row_list, max_heights, max_widths, total_height, total_width, background_color)
    st.write('final image arranged...')
    st.write('creating reduced image...')
    small_image=fx.resize(final_image, reduced_width)
    small_image.save('small_image.tif')
    st.write('saved reduced image...')
    if non_reduced_output==1:
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