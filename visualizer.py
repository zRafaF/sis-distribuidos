import argparse
import numpy as np
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to raw file")
    parser.add_argument("--size", type=int, required=True, help="Image width/height")
    parser.add_argument("--title", default="Image", help="Plot title")
    args = parser.parse_args()

    try:
        # Load and reshape
        data = np.fromfile(args.file, dtype=np.uint8).reshape((args.size, args.size))

        # Plot
        plt.figure(figsize=(6, 6))
        plt.imshow(data, cmap="gray", vmin=0, vmax=255)
        plt.title(args.title)
        plt.axis("off")
        plt.tight_layout()
        print(f"Displaying {args.title}...")
        plt.show()

    except FileNotFoundError:
        print(f"Error: File {args.file} not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
