# Text to image coder
Encoding and decoding text from images.

Program getting text from specified text file, converting to bytes and writing every byte to pixel color channel, and image consists of a set of this pixels. Encoding is depends by file encoding.

Encoded text to image sample:

![Sample image](example.png "Sample image")

After that, you can decode this image back to text, specify image path and encoding, which depends by file encoding, typicaly is UTF-8 (you can press enter to select UTF-8). You can also specify other encoding, or don't decode, by entering "n". After that, you will get decoded text. And if file has incorrect pixels or encoding has errors, program will be notified to you about that.

Program is too easy to use, and you can use this as CLI *(Command Line Interface)* or as library, imported to other file.

But follow the **license** in license file!
