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

from os.path import exists, isfile
from os import remove
import lib


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


try:
    _mode = input("Enter mode (write image (W) / read image (R)): ").strip().lower()

    # Write mode
    if _mode == "w":
        data_filename = input("Enter filename to load text data (press enter to enter text here): ")

        # If user is not writed filename
        if not data_filename:
            bytes_text = input("Enter text data: ")
            _encoding = input("Enter text encoding (enter to utf-8): ")

            # If user pressed enter, set encoding to UTF-8
            if not _encoding:
                _encoding = "utf-8"

            bytes_text = bytes_text.encode(_encoding) # Encode text

        # If user writed filename
        else:
            if not exists(data_filename): # Check for file existing
                raise Exception(f"file \"{data_filename}\" is not exists!")

            elif not isfile(data_filename): # If this is not file
                raise Exception(f"\"{data_filename}\" is not file!")

            bytes_text = open(data_filename, 'rb').read()

        img_filename = input("Enter filename to save image: ")


        _img_override = ""

        if isfile(img_filename): # If image file is existing, showing override prompt
            _img_override = input(f"File \"{img_filename}\" is existing. Override [ Yes (Y) / No (N) ]: ").strip().lower()

            # Exit program, if is not override file
            if _img_override != "y":
                raise KeyboardInterrupt()

        elif exists(img_filename): # If directory is existing
            raise Exception(f"Directory named \"{img_filename}\" is existing. Please rename or remove this directory.")


        img_width = int( input("Enter image width: ").strip() )
        img_height = int( input("Enter image height: ").strip() )


        # Byte colorize prompt
        _img_colorize = input("\nByte colorize modes:\n 0. Simple red data — don't colorize,\n 1. Colorize bytes — to make it looks like LED display,\n 2. Blackize bytes — to make it darker and more hidden.\nSelect byte colorize mode: ").strip()

        print()

        if is_int(_img_colorize) and 0 <= int(_img_colorize) <= 2:
            colorize_mode = int(_img_colorize)
        else:
            colorize_mode = 0
            print(f"⚠️ Warning: invalid answer \"{_img_colorize}\".")


        # Convert bytes to image data
        image_data = lib.convert_bytes_to_image(bytes_text, colorize_mode)

        # Convert to PyPNG array
        png_array, width, height = lib.convert_image_data_to_png_array(image_data, img_width, img_height)

        # Notify user about image height changes, if data is not fit
        if height != img_height: print("⚠️ Warning: height is changed, because data is not fit due to data.")

        if _img_override: remove(img_filename) # Override image

        # Write image to file
        lib.write_image(img_filename, png_array, width, height)


    # Read mode
    elif _mode == "r":
        filename = input("Enter filename to load image: ")

        if not exists(filename): # If image file is not exists
            raise Exception(f"file \"{filename}\" is not exists.")

        elif not isfile(filename): # If this is not a file
            raise Exception(f"\"{filename}\" is directory!")

        encoding = input("Enter encoding to decode data (enter to utf-8, n to raw bytes): ").strip().lower()

        print()

        readed_image = lib.read_image(filename) # Get PyPNG array from image
        readed_image = lib.convert_png_array_to_image_data(readed_image) # Convert from PyPNG array to image data
        readed_image = lib.convert_image_to_bytes(readed_image) # Convert image data to bytes


        if encoding != "n":
            # If user pressed enter to select utf-8
            if not encoding:
                encoding = "utf-8"

            # Trying to decode bytes
            try:
                readed_image = readed_image.decode(encoding)

            # If decoding has errors
            except UnicodeDecodeError:
                print("⚠️ Warning: unicode decoded with errors!")
                readed_image = readed_image.decode(encoding, errors="ignore") # Decoding with errors ignore

            readed_image = f"\"{readed_image}\""


        # Writing result
        print(f"\nResult: {readed_image}.")


# Program exit
except KeyboardInterrupt: ...

