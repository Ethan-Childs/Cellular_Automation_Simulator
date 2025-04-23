# Cellular Automaton Simulator

**Author**: Ethan Childs  
**Language**: Python  
**Project Type**: Multiprocessing Matrices

**Project Overview**

This program simulates a grid of cells over iterations using defined transformation rules based on neighbor values. 
It includes both serial and multiprocessing (parallel) implementations for speed optimization.
I have included 100 6x6 matrices in the test_matrices folder but this program can run any size matrices just take note
the large the size the longer the simulation takes.
Python is notoriously slow when it comes to multiprocessing especially since I am incorporating index
wrapping with Modulo Arithmetic.

**Important Features**
- Reads input matrix from file
- Simulates iterations of cell behavior
- Handles edge wrap-around (toroidal grid)
- Applies transformation logic (Fibonacci, powers of 2, prime checks)
- Supports multiprocessing with customizable number of threads
- Prints matrix to terminal and writes to file
- Displays execution time

**Conditions for the Cells**

For each cell of the matrix, sum up the neighboring cells using the following rules:
Neighboring cells that are “Healthy O Cells” are equal to three (+3).
Neighboring cells that are “Weakened O Cells” are equal to one (+1).
Neighboring cells that are “dead” are equal to zero (0).
Neighboring cells that are “Weakened X Cells” are equal to negative one (-1).
Neighboring cells that are “Healthy X Cells” are equal to negative three (-3).

If the current cell is a healthy ‘O’ cell
- If the sum of neighbor values is a member of the Fibonacci Sequence, the cell immediately dies.
- Otherwise, if the sum of neighbor values is less than 12, then it becomes a weakened ‘o’ cell.
- Otherwise, the cell remains unchanged.

If the current cell is a weakened ‘o’ cell
- If the sum of neighbor values is less than 0, the cell immediately dies.
- Otherwise, if the sum of neighbor values is greater than 6, then it becomes a healthy ‘O’ cell.
- Otherwise, the cell remains unchanged.

If the current cell is a dead cell
- If the sum of neighbor values is a power of 2, the cell becomes a weakened ‘o’ cell.
- Otherwise, if the absolute value of the sum of neighbor values is a power of 2, the cell becomes a weakened ‘x’ cell.
- Otherwise, the cell remains unchanged.

If the current cell is a weakened ‘x’ cell
- If the sum of neighbor values is greater than or equal to 1, the cell immediately dies.
- Otherwise, if the sum of neighbor values is less than -6, then it becomes a healthy ‘X’ cell.
- Otherwise, the cell remains unchanged.

If the current cell is a healthy ‘X’ cell
- If the absolute value of the sum of neighbor values is a prime number, the cell immediately dies.
- Otherwise, if the sum of neighbor values is greater than -12, then it becomes a weakened ‘x’ cell.
- Otherwise, the cell remains unchanged.

