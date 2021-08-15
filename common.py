import numpy as np
from PIL import Image, ImageTk


def read_image(path_image) -> np.ndarray:
    load_image = Image.open(path_image)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_array = np.asarray(load_image)
    return np_load_array


def generate_image(np_load_image):
    np_load_image = Image.fromarray(np.uint8(np_load_image), mode="RGB")
    return np_load_image