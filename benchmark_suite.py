import subprocess
import sys
import os
import time
import matplotlib.pyplot as plt
import numpy as np

# Configurações
SIZES = [1024, 2048, 4096]
KERNELS = [3, 15, 21]
PROCS_LIST = [2, 4, 8]
REPEATS = 3
INPUT_DIR = "bench_inputs"
RESULTS_DIR = "results"


def run_cmd(cmd):
    """
    Executa o comando e retorna uma tupla: (tempo_computacao, tempo_total_real)
    """
    start_real = time.time()
    try:
        # check=True garante que erros parem a execução
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_real = time.time()

        # O tempo total que você sente no relógio
        total_duration = end_real - start_real

        # O tempo de computação reportado pelo script (última linha do stdout)
        lines = result.stdout.strip().split("\n")
        compute_duration = float(lines[-1])

        return compute_duration, total_duration

    except Exception as e:
        print(f"Erro: {e}")
        return None, None


def main():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    # Estrutura: results[kernel][size]['serial'|'mpi'][procs]
    data = {}

    print("--- 1. Gerando Entradas ---")
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    for s in SIZES:
        path = os.path.join(INPUT_DIR, f"input_{s}.raw")
        if not os.path.exists(path):
            print(f"Gerando {s}x{s}...")
            subprocess.run(
                [
                    sys.executable,
                    "generate_inputs.py",
                    "--size",
                    str(s),
                    "--output",
                    path,
                ]
            )

    print("\n--- 2. Benchmarking (Comparando Tempo de Cálculo vs Tempo Total) ---")

    for k in KERNELS:
        data[k] = {}
        print(f"\n{'='*20} KERNEL SIZE: {k} {'='*20}")

        for s in SIZES:
            data[k][s] = {"serial": 0, "mpi": {}}
            input_path = os.path.join(INPUT_DIR, f"input_{s}.raw")

            # --- Execução Serial ---
            print(f"\n[Img {s}x{s}] Serial:")
            times_compute = []
            times_total = []

            for i in range(REPEATS):
                comp, tot = run_cmd(
                    [
                        sys.executable,
                        "serial_main.py",
                        "--input",
                        input_path,
                        "--size",
                        str(s),
                        "--kernel",
                        str(k),
                    ]
                )
                if comp:
                    times_compute.append(comp)
                    times_total.append(tot)
                    print(f"  Run {i+1}: Cálculo={comp:.3f}s | Total={tot:.2f}s")

            avg_comp = np.mean(times_compute) if times_compute else 0
            data[k][s]["serial"] = avg_comp
            print(f"  -> Média Cálculo: {avg_comp:.4f}s")

            # --- Execução MPI ---
            for p in PROCS_LIST:
                print(f"[Img {s}x{s}] MPI n={p}:")
                times_compute = []
                times_total = []

                for i in range(REPEATS):
                    cmd = [
                        "mpiexec",
                        "-n",
                        str(p),
                        sys.executable,
                        "mpi_main.py",
                        "--input",
                        input_path,
                        "--size",
                        str(s),
                        "--kernel",
                        str(k),
                    ]

                    comp, tot = run_cmd(cmd)
                    if comp:
                        times_compute.append(comp)
                        times_total.append(tot)
                        print(f"  Run {i+1}: Cálculo={comp:.3f}s | Total={tot:.2f}s")

                avg_mpi = np.mean(times_compute) if times_compute else 0
                data[k][s]["mpi"][p] = avg_mpi

                # Speedup baseado apenas no cálculo (o correto para algoritmos)
                speedup = data[k][s]["serial"] / avg_mpi if avg_mpi > 0 else 0
                print(f"  -> Média Cálculo: {avg_mpi:.4f}s (Speedup: {speedup:.2f}x)")

    print("\n--- 3. Gerando Gráficos ---")
    plot_results(data)


def plot_results(data):
    for k in KERNELS:
        # Gráfico 1: Speedup (Separado por Kernel)
        plt.figure(figsize=(10, 6))
        for s in SIZES:
            serial = data[k][s]["serial"]
            if serial == 0:
                continue
            procs = sorted(data[k][s]["mpi"].keys())
            speedups = [serial / data[k][s]["mpi"][p] for p in procs]
            plt.plot(procs, speedups, marker="o", label=f"Img {s}x{s}")

        plt.title(f"Speedup MPI - Apenas Cálculo (Kernel {k})")
        plt.xlabel("Processos")
        plt.ylabel("Speedup")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(RESULTS_DIR, f"speedup_kernel_{k}.png"))
        plt.close()

        # Gráfico 2: Tempo Absoluto (Separado por Kernel)
        plt.figure(figsize=(10, 6))
        serial_times = [data[k][s]["serial"] for s in SIZES]
        plt.plot(SIZES, serial_times, "k--", marker="x", label="Sequencial")

        for p in PROCS_LIST:
            mpi_times = [data[k][s]["mpi"][p] for s in SIZES]
            plt.plot(SIZES, mpi_times, marker="o", label=f"MPI n={p}")

        plt.title(f"Tempo de Cálculo (Kernel {k})")
        plt.xlabel("Tamanho Imagem")
        plt.ylabel("Tempo (s)")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(RESULTS_DIR, f"tempo_kernel_{k}.png"))
        plt.close()

    print(f"Gráficos salvos em: {os.getcwd()}/{RESULTS_DIR}")


if __name__ == "__main__":
    main()
