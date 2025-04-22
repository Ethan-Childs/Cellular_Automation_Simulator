# Libraries
# imports for command arguments
import argparse
import os
# import for the Mathematical Conditions
import math
# import to preform the Multiprocessing
from multiprocessing import Pool
# import to track how long this takes to iteration through each matrix
import time

# Function to ensure an input file exists
def input_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"[Error] Input File does not Exist: '{path}'")
    return path

# Function to ensure a directory for the output file exists
def output_file(path):
    directory = os.path.dirname(path) or '.'
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(f"[Error] Directory for Output File does not Exist: '{directory}'")
    return path

# Function to track the number of process to spawn
def process_count(value):
    try:
        spawn = int(value)
        if spawn <= 0:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"[Error] there must be more than 0 processes")
    return spawn

# Function to Parse the correct arguments -i, -o, -p
def parse_arguments():
    parser = argparse.ArgumentParser()
    # adding argument for -i
    parser.add_argument(
        '-i','--input',
        required = True,
        type = input_file
    )

    # adding argument for -o
    parser.add_argument(
        '-o','--output',
        required = True,
        type = output_file
    )

    # adding argument for -p
    parser.add_argument(
        '-p','--processes',
        type = process_count,
        default = 1
    )

    return parser.parse_args()

# Function to read the matrix file from -i and return it as a 2D list
def read_matrix(path):
    matrix = []

    try:
        with open(path, 'r') as file:
            for line in file:
                line = line.strip() # accounting for blank lines
                if line:
                    matrix.append(list(line))

        row_length = len(matrix[0])
        for i, row in enumerate(matrix):
           if len(row) != row_length:
                raise ValueError(f"[Error] Row {i + 1} has an invalid length")
        return matrix

    except FileNotFoundError:
        raise FileNotFoundError(f"[Error] Input File Not Found: {path}")
    except Exception as e:
        raise Exception(f"[Error] Problem Reading Matrix: {e}")

# Function to write the matrix to an outputfile
def write_matrix(path, matrix):
    try:
        with open(path, 'w') as file:
            for row in matrix:
                line = ''.join(row)
                file.write(line + '\n') # Printing to the file
                print(line) # Printing to the console
    except Exception as e:
        raise Exception(f"[Error] Cannot Write Matrix: {e}")

# Functions to do 100 iterations on the matrix using various algorithms
def sum_matrix(matrix, row, col):
    weights = {'O':3,  #Healthy o
               'o':1,  #Weakened o
               '.':0,  #Dead
               'x':-1, #Weakened x
               'X':-3}  #Healthy x

    # Wrapping around to ensure we always have 8 neighboring elements
    total = 0
    num_row = len(matrix)
    num_col = len(matrix[0])
    # Establishing the 3x3 excluding the center element
    for rwrap in [-1,0,1]:
        for cwrap in [-1,0,1]:
            if rwrap == 0 and cwrap ==0:
                continue

            # Modulus remainder math to preform the wraparound
            r = (row + rwrap) % num_row
            c = (col + cwrap) % num_col
            status = matrix[r][c]
            value = weights.get(status,0)
            total = total + value
    return total

# Function to kill the Healthy 'O' cell if sum_matrix = a Fibonacci number
# Binet's Formula proves
# A number n is a Fibonacci number if and only if either:
# 5n^2 + 4 or 5n^2 - 4 is a perfect square such that n is positive integer

def fibonacci_check(n): # n here is referring to total from sum_matrix
    if n < 0:
        return False

    def passes_test(x):
        root = int(math.sqrt(x))
        return root * root == x

    return (
            passes_test(5 * n * n + 4) or
            passes_test(5 * n * n - 4)
    )

# Function to turn dead cells '.' into weakened 'o' cells if sum_matrix = a power of 2
def power_of_two_check(n): # n here is referring to total from sum_matrix
    return n > 0 and (n & (n - 1)) == 0

# Function to turn Healthy 'X' cell dead if sum_matrix = a prime number
def prime_number_check(n): # n here is referring to total from sum_matrix
    if n <= 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True

#Function to build each new row with multiprocessing
def multiprocess_row(row_multi, matrix):
    num_cols = len(matrix[0])
    new_row = []

    for col in range(num_cols):
        cell = matrix[row_multi][col]
        neighbor_sum = sum_matrix(matrix, row_multi, col)

        # Checking same conditions from simulate_matrix() but with new variables for multiprocessing
        # Healthy 'O' cell
        if cell == 'O':
            if fibonacci_check(neighbor_sum):
                new_row.append('.')
            elif neighbor_sum < 12:
                new_row.append('o')
            else:
                new_row.append('O')

        # Weakened 'o' cell
        elif cell == 'o':
            if neighbor_sum < 0:
                new_row.append('.')
            elif neighbor_sum > 6:
                new_row.append('O')
            else:
                new_row.append('o')

        # Dead '.' cell
        elif cell == '.':
            if power_of_two_check(neighbor_sum):
                new_row.append('o')
            elif power_of_two_check(abs(neighbor_sum)):
                new_row.append('x')
            else:
                new_row.append('.')

       # Weakened 'x' cell
        elif cell == 'x':
            if neighbor_sum >= 1:
                new_row.append('.')
            elif neighbor_sum < -6:
                new_row.append('X')
            else:
                new_row.append('x')

        # Healthy 'X' cell
        elif cell == 'X':
            if prime_number_check(abs(neighbor_sum)):
                new_row.append('.')
            elif neighbor_sum > -12:
                new_row.append('x')
            else:
                new_row.append('X')

         # Setting any invalid character to dead
        else:
            new_row.append('.')

    return row_multi, new_row

# Function to build and simulate the 100 iterations and include the multiprocessing
def simulate_matrix(matrix, iterations = 100, processes = 1):
    num_row = len(matrix)

    for _ in range(iterations):
        with Pool(processes = processes) as pool:

            # Makes a command arguments for each row
            args = [(i, matrix) for i in range(num_row)]
            # Runs each row and updates them parallel to each other
            results = pool.starmap(multiprocess_row, args)

        # Using Hash Key to sort by row index to ensure nothing comes back out of order
        results.sort(key = lambda x: x[0])

        # Initializing the new matrix
        matrix = [row for _, row in results]

    return matrix

# Main function to test stages
def main():
    print("Process :: Begin")

    start = time.time() # Starting Timer

    args = parse_arguments()  # Parse and validate all command-line args

    matrix = read_matrix(args.input)
    matrix = simulate_matrix(matrix, processes=args.processes)
    write_matrix(args.output, matrix)

    end = time.time() # Ending Timer

    print("Process :: End")

    print(f"Execution Time:{end - start: .2f} seconds")

if __name__ == "__main__":
    main()

