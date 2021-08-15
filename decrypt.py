from common import read_image
from typing import Deque, List
import numpy as np
import sys
from textwrap import wrap


path_image = "new_image.bmp"


# TODO
BLACK = [0, 0, 0]
CONTROL_COLOR = BLACK
ENCODE_COLOR = [0,0,1]



def get_pixel_message_in_image(image_array: np.ndarray, control_color, encode_color) -> np.ndarray:
    """
    Decode the message in the image using the control color.
    """

    counter = 0
    message = []
    # Iterate for all the encoded pixels and change its color to the message character color.
    print("Decoding characters from pixels...")
    for y in range(image_array.shape[0]):
        for x in range(image_array.shape[1]):
            # Change the color of the pixel
            if (image_array[y][x] == control_color).all(): #and (image_array[y][x] != encode_color).all():
                # breakpoint()
                # breakpoint()
                # TODO Validate IndexError: index 400 is out of bounds for axis 0 with size 400
                next_one = image_array[y][x+1] if x < image_array.shape[1] else image_array[y+1][0]
                if (next_one == encode_color).all():
                    continue
                message.append(pixel_message_generator(next_one))
                # TODO Add a stop signal when the encoder finish the message and count the pixels here.
                counter += 1
    # TODO Find a better fix.
    # TODO There are more colisions like: ",./" and all the numbers.
    # Probably it will be required to encode in 3 pixels instead of 1.
    return "".join(message).replace("@", " ")
    

def get_binary_complete(args):
    pos, number = args
    if pos == 1:
        return str(number).zfill(3)
    # elif pos == 2:
    #     return str(number) if number
    return str(number)

def pixel_message_generator(pixel, debug=False):
    binary_character = "".join(map(get_binary_complete, enumerate(pixel)))
    try:
        char = (chr(int("0b" + binary_character, 2)))
    except ValueError:
        return ""
    if debug:
        print("Binary character:", binary_character, pixel, char)
    return char

def decrypt(image_file, key: List[int] = CONTROL_COLOR, encode_color=ENCODE_COLOR):
    # Read the image
    np_load_image = read_image(image_file)

    # Decode the message in the modified image using the control color
    message = (get_pixel_message_in_image(np_load_image, control_color=key, encode_color=encode_color))
    print(f"The message encoded in the image is:\n\n{'-'*130}\n", message, f"\n{'-'*130}")
