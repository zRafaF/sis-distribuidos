PYTHON = python
PIP = pip

# Requirements: numpy mpi4py scipy matplotlib
setup:
	$(PIP) install numpy mpi4py scipy matplotlib

# Clean generated files
clean:
	rm -rf bench_inputs *.raw *.png __pycache__

# Run the full benchmark suite (Generates inputs, runs tests, plots)
benchmark:
	$(PYTHON) benchmark_suite.py

show:
	@echo "--- Generating Demo Input ---"
	$(PYTHON) generate_inputs.py --size 512 --output demo_input.raw
	
	@echo "--- Running MPI Blur (n=4) ---"
	mpiexec -n 4 $(PYTHON) mpi_main.py --input demo_input.raw --size 512 --output demo_output.raw
	
	@echo "--- Visualizing Results ---"
	$(PYTHON) visualizer.py --file demo_input.raw --size 512 --title "Input Pattern (512x512)"
	$(PYTHON) visualizer.py --file demo_output.raw --size 512 --title "MPI Box Blur Result"

# Manual run example (useful for debugging without plotting)
run_manual:
	$(PYTHON) generate_inputs.py --size 2048 --output input.raw
	mpiexec -n 4 $(PYTHON) mpi_main.py --input input.raw --size 2048 --output out.raw