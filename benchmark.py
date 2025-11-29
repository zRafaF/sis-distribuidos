import subprocess
import time
import numpy as np
import sys
import os

# --- Configuration ---
ITERATIONS = 5
MPI_PROCS = 10
INPUT_FILE = "input_files/image_input.raw"

SERIAL_CMD = [sys.executable, "serial_main.py", INPUT_FILE]
# Note: Adjust 'mpiexec' if your system uses 'mpirun'
MPI_CMD = [
    "mpiexec",
    "-n",
    str(MPI_PROCS),
    sys.executable,
    "-u",
    "mpi_main.py",
    INPUT_FILE,
]


def run_benchmark(label, command, runs):
    times = []
    print(f"\n--- Benchmarking {label} ({runs} runs) ---")
    print(f"Command: {' '.join(command)}")

    for i in range(runs):
        start_time = time.time()

        # Run the subprocess
        result = subprocess.run(command, capture_output=True)

        end_time = time.time()
        duration = end_time - start_time

        if result.returncode != 0:
            print(f"Run {i+1} failed!")
            print(result.stderr.decode())
            return None

        times.append(duration)
        print(f"Run {i+1}: {duration:.4f}s")

    return np.array(times)


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'make generate' first.")
        sys.exit(1)

    print(f"Starting Benchmark Suite (N={ITERATIONS})")

    # 1. Run Serial
    serial_times = run_benchmark("Serial", SERIAL_CMD, ITERATIONS)

    # 2. Run Parallel
    parallel_times = run_benchmark(f"Parallel (MPI n={MPI_PROCS})", MPI_CMD, ITERATIONS)

    if serial_times is None or parallel_times is None:
        print("Benchmarking aborted due to errors.")
        sys.exit(1)

    # 3. Report
    print("\n" + "=" * 40)
    print("       BENCHMARK RESULTS       ")
    print("=" * 40)

    s_mean = np.mean(serial_times)
    s_std = np.std(serial_times)

    p_mean = np.mean(parallel_times)
    p_std = np.std(parallel_times)

    speedup = s_mean / p_mean

    print(f"{'Metric':<15} | {'Serial':<12} | {'Parallel':<12}")
    print("-" * 45)
    print(f"{'Mean Time':<15} | {s_mean:.4f}s      | {p_mean:.4f}s")
    print(f"{'Std Dev':<15} | {s_std:.4f}s      | {p_std:.4f}s")
    print(
        f"{'Min Time':<15} | {np.min(serial_times):.4f}s      | {np.min(parallel_times):.4f}s"
    )
    print(
        f"{'Max Time':<15} | {np.max(serial_times):.4f}s      | {np.max(parallel_times):.4f}s"
    )
    print("-" * 45)
    print(f"Speedup: {speedup:.2f}x")
    print("=" * 40)


if __name__ == "__main__":
    main()
