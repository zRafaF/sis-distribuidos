import numpy as np
from scipy.signal import convolve2d


def generate_box_blur_kernel(size):
    return np.ones((size, size), dtype=np.float32) / (size * size)


def apply_convolution(image, kernel):
    return convolve2d(image, kernel, mode="same", boundary="fill", fillvalue=0)
