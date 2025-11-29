import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys
import os

SIZES = [1024, 2048, 4096]
KERNELS = [3, 15, 21]
INPUT_DIR = "show_inputs"
OUTPUT_DIR = "show_outputs"


def main():
    # Setup
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig, axes = plt.subplots(len(SIZES), len(KERNELS), figsize=(12, 12))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    fig.suptitle(
        "Comparação Visual: Tamanho da Imagem vs Tamanho do Kernel", fontsize=16
    )

    print("--- Gerando e Processando Demo (Isso pode demorar um pouco) ---")

    for i, size in enumerate(SIZES):
        # 1. Gerar Imagem Base
        in_path = os.path.join(INPUT_DIR, f"base_{size}.raw")
        if not os.path.exists(in_path):
            print(f"Gerando entrada {size}x{size}...")
            subprocess.run(
                [
                    sys.executable,
                    "generate_inputs.py",
                    "--size",
                    str(size),
                    "--output",
                    in_path,
                ]
            )

        for j, kernel in enumerate(KERNELS):
            out_path = os.path.join(OUTPUT_DIR, f"blur_{size}_k{kernel}.raw")

            # 2. Processar (Usando MPI n=4 para ser mais rápido)
            print(f"Processando: Img {size} | Kernel {kernel} ...")
            subprocess.run(
                [
                    "mpiexec",
                    "-n",
                    "4",
                    sys.executable,
                    "mpi_main.py",
                    "--input",
                    in_path,
                    "--output",
                    out_path,
                    "--size",
                    str(size),
                    "--kernel",
                    str(kernel),
                ]
            )

            # 3. Carregar e Plotar
            # Dica: Downsample (::size//256) para renderizar rápido no matplotlib
            step = max(1, size // 512)
            try:
                data = np.fromfile(out_path, dtype=np.uint8).reshape((size, size))

                # Plot na grade [i, j]
                ax = axes[i, j]
                ax.imshow(data[::step, ::step], cmap="gray", vmin=0, vmax=255)
                ax.set_title(f"Img: {size}px | Kernel: {kernel}")
                ax.axis("off")
            except Exception as e:
                print(f"Erro ao ler {out_path}: {e}")

    print("Exibindo resultados...")
    plt.show()


if __name__ == "__main__":
    main()
