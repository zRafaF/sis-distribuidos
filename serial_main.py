import sys
import argparse
import numpy as np
import time
from boxblur_logic import generate_box_blur_kernel, apply_convolution, KERNEL_SIZE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--output", default="serial_result.raw")
    args = parser.parse_args()

    # Carregar
    try:
        raw_data = np.fromfile(args.input, dtype=np.uint8)
        image = raw_data.reshape((args.size, args.size))
    except FileNotFoundError:
        # Erros vão para stderr para não quebrar o benchmark
        print(f"Erro: Arquivo {args.input} não encontrado.", file=sys.stderr)
        sys.exit(1)

    # Processar
    start = time.time()
    kernel = generate_box_blur_kernel(KERNEL_SIZE)
    result = apply_convolution(image, kernel)
    duration = time.time() - start

    # Salvar de forma robusta (Python nativo + tobytes)
    try:
        with open(args.output, "wb") as f:
            f.write(result.astype(np.uint8).tobytes())

        # O print do tempo vai para stdout (sucesso)
        print(f"{duration:.4f}")

    except Exception as e:
        print(f"Erro ao salvar: {e}", file=sys.stderr)
        # Ainda imprimimos o tempo para o benchmark não falhar totalmente,
        # mas o erro estará visível no log
        print(f"{duration:.4f}")


if __name__ == "__main__":
    main()
