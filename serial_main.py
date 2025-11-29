import sys
import argparse
import numpy as np
import time
from boxblur_logic import generate_box_blur_kernel, apply_convolution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--kernel", type=int, default=15)
    parser.add_argument("--output", default="serial_result.raw")
    args = parser.parse_args()

    try:
        raw_data = np.fromfile(args.input, dtype=np.uint8)
        image = raw_data.reshape((args.size, args.size))
    except FileNotFoundError:
        print(f"Erro: Arquivo {args.input} não encontrado.", file=sys.stderr)
        sys.exit(1)

    start = time.time()
    kernel_matrix = generate_box_blur_kernel(args.kernel)
    result = apply_convolution(image, kernel_matrix)
    duration = time.time() - start

    try:
        with open(args.output, "wb") as f:
            f.write(result.astype(np.uint8).tobytes())
        print(f"{duration:.4f}")
    except Exception as e:
        print(f"Erro ao salvar: {e}", file=sys.stderr)
        print(f"{duration:.4f}")


if __name__ == "__main__":
    main()
