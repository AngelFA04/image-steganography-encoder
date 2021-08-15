from collections import deque
from typing import List

import random
from common import generate_image, read_image
import numpy as np
import sys
from PIL import Image, ImageTk
from textwrap import wrap
path_image = "test.jpg"
# TODO Should be the same of the image.
image_display_size = 400, 300

# TODO
BLACK = [0, 0, 0]
CONTROL_COLOR = BLACK
ENCODE_COLOR = [0,0,1]

# Add to this function the validation in case that the color already exists in the image.
# TODO Find a better way to randomize the pixels distribution.
# TODO Remove hard_coded total_pixels
def random_color_change(np_load_image: np.ndarray, key_color, total_pixels: int = 100):
    """
    Change a random amount of pixels to the encoding color.
    """
    # Generate a list of unique pixels
    #random_pixel_indexs = np.random.choice(np_load_image.shape[0] * np_load_image.shape[1], total_pixels, replace=False)
    print("Creating reference points to add message...")
    # random_len_in_y = random.choices(range(0, np_load_image.shape[0]))
    random_len_in_y = np.random.choice(total_pixels//4, replace=False)
    row_positions =  np.random.choice(np_load_image.shape[0], random_len_in_y, replace=False)
    # TODO Validate that product of len(row_positions) and len(random_len_in_y) is >= to total_pixels
    division = total_pixels//(random_len_in_y)
    column_positions = np.random.choice(np_load_image.shape[1], 
                                        division + (total_pixels - division *(random_len_in_y)), 
                                        replace=False)
    # Change the color of the pixels
    for y in row_positions:
        for x in column_positions:
            # TODO Add another pixel key before this one
            np_load_image[y][x] = key_color
    
    print("Reference points created")

    return np_load_image

def find_key_color_and_insert_message(image_array: np.ndarray, message_pixels: deque, key_color: list, encode_color=ENCODE_COLOR):
    """
    Search a color in the image and replace the inmediate right pixel, but with a new color.
    """
    # Iterate over the image
    pixels_changed = 0

    for y in range(image_array.shape[0]):
        for x in range(image_array.shape[1]):
            # Change the color of the pixel
            # TODO Optimize this function. Here can be added the message.
            if (image_array[y][x] == key_color).all():
                if not message_pixels:
                    break
                if x < image_array.shape[1] - 1:
                    # TODO Add another pixel key before this one
                    image_array[y][x + 1] = message_pixels.popleft()
                    pixels_changed += 1
                else:
                    # Update the first pixel of the following row
                    image_array[y + 1][0] = message_pixels.popleft()
                    pixels_changed += 1
    print("{} pixels changed".format(pixels_changed))
    return image_array# , pixels_changed


def encode_message(message: str) -> np.ndarray:
    """
    Encode the message in the image using the encode color.
    """

    # TODO Change to logger
    print("Encoding message into the image...")

    pixels_from_message = deque()
    # Generate a list of pixels that came from the message
    for char in message:
        # TODO IMPORTANT Verify what is the max number of the ASCII table
        # TODO The " " character is lost.
        color = [int(part) for part in wrap(bin(ord(char))[2:], 3)] # TODO Convert into a list,
        if len(color) == 1:
            color.extend([0,0])
        elif len(color) == 2:
            color.extend([0])
        elif len(color) > 3:
            print("ERROR Encoding", char)
       
        pixels_from_message.append(color)
    return pixels_from_message


def encrypt(image_file, message, key: List[int], encode_color=ENCODE_COLOR):
    # Read the image
    np_load_image = read_image(image_file)

    # Randomly change the color of the pixels to encode the message
    np_load_image = random_color_change(np_load_image, key_color=key, total_pixels=len(message))

    # Search the key color and encode the message 
    pixels_from_message = encode_message(message)
    np_load_image = find_key_color_and_insert_message(np_load_image, pixels_from_message, key_color=key)

    # # Encode the message in the modified image using the encode_color
    # np_load_image = encode_message_in_image(np_load_image, message, control_color=key, encode_color=encode_color)

    # # Generate the image
    load_image = generate_image(np_load_image)
    load_image.save("encoded_image.png", bitmap_format="bmp")
