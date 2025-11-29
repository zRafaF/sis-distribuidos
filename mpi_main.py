import sys
import argparse
import numpy as np
import time
from mpi4py import MPI
from boxblur_logic import (
    generate_box_blur_kernel,
    apply_convolution,
    KERNEL_SIZE,
    HALO_SIZE,
)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--output", default="mpi_result.raw")
    args = parser.parse_args()

    N = args.size

    # --- 1. Preparação ---
    local_rows = N // size
    full_data = None
    if rank == 0:
        try:
            raw = np.fromfile(args.input, dtype=np.uint8).reshape((N, N))
            if raw.shape[0] % size != 0:
                raw = raw[: (N // size) * size, :]
            full_data = np.ascontiguousarray(raw)
        except FileNotFoundError:
            sys.exit(1)

    # --- 2. Scatter ---
    local_chunk = np.zeros((local_rows, N), dtype=np.uint8)

    if rank == 0:
        start_time = time.time()

    comm.Scatter(full_data, local_chunk, root=0)

    # --- 3. Halo Exchange ---
    top_halo = np.zeros((HALO_SIZE, N), dtype=np.uint8)
    bottom_halo = np.zeros((HALO_SIZE, N), dtype=np.uint8)

    reqs = []
    if rank > 0:
        reqs.append(
            comm.Isend(
                np.ascontiguousarray(local_chunk[:HALO_SIZE]), dest=rank - 1, tag=11
            )
        )
        reqs.append(comm.Irecv(top_halo, source=rank - 1, tag=22))

    if rank < size - 1:
        reqs.append(
            comm.Isend(
                np.ascontiguousarray(local_chunk[-HALO_SIZE:]), dest=rank + 1, tag=22
            )
        )
        reqs.append(comm.Irecv(bottom_halo, source=rank + 1, tag=11))

    MPI.Request.Waitall(reqs)

    # --- 4. Computação ---
    process_stack = []
    if rank > 0:
        process_stack.append(top_halo)
    process_stack.append(local_chunk)
    if rank < size - 1:
        process_stack.append(bottom_halo)

    compute_input = np.vstack(process_stack)
    kernel = generate_box_blur_kernel(KERNEL_SIZE)

    processed = apply_convolution(compute_input, kernel)

    start_row = HALO_SIZE if rank > 0 else 0
    end_row = processed.shape[0] - (HALO_SIZE if rank < size - 1 else 0)

    result_chunk = np.ascontiguousarray(
        processed[start_row:end_row, :].clip(0, 255).astype(np.uint8)
    )

    # --- 5. Gather ---
    final_image = None
    if rank == 0:
        final_image = np.zeros((local_rows * size, N), dtype=np.uint8)

    comm.Gather(result_chunk, final_image, root=0)

    if rank == 0:
        duration = time.time() - start_time
        # Correção Robusta: write + tobytes
        try:
            with open(args.output, "wb") as f:
                f.write(final_image.tobytes())
            print(f"{duration:.4f}")
        except Exception as e:
            print(f"Erro ao salvar MPI: {e}", file=sys.stderr)
            print(f"{duration:.4f}")


if __name__ == "__main__":
    main()
