import sys
import os
import numpy as np
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

    # Check for silent mode (to avoid spamming stdout during benchmarks)
    verbose = "--verbose" in sys.argv
    input_path = (
        sys.argv[1]
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-")
        else "input_files/image_input.raw"
    )

    # --- 1. Master Preparation ---
    image_shape = None
    full_data = None

    if rank == 0:
        if verbose:
            print(f"Master: Loading {input_path}", flush=True)
        try:
            with open(input_path, "rb") as file:
                raw_data = np.fromfile(file, dtype=np.uint8)

            array_side = int(np.sqrt(raw_data.size))
            full_data = raw_data.reshape((array_side, array_side))

            # Handle height padding
            rows, cols = full_data.shape
            if rows % size != 0:
                rows = (rows // size) * size
                full_data = full_data[:rows, :]

            # Contiguous memory for MPI
            full_data = np.ascontiguousarray(full_data)
            image_shape = full_data.shape

        except Exception as e:
            print(f"Error loading image: {e}")
            sys.exit(1)

    # --- 2. Broadcast & Scatter ---
    image_shape = comm.bcast(image_shape, root=0)
    total_rows, cols = image_shape
    rows_per_rank = total_rows // size

    local_data = np.zeros((rows_per_rank, cols), dtype=np.uint8)
    comm.Scatter(full_data, local_data, root=0)

    # --- 3. Halo Exchange ---
    top_halo = np.zeros((HALO_SIZE, cols), dtype=np.uint8)
    bottom_halo = np.zeros((HALO_SIZE, cols), dtype=np.uint8)

    up_neighbor = rank - 1
    down_neighbor = rank + 1
    TAG_UP, TAG_DOWN = 10, 20
    requests = []

    # Exchange logic
    if up_neighbor >= 0:
        requests.append(
            comm.Isend(
                np.ascontiguousarray(local_data[0:HALO_SIZE, :]),
                dest=up_neighbor,
                tag=TAG_UP,
            )
        )
    if down_neighbor < size:
        requests.append(comm.Irecv(bottom_halo, source=down_neighbor, tag=TAG_UP))
    if down_neighbor < size:
        requests.append(
            comm.Isend(
                np.ascontiguousarray(local_data[-HALO_SIZE:, :]),
                dest=down_neighbor,
                tag=TAG_DOWN,
            )
        )
    if up_neighbor >= 0:
        requests.append(comm.Irecv(top_halo, source=up_neighbor, tag=TAG_DOWN))

    MPI.Request.Waitall(requests)

    # --- 4. Process ---
    parts = []
    if up_neighbor >= 0:
        parts.append(top_halo)
    parts.append(local_data)
    if down_neighbor < size:
        parts.append(bottom_halo)

    compute_data = np.vstack(parts)
    kernel = generate_box_blur_kernel(KERNEL_SIZE)
    processed_chunk = apply_convolution(compute_data, kernel)

    # --- 5. Clip & Gather ---
    start_row = HALO_SIZE if up_neighbor >= 0 else 0
    end_row = processed_chunk.shape[0] - (HALO_SIZE if down_neighbor < size else 0)

    final_strip = np.ascontiguousarray(processed_chunk[start_row:end_row, :])

    gathered_image = None
    if rank == 0:
        gathered_image = np.zeros(image_shape, dtype=np.uint8)

    comm.Gather(final_strip, gathered_image, root=0)

    if rank == 0:
        gathered_image.flatten().tofile("mpi_result.raw")
        if verbose:
            print("Master: Done.", flush=True)


if __name__ == "__main__":
    main()
