#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <number_of_queens>"
  exit 1
fi

NUM_QUEENS=$1

gcc -fopenmp nqueens.c -o nqueens
gcc nqueens_viz.c -o nqueens_viz

./nqueens $NUM_QUEENS

./nqueens_viz nqueens_solutions.txt
python3 visualize_html.py
python3 distribution.py
