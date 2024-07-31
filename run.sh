#!/bin/bash

set -e

echo "Running ImportLogs.py..."
python ImportLogs.py

echo "Running Solve.py..."
python Solve.py

echo "Running Test.py..."
python Test.py

echo "Running UnitTest.py..."
python UnitTest.py

echo "All scripts executed successfully."
