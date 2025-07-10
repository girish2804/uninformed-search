# 15-Puzzle Solver

A Python implementation for solving the 15-puzzle problem using various uninformed search algorithms. The solver can find a solution path from any solvable initial state to a goal state and can also run benchmarks to compare the performance of different search methods over many random puzzles.

## Features

-   Solves the 15-puzzle (4x4 grid).
-   Checks for puzzle solvability before attempting a search.
-   **Benchmarking Mode**: Automatically generates and solves dozens or hundreds of puzzles to provide stable performance metrics.
-   Implements three search algorithms:
    -   **Breadth-First Search (BFS)**: Guaranteed to find the shortest solution path.
    -   **Depth-First Search (DFS)**: Not optimal and may be very slow or run out of memory.
    -   **Iterative Deepening DFS (IDDFS)**: Combines the benefits of DFS's low memory footprint with BFS's optimality.
-   Flexible command-line interface for both single solves and batch benchmarking.

## File Structure

-   `puzzle_model.py`: Contains the core logic for the puzzle. This includes the `PuzzleNode` class, state transition functions, solvability checks, and the implementation of the BFS, DFS, and IDDFS search algorithms.
-   `test_puzzle.py`: Provides a command-line interface (CLI) to interact with the puzzle solver. It can solve a single user-defined puzzle or run a large benchmark of randomly generated puzzles.

## Requirements

-   Python 3.x
-   NumPy

You can install the necessary library using pip:

```sh
pip install numpy
```

## Usage

The solver is run from the command line using `test_puzzle.py`. You can either solve one specific puzzle or run a benchmark.

### Mode 1: Solving a Single Puzzle

To solve a single, specific puzzle, provide the `--initial` state. You can optionally provide a `--goal` state and choose a specific `--algorithm`.

**Command-Line Arguments:**

-   `--initial`: A required list of 16 integers representing the starting board. Use `0` for the blank space.
-   `--goal` (optional): A list of 16 integers for the target board. Defaults to `1 2 ... 15 0`.
-   `--algorithm` (optional): The algorithm to use (`bfs`, `dfs`, `iddfs`, or `compare`). Defaults to `compare`.

**Example:**

```sh
python test_puzzle.py \
--initial 1 2 3 4 5 6 0 8 9 10 7 11 13 14 15 12 \
--goal 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0 \
--algorithm bfs
```

### Mode 2: Benchmarking Multiple Puzzles

To evaluate algorithm performance robustly, run a benchmark on a set number of randomly generated, solvable puzzles. This mode will report the average time, average moves, and success rate for each algorithm.

**Command-Line Arguments:**

-   `--benchmark N`: A required argument, where `N` is the number of random puzzles to generate and solve.

**Example:**

To run a benchmark on 50 random puzzles:

```sh
python test_puzzle.py --benchmark 50
```

The output will be a final summary table that looks like this:

```
=================================================================
Benchmark Summary (50 puzzles)
=================================================================
Algorithm  | Avg Time (s)    | Avg Moves    | Goals Found (%)
-----------------------------------------------------------------
BFS        | 0.045182        | 14.50        | 100.0
DFS        | 1.891543        | 3542.81      | 92.0
IDDFS      | 0.098331        | 14.50        | 100.0
-----------------------------------------------------------------
```
*(Note: DFS may not find all goals if it hits its internal node limit, which is reflected in the 'Goals Found' percentage.)*
