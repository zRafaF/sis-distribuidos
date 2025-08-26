# Makefile for the Sockets CRUD application

# Use 'python3' if your system defaults to Python 2, otherwise 'python' is fine.
PYTHON = python

# Target to run the server
# Usage: make server
server:
	@echo "Starting the server..."
	$(PYTHON) -m server.main

# Target to run the client
# Usage: make client
client:
	@echo "Starting the client..."
	$(PYTHON) -m client.main

# Phony targets tell make that these are command names, not files.
.PHONY: server client
