import numpy as np
from scipy.signal import convolve2d

# Configuration
KERNEL_SIZE = 19
HALO_SIZE = KERNEL_SIZE // 2


def generate_box_blur_kernel(size):
    """Generates a normalized box blur kernel."""
    num_of_elements = size * size
    return np.full((size, size), 1.0 / num_of_elements)


def apply_convolution(arr, kernel):
    """
    Applies convolution using 'same' mode.
    Note: In MPI, this is applied to the (Halo + Data + Halo) block.
    """
    convolved = convolve2d(arr, kernel, mode="same", boundary="fill", fillvalue=0)
    return np.clip(convolved, 0, 255).astype(np.uint8)
