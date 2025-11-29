PYTHON = python
PIP = pip

setup:
	$(PIP) install numpy mpi4py scipy matplotlib

clean:
	rm -rf bench_inputs show_inputs show_outputs results *.raw *.png __pycache__

# Roda o benchmark completo e gera gráficos na pasta results/
benchmark:
	$(PYTHON) benchmark_suite.py

# Gera uma Grade Visual (3 Tamanhos x 3 Kernels) em uma única figura
show:
	$(PYTHON) show_grid_demo.py