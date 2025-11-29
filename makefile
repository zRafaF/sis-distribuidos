# --- Configuration ---
PYTHON = python
MPI_RUN = mpiexec
N_PROCS = 10
IMG_SIZE = 2048

# Files
GEN_SCRIPT = generate_inputs.py
SERIAL_SCRIPT = serial_main.py
MPI_SCRIPT = mpi_main.py
BENCH_SCRIPT = benchmark.py
VIS_SCRIPT = visualize_results.py

INPUT_DIR = input_files
INPUT_IMG = $(INPUT_DIR)/image_input.raw
OUTPUT_SERIAL = serial_result.raw
OUTPUT_MPI = mpi_result.raw

# --- Targets ---

all: generate run_mpi

generate:
	@echo "--- Generating Input ---"
	$(PYTHON) $(GEN_SCRIPT)

# Run just the MPI version (single run)
run_mpi:
	@echo "--- Running MPI Version ---"
	$(MPI_RUN) -n $(N_PROCS) $(PYTHON) -u $(MPI_SCRIPT) $(INPUT_IMG) --verbose

# Run just the Serial version (single run)
run_serial:
	@echo "--- Running Serial Version ---"
	$(PYTHON) $(SERIAL_SCRIPT) $(INPUT_IMG) $(OUTPUT_SERIAL)

# Run the benchmark suite
benchmark:
	@echo "--- Running Benchmark Suite ---"
	$(PYTHON) -u $(BENCH_SCRIPT)

# Visualize results
show:
	@echo "--- Visualizing MPI Result ---"
	$(PYTHON) $(VIS_SCRIPT) $(INPUT_IMG) $(OUTPUT_MPI) $(IMG_SIZE)

clean:
	rm -rf $(INPUT_DIR)
	rm -f $(OUTPUT_MPI) $(OUTPUT_SERIAL)

.PHONY: all generate run_mpi run_serial benchmark show clean