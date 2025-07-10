# 15-Puzzle Solver

A Python implementation for solving the 15-puzzle problem using various uninformed search algorithms. The solver can find a solution path from any solvable initial state to a goal state and can also compare the performance of different search methods.

## Features

-   Solves the 15-puzzle (4x4 grid).
-   Checks for puzzle solvability before attempting a search.
-   Implements three search algorithms:
    -   **Breadth-First Search (BFS)**: Guaranteed to find the shortest solution path.
    -   **Depth-First Search (DFS)**: Not optimal and may be very slow or run out of memory.
    -   **Iterative Deepening DFS (IDDFS)**: Combines the benefits of DFS's low memory footprint with BFS's optimality.
-   Command-line interface for easy execution and scripting.
-   Ability to compare the performance of all implemented algorithms on a given puzzle.

## File Structure

-   `puzzle_model.py`: Contains the core logic for the puzzle. This includes the `PuzzleNode` class, state transition functions, solvability checks, and the implementation of the BFS, DFS, and IDDFS search algorithms.
-   `test_puzzle.py`: Provides a command-line interface (CLI) to interact with the puzzle solver. It parses user arguments, calls the appropriate functions from `puzzle_model.py`, and displays the results.

## Requirements

-   Python 3.x
-   NumPy

You can install the necessary library using pip:

```sh
pip install numpy
```

## Usage

The solver is run from the command line using `test_puzzle.py`. You must provide the initial state, the goal state, and the algorithm to use.

### Command-Line Arguments

-   `--initial`: A required list of 16 integers representing the starting board. Use `0` for the blank space.
-   `--goal`: A required list of 16 integers representing the target board.
-   `--algorithm`: A required choice of which algorithm to run.
    -   `bfs`: Solves using Breadth-First Search.
    -   `dfs`: Solves using Depth-First Search.
    -   `iddfs`: Solves using Iterative Deepening DFS.
    -   `compare`: Runs all three algorithms and shows a performance comparison table.

### Example 1: Solving with a Single Algorithm (BFS)

To solve a puzzle and see the step-by-step solution, specify an algorithm like `bfs`.

```sh
python test_puzzle.py \
--initial 1 2 3 4 5 6 7 8 9 10 11 0 13 14 15 12 \
--goal 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0 \
--algorithm bfs
```

### Example 2: Comparing All Algorithms

To see how the different algorithms perform on the same puzzle, use `compare`.

```sh
python test_puzzle.py \
--initial 1 2 3 4 5 6 0 8 9 10 7 11 13 14 15 12 \
--goal 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0 \
--algorithm compare
```

The output will be a summary table:

```
--- Comparing Search Algorithms ---
Note: DFS is not optimal and can be very slow or fail on complex puzzles.

Running BFS...
Running DFS...
Running IDDFS...

--------------------------------------------------
Algorithm  | Time (s)        | Moves      | Found
--------------------------------------------------
BFS        | 0.002135        | 4          | Yes
DFS        | 0.000150        | 16         | Yes
IDDFS      | 0.002661        | 4          | Yes
--------------------------------------------------
```

