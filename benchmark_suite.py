import subprocess
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

SIZES = [1024, 2048, 4096]
PROCS_LIST = [2, 4, 8]
REPEATS = 3
INPUT_DIR = "bench_inputs"


def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        return float(lines[-1])
    except subprocess.CalledProcessError as e:
        print(f"\nErro ao executar comando: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        return None


def main():
    results = {"sizes": SIZES, "serial": {}, "mpi": {}}

    print("--- 1. Gerando Dados de Entrada ---")
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)

    for s in SIZES:
        path = os.path.join(INPUT_DIR, f"input_{s}.raw")
        if not os.path.exists(path):
            print(f"  Gerando {s}x{s}...", end=" ", flush=True)
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
            print("Feito.")

    print("\n--- 2. Executando Benchmarks ---")

    for s in SIZES:
        input_path = os.path.join(INPUT_DIR, f"input_{s}.raw")
        print(f"\n[Tamanho da Imagem: {s}x{s}]")

        print(f"  Sequencial: ", end="", flush=True)
        times = []
        for _ in range(REPEATS):
            t = run_cmd(
                [
                    sys.executable,
                    "serial_main.py",
                    "--input",
                    input_path,
                    "--size",
                    str(s),
                ]
            )
            if t:
                times.append(t)
                print(f"[{t:.2f}s] ", end="", flush=True)

        avg_serial = np.mean(times) if times else 0
        results["serial"][s] = avg_serial
        print(f"-> Méd: {avg_serial:.4f}s")

        results["mpi"][s] = {}
        for p in PROCS_LIST:
            print(f"  MPI (n={p}): ", end="", flush=True)
            times = []
            for _ in range(REPEATS):
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
                ]
                t = run_cmd(cmd)
                if t:
                    times.append(t)
                    print(f"[{t:.2f}s] ", end="", flush=True)

            avg_mpi = np.mean(times) if times else 0
            results["mpi"][s][p] = avg_mpi

            speedup = avg_serial / avg_mpi if avg_mpi > 0 else 0
            print(f"-> Méd: {avg_mpi:.4f}s (Speedup: {speedup:.2f}x)")

    print("\n--- 3. Gerando Gráficos ---")
    plot_results(results)


def plot_results(data):
    try:
        sizes = data["sizes"]

        plt.figure(figsize=(10, 6))
        for s in sizes:
            if data["serial"][s] == 0:
                continue

            serial_time = data["serial"][s]
            procs = sorted(data["mpi"][s].keys())
            speedups = [serial_time / data["mpi"][s][p] for p in procs]
            plt.plot(procs, speedups, marker="o", label=f"Imagem {s}x{s}")

        plt.title("Speedup MPI vs Número de Processos")
        plt.xlabel("Número de Processos (Ranks MPI)")
        plt.ylabel("Fator de Speedup (vs Sequencial)")
        plt.grid(True)
        plt.legend()
        plt.savefig("benchmark_speedup.png")
        print("Salvo benchmark_speedup.png")

        plt.figure(figsize=(10, 6))
        serial_times = [data["serial"][s] for s in sizes]
        plt.plot(
            sizes,
            serial_times,
            marker="x",
            linestyle="--",
            label="Sequencial",
            color="black",
        )

        for p in PROCS_LIST:
            mpi_times = [data["mpi"][s][p] for s in sizes]
            plt.plot(sizes, mpi_times, marker="o", label=f"MPI (n={p})")

        plt.title("Tempo de Execução vs Tamanho da Imagem")
        plt.xlabel("Tamanho da Imagem (N x N)")
        plt.ylabel("Tempo (segundos)")
        plt.grid(True)
        plt.legend()
        plt.savefig("benchmark_time.png")
        print("Salvo benchmark_time.png")
    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")


if __name__ == "__main__":
    main()
