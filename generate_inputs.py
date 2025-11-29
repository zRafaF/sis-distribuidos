import argparse
import numpy as np
import os


def generate_checkerboard(size):
    block_size = max(16, size // 16)
    checkerboard = np.zeros((size, size), dtype=np.float32)

    for i in range(0, size, block_size):
        for j in range(0, size, block_size):
            if ((i // block_size) + (j // block_size)) % 2 != 0:
                checkerboard[i : i + block_size, j : j + block_size] = 255.0

    noise = np.random.randint(-50, 50, (size, size))
    return (checkerboard + noise).clip(0, 255).astype(np.uint8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--size", type=int, required=True, help="Image side length (square)"
    )
    parser.add_argument("--output", type=str, required=True, help="Output file path")
    args = parser.parse_args()

    print(f"Generating {args.size}x{args.size} image to {args.output}...")
    data = generate_checkerboard(args.size)

    dir_name = os.path.dirname(args.output)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    data.tofile(args.output)
