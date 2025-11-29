import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Default size used in generator
DEFAULT_SIZE = 1024


def load_raw_image(filepath, size):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None

    try:
        with open(filepath, "rb") as f:
            data = np.fromfile(f, dtype=np.uint8)

        # Safety check for size mismatch
        if data.size != size * size:
            print(
                f"Warning: File size {data.size} does not match expected {size}x{size}={size*size}."
            )
            # Try to infer square size
            actual_size = int(np.sqrt(data.size))
            print(f"Inferring size as {actual_size}x{actual_size}")
            return data.reshape((actual_size, actual_size))

        return data.reshape((size, size))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python visualize_results.py <input_raw> <output_raw> [size]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_SIZE

    print("Loading images...")
    img_in = load_raw_image(input_path, size)
    img_out = load_raw_image(output_path, size)

    if img_in is None:
        sys.exit(1)

    # Setup the plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot Input
    axes[0].imshow(img_in, cmap="gray", vmin=0, vmax=255)
    axes[0].set_title("Input (Noisy Checkerboard)")
    axes[0].axis("off")

    # Plot Output
    if img_out is not None:
        axes[1].imshow(img_out, cmap="gray", vmin=0, vmax=255)
        axes[1].set_title("Output (Parallel Box Blur)")
        axes[1].axis("off")
    else:
        axes[1].text(
            0.5,
            0.5,
            'Output file not found\nRun "make run" first',
            ha="center",
            va="center",
        )
        axes[1].axis("off")

    plt.tight_layout()
    print("Displaying plot window...")
    plt.show()


if __name__ == "__main__":
    main()
