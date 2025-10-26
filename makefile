# Makefile for the Sockets CRUD application

# Use 'python3' if your system defaults to Python 2, otherwise 'python' is fine.
PYTHON = python

# Target to run the server
# Usage: make server
server:
	@echo "Starting the server..."
	fastapi run ./server/main.py

dev:
	@echo "Starting the server in dev mode..."
	fastapi dev ./server/main.py

# Target to run the client
# Usage: make client
client:
	@echo "Deprecated. Does not apply to FastAPI server."

# Phony targets tell make that these are command names, not files.
.PHONY: server client dev
