# Cellular Automaton Simulator

**Author**: Ethan Childs  
**Language**: Python  
**Project Type**: Multiprocessing Matrices

**Project Overview**
This program simulates a grid of cells over 100 iterations using defined transformation rules based on neighbor values. 
It includes both serial and multiprocessing (parallel) implementations for speed optimization.
I have included 100 6x6 matrices in the test_matrices folder but this program can run any size matrices just take note
the large the size the longer the simulation takes.
Python is notoriously slow when it comes to multiprocessing especially since I am incorporating index
wrapping with Modulo Arithmetic.

**Important Features**
- Reads input matrix from file
- Simulates 100 iterations of cell behavior
- Handles edge wrap-around (toroidal grid)
- Applies complex transformation logic (Fibonacci, powers of 2, prime checks)
- Supports multiprocessing with customizable number of threads
- Prints matrix to terminal and writes to file
- Displays execution time

**Conditions for the Cells**
1. For each cell of the matrix, sum up the neighboring cells using the following rules:
    a. Neighboring cells that are “Healthy O Cells” are equal to three (+3).
    b. Neighboring cells that are “Weakened O Cells” are equal to one (+1).
    c. Neighboring cells that are “dead” are equal to zero (0).
    d. Neighboring cells that are “Weakened X Cells” are equal to negative one (-1).
    e. Neighboring cells that are “Healthy X Cells” are equal to negative three (-3).

2. If the current cell is a healthy ‘O’ cell
   a. If the sum of neighbor values is a member of the Fibonacci Sequence, the cell immediately dies.
   b. Otherwise, if the sum of neighbor values is less than 12, then it becomes a weakened ‘o’ cell.
   c. Otherwise, the cell remains unchanged.

3. If the current cell is a weakened ‘o’ cell
   a. If the sum of neighbor values is less than 0, the cell immediately dies.
   b. Otherwise, if the sum of neighbor values is greater than 6, then it becomes a healthy ‘O’ cell.
   c. Otherwise, the cell remains unchanged.

4. If the current cell is a dead cell
   a. If the sum of neighbor values is a power of 2, the cell becomes a weakened ‘o’ cell.
   b. Otherwise, if the absolute value of the sum of neighbor values is a power of 2, the cell becomes
   a weakened ‘x’ cell.
   c. Otherwise, the cell remains unchanged.

5. If the current cell is a weakened ‘x’ cell
   a. If the sum of neighbor values is greater than or equal to 1, the cell immediately dies.
   b. Otherwise, if the sum of neighbor values is less than -6, then it becomes a healthy ‘X’ cell.
   c. Otherwise, the cell remains unchanged.

6. If the current cell is a healthy ‘X’ cell
   a. If the absolute value of the sum of neighbor values is a prime number, the cell immediately dies.
   b. Otherwise, if the sum of neighbor values is greater than -12, then it becomes a weakened ‘x’
   cell.
   c. Otherwise, the cell remains unchanged.

