# Copyright 2026 MrBabay1664
# Author https://github.com/MrBabay1664
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import png
import random
import subprocess


color_limit = 255


# Show image to kitty terminal
def show_image(image_bytes: bytes):
    subprocess.run(["kitty", "+kitten", "icat"], input=image_bytes)


# Convert G color value to color multiplier
def g_to_multiplier(g: int):
    if g is 0:
        return 1
    elif g is 1:
        return 2
    else:
        return (g-1) / 10 + 2

# Convert multiplier to G color value
def multiplier_to_g(multiplier: int):
    if multiplier is 1:
        return 0
    elif multiplier is 2:
        return 1
    else:
        return (multiplier-2) * 10


# Convert text bytes to image color values
def convert_bytes_to_image(bytes_text: bytes) -> list[tuple[int, int, int]]:

    i = 0
    image_data = []

    for by in bytes_text:
        r = g = b = 0 # Reset color values
        r = by # Setting R to byte code

        # If R is bigger, than color limit
        while r > color_limit:
            g += 1 # Multiply this
            r = int(by / g_to_multiplier(g))

        b = by - (r * g_to_multiplier(g)) # Division remainder

        # Paint this
        #if g is 0 and (i % 2 is 0):
        #    b = r
        #    r = 0
        #    if i % 4:
        #        g = color_limit - b

        # Append colors
        image_data.append((r, g, b))

        i += 1

    return image_data


# Convert image data to bytes
def convert_image_to_bytes(image_data: list[tuple[int, int, int]]) -> bytes:
    result_text = []
    errors = False

    for colors in image_data:
        # Get colors
        r = colors[0]
        g = colors[1]
        b = colors[2]

        # Calculate byte
        byte = int(r*g_to_multiplier(g)) + b

        #if byte not in range(0, 256):
        if not (0 <= byte <= 255):
            errors = True
            continue

        result_text.append( byte )

    if errors:
        print("⚠️ Warning: image has invalid bytes!")

    # Convert to bytes type
    result_text = bytes(result_text)

    return result_text


# Convert image data to PyPNG array
def convert_image_data_to_png_array(image_data: list[tuple[int, int, int]], width: int, height: int) -> tuple[list[list[int]], int, int]:
    result = [[]]
    
    #i = 0
    for colors in image_data:
        # If array size is bigger, than width, add new line
        if len(result[-1]) >= (width*3):
            result.append([])

        # Extend line with colors
        result[-1].extend(colors)

        #i += 1

    # If latest line array size is smaller, than with,
    # expand this with empty bytes
    while len(result[-1]) < (width*3):
        result[-1].extend((0,0,0))

    # If lines is smaller, than height, expand this
    while len(result) < height:
        result.append([])

        # And fill every line with empty bytes
        for x in range(width):
            result[-1].extend((0,0,0))

    # Calculate width by latest line
    width = int(len(result[-1])/3)
    # Calculate height by lines count
    height = len(result)

    return (result, width, height)

# Convert PyPNG image array to image data
def convert_png_array_to_image_data(png_array: list[list[int]]) -> list[list[tuple[int, int, int]]]:
    result = []

    #y = 0
    for row in png_array:

        x = 0
        # Reduce iterages, because it's filled with multiple colors
        for x_ in range( int( len(row) / 3 ) ):
            result.append( ( row[x], row[x+1], row[x+2] ) )
            x += 3 # Add 3 to index, for skip this pixel, consisting of multiple colors

        #y += 1

    return result


# Write ready PyPNG array to image file
def write_image(filename: str, width: int, height: int):

    # Open a file in binary write mode
    with open(filename, 'wb') as f:
        # Create a PNG writer instance
        w = png.Writer(width, height, greyscale=False, bitdepth=8)
        # Write the image data to the file
        w.write(f, png_array)

    print(f"Image '{filename}' created successfully.")



# Read writed image
def read_image(filename: str):
    reader = png.Reader(filename=filename)
    width, height, pixels, metadata = reader.read()

    result = [list(item) for item in pixels]

    return result



if __name__ == "__main__":

    # image_data = convert_bytes_to_image(bytes_text)
    # print("IMAGE DATA", image_data)


    # result_text = convert_image_to_bytes(image_data)

    # result_text = result_text.decode("utf-8")
    # print(result_text)


    # png_array, width, height = convert_image_data_to_png_array(image_data, 64, 64)
    # print("PNG ARRAY", png_array)

    # write_image("image.png", width, height)

    # readed_image = read_image("image.png")
    # readed_image = convert_png_array_to_image_data(readed_image)
    # print("READED IMAGE", readed_image)


    # readed_image = convert_image_to_bytes(readed_image).decode("utf-8")
    # print(readed_image)

    _mode = input("Enter mode (write image (W) / read image (R)): ").strip().lower()

    if _mode == "w":
        data_filename = input("Enter filename to load text data: ")
        img_filename = input("Enter filename to save image: ")

        img_width = int( input("Enter image width: ").strip() )
        img_height = int( input("Enter image height: ").strip() )

        bytes_text = open(data_filename, 'rb').read()
        image_data = convert_bytes_to_image(bytes_text)

        png_array, width, height = convert_image_data_to_png_array(image_data, img_width, img_height)

        if height != img_height: print("⚠️ Warning: height is changed, because data is not fit due to data")

        write_image(img_filename, width, height)

    elif _mode == "r":
        filename = input("Enter filename to load image: ")
        encoding = input("Enter encoding to decode (enter to utf-8, n to none): ").strip().lower()

        readed_image = read_image(filename)
        readed_image = convert_png_array_to_image_data(readed_image)
        readed_image = convert_image_to_bytes(readed_image)

        if encoding != "n":
            if not encoding:
                encoding = "utf-8"
            
            try:
                readed_image = readed_image.decode(encoding)
            except UnicodeDecodeError:
                print("⚠️ Warning: unicode decoded with errors!")
                readed_image = readed_image.decode(encoding, errors="ignore")
        

        print(f"Result: {readed_image}")

