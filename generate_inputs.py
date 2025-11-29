import os
import numpy as np

# Configuration
INPUT_FILES_DIR = "input_files"
IMAGE_FILENAME = "image_input.raw"
IMAGE_INPUT_PATH = os.path.join(os.getcwd(), INPUT_FILES_DIR, IMAGE_FILENAME)
IMAGE_SIZE = 4096


def generate_noise(size: int):
    """
    Generates random noise to simulate texture.
    """
    np.random.seed(1234)
    # Generate random integers.
    # Range is wide to create distinct noise when scaled down.
    noise = np.random.randint(
        -256,
        256,
        (size, size),
    )
    return noise


def generate_checkerboard(size: int):
    """
    Generates a checkerboard pattern with overlaid noise.
    """
    block_size = size // 8
    checkerboard = np.zeros((size, size), dtype=np.float32)

    # Fill the checkerboard
    for i in range(0, size, block_size):
        for j in range(0, size, block_size):
            # Alternate between black (0) and white (255) blocks
            is_white = ((i // block_size) + (j // block_size)) % 2 != 0
            if is_white:
                checkerboard[i : i + block_size, j : j + block_size] = 255.0

    noise = generate_noise(size)

    # Combine: Base Pattern + 50% intensity noise
    # We clip to ensure pixel values stay valid (0-255)
    composite = (checkerboard + (noise * 0.5)).clip(0, 255).astype(np.uint8)

    return composite


def main():
    print(f"--- Generating Input Data ({IMAGE_SIZE}x{IMAGE_SIZE}) ---")

    # Ensure directory exists
    if not os.path.exists(INPUT_FILES_DIR):
        print(f"Creating directory: {INPUT_FILES_DIR}")
        os.makedirs(INPUT_FILES_DIR, exist_ok=True)

    # Generate data
    data = generate_checkerboard(IMAGE_SIZE)

    # Save raw bytes
    with open(IMAGE_INPUT_PATH, "wb") as f:
        f.write(data.tobytes())

    print(f"Success: Image saved to {IMAGE_INPUT_PATH}")
    print(f"Data stats - Min: {data.min()}, Max: {data.max()}, Mean: {data.mean():.2f}")


if __name__ == "__main__":
    main()
