#!/bin/bash

set -e

echo "Running Ruff..."
ruff check .

echo "Running Tests..."
pytest -q

echo "Starting Application..."
timeout 5 python main.py

echo "Smoke Test Passed."
