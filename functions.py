def get_dimensions(row_list, column_list):
  max_heights = {}
  max_widths = {}
  total_height = 0
  total_width = 0
  for row_index, row in enumerate(row_list):
    max_row_height = 0
    for image in row:
      image_height = image.size[1]
      max_row_height = max(max_row_height, image_height)
    max_heights[row_index] = max_row_height
    total_height += max_row_height
  for column_index, column in enumerate(column_list):
    max_column_width = 0
    for image in column:
      image_width = image.size[0]
      max_column_width = max(image_width, max_column_width)
    max_widths[column_index] = max_column_width
    total_width += max_column_width
  return max_heights, max_widths, total_height, total_width


def load_images_from_folder(folder_path):
  filename_list = sorted(os.listdir(folder_path))
  image_list = [
      Image.open(os.path.join(folder_path, file_name))
      for file_name in filename_list
  ]
  return image_list, filename_list


def label_images(image_list, label_info):
  labeled_images = []
  #variables
  (label_position_ver, label_position_hor, background_on, background_color, x_percent,
   y_percent, font_size, font, font_color) = label_info
  for idx, image in enumerate(image_list):
    x_pos = image.width / 100 * x_percent
    y_pos = image.height / 100 * y_percent
    if background_on==1:
      square_start = (x_percent, y_percent)
      square = Image.new("RGBA", square_size, background_color)
      image.paste(square, square_start)
    letter = chr(ord('a') + idx) + ')'
    draw = ImageDraw.Draw(image)
    draw.text((x_pos, y_pos), letter, font=font, fill=font_color)
    labeled_images.append(image)
  return labeled_images


def drawing_setup(labeled_images, number_of_rows, number_of_columns):
  if number_of_rows <= 0:
    raise ValueError("number_of_rows must be a positive integer")
  images_per_row = len(labeled_images) // number_of_rows
  remain_per_row = len(labeled_images) % number_of_rows
  rows = []
  start_row = 0
  for i in range(number_of_rows):
    end_row = start_row + images_per_row + (1 if i < remain_per_row else 0)
    row = labeled_images[start_row:end_row]
    rows.append(row)
    start_row = end_row
  columns = [[] for _ in range(number_of_columns)]
  for i, filename in enumerate(labeled_images):
    col_index = i % number_of_columns
    columns[col_index].append(filename)
  return rows, columns


#caculating rows or columns
#If row_overflow = 1 then the number of images will not fit without rest into the number of rows given so there will me another column which is not full
#if column_overflow = 1 the number of images will not fit without rest in the number of columns so there is an additional row which is not full
def calc_row_column(filename_list, number_of_rows, number_of_columns):
  row_overflow = 0
  column_overflow = 0
  if number_of_rows > 0 and number_of_columns == 0:
    if len(filename_list) % number_of_rows > 0:
      row_overflow = 1
    number_of_columns = ((len(filename_list) // number_of_rows) + row_overflow)
    st.write(
        f'number of columns set to {number_of_columns} number of rows was given ({number_of_rows})'
    )
  elif number_of_rows == 0 and number_of_columns > 0:
    if len(filename_list) % number_of_columns > 0:
      column_overflow = 1
    number_of_rows = ((len(filename_list) // number_of_columns) +
                      column_overflow)
    st.write(
        f'number of rows set to {number_of_rows} number of columns was given ({number_of_columns}'
    )
  else:
    raise ValueError(
        'One of row_overflow and column_overflow must be 0 the other one an integer >0'
    )
  return number_of_rows, number_of_columns


def arange_images(row_list, max_heights, total_height, total_width, image_background):
  complete_image = Image.new('RGBA', (total_width, total_height), image_background)
  current_y = 0
  for row_index, row in enumerate(row_list):
    current_x = 0
    for col_index, image in enumerate(row):
      complete_image.paste(image, (current_x, current_y))
      current_x += max_widths[col_index]
    current_y += max_heights[row_index]
  return complete_image

def resize(image, reduced_width):
  image_width, image_height=image.size
  scaling_factor=reduced_width/image_width
  reduced_height=int(round(image_height*scaling_factor))
  resized_image=image.resize((reduced_width, reduced_height), Image.LANCZOS)
  return resized_image