import sys
import numpy as np
from boxblur_logic import generate_box_blur_kernel, apply_convolution, KERNEL_SIZE


def main():
    if len(sys.argv) < 2:
        print("Usage: python serial_main.py <input_path> [output_path]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "serial_result.raw"

    try:
        # Load Data
        with open(input_path, "rb") as f:
            raw_data = np.fromfile(f, dtype=np.uint8)

        # Reshape to square
        size = int(np.sqrt(raw_data.size))
        image = raw_data.reshape((size, size))

        # Process
        kernel = generate_box_blur_kernel(KERNEL_SIZE)
        result = apply_convolution(image, kernel)

        # Save
        result.flatten().tofile(output_path)

    except Exception as e:
        print(f"Error in serial execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
