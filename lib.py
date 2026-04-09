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
def g_to_multiplier(g: int) -> int:
    if g == 0:
        return 1
    elif g == 1:
        return 2
    else:
        return (g-1) / 10 + 2

# Convert multiplier to G color value
def multiplier_to_g(multiplier: int) -> int:
    if multiplier == 1:
        return 0
    elif multiplier == 2:
        return 1
    else:
        return (multiplier-2) * 10


# Colorizes bytes in image
def colorize_byte(byte: int, i: int) -> tuple[int, int, int]:
    # Common color pallete
    r = byte
    g = b = 0

    # Colorizing after two
    if i % 2 == 0:

        # Changing R to B color
        b = r
        r = 0

        # Colorizing after five
        if i % 5 == 0:
            g = color_limit - b # Some value

    else:
        if (byte % 2 == 0) and (i % 5 == 0):
            r = int(r / 2)
            g = multiplier_to_g(2)
            b = byte - r*2

    return (r, g, b)


# Make byte more dark to make it more hidden
def blackize_byte(byte: int) -> tuple[int, int, int]:
    # Common color pallete
    r = byte
    g = b = 0

    # Multiply G color, while it's visible
    while r > g:
        g += 1
        r = int(byte / g_to_multiplier(g))
        b = byte - int(r*g_to_multiplier(g))

    # Turning back into lucky colors
    g -= 1
    r = int(byte / g_to_multiplier(g))
    b = byte - int(r*g_to_multiplier(g))

    return (r, g, b)


# Convert text bytes to image color values
def convert_bytes_to_image(bytes_text: bytes, colorize_mode: int = 0) -> list[tuple[int, int, int]]:
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

        # Colorize byte
        if colorize_mode == 1:
            r, g, b = colorize_byte(by, i)
        # Blackize byte
        elif colorize_mode == 2:
            r, g, b = blackize_byte(by)

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
def write_image(filename: str, png_array: list[list[int]], width: int, height: int):

    # Open a file in binary write mode
    with open(filename, 'wb') as f:
        # Create a PNG writer instance
        w = png.Writer(width, height, greyscale=False, bitdepth=8)
        # Write the image data to the file
        w.write(f, png_array)

    print(f"Image '{filename}' created successfully.")



# Read writed image
def read_image(filename: str) -> list[list[int]]:
    reader = png.Reader(filename=filename)
    width, height, pixels, metadata = reader.read()

    result = [list(item) for item in pixels]

    return result

