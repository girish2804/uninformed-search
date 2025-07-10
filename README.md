# 15-Puzzle Solver

A Python implementation for solving the 15-puzzle problem using various uninformed search algorithms. The solver can find a solution path from any solvable initial state to a goal state and can also run benchmarks to compare the performance of different search methods over many random puzzles.

## Features

-   Solves the 15-puzzle (4x4 grid).
-   Checks for puzzle solvability before attempting a search.
-   **Robust Benchmarking Mode**: Automatically generates and solves puzzles, reporting aggregated performance metrics. Each algorithm run is sandboxed with a **timeout** to prevent slow or stuck algorithms from halting the entire process.
-   Implements three uninformed search algorithms:
    -   **Breadth-First Search (BFS)**: An optimal blind search, guaranteed to find the shortest solution. Can be slow and memory-intensive.
    -   **Bidirectional Search**: A significantly faster optimal search that runs two BFS searches simultaneously—one from the start and one from the goal—meeting in the middle. This dramatically reduces the search space.
    -   **Iterative Deepening DFS (IDDFS)**: An optimal blind search that combines the benefits of DFS's low memory footprint with BFS's optimality.

## File Structure

-   `puzzle_model.py`: Contains the core logic for the puzzle, including the `PuzzleNode` class and implementations of the BFS, Bidirectional, and IDDFS search algorithms.
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

To solve a single, specific puzzle, provide the `--initial` state.

**Command-Line Arguments:**

-   `--initial`: A required list of 16 integers representing the starting board. Use `0` for the blank space.
-   `--goal` (optional): A list of 16 integers for the target board. Defaults to `1 2 ... 15 0`.
-   `--algorithm` (optional): The algorithm to use (`bfs`, `bidi`, `iddfs`). Defaults to `bidi`.

**Example:**

To solve using Bidirectional Search:

```sh
python test_puzzle.py --initial 1 2 3 4 5 6 0 8 9 10 7 11 13 14 15 12 --algorithm bidi
```

### Mode 2: Benchmarking Multiple Puzzles

To evaluate algorithm performance robustly, run a benchmark on a set number of randomly generated, solvable puzzles.

**Command-Line Arguments:**

-   `--benchmark N`: A required argument, where `N` is the number of random puzzles to generate and solve.

**Example:**

To run a benchmark on 50 random puzzles:

```sh
python test_puzzle.py --benchmark 50
```

The output will be a final summary table that looks like this:

```
======================================================================
Benchmark Summary (50 puzzles, 15s timeout per run)
======================================================================
Algorithm  | Avg Time (s)    | Avg Moves    | Goals Found (%)
----------------------------------------------------------------------
BFS        | 0.045182        | 14.50        | 100.0
BIDI       | 0.001950        | 14.50        | 100.0
IDDFS      | 0.098331        | 14.50        | 100.0
----------------------------------------------------------------------
```
*(Note: As seen in the example, Bidirectional Search is typically much faster than BFS while finding the same optimal path length.)*
