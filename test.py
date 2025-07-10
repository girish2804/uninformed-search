# test_puzzle.py

import time
import argparse
from puzzle_model import bfs_search, dfs_search, iddfs_search, is_solvable

# Map algorithm names to their functions in the model
SEARCH_ALGORITHMS = {
    "bfs": bfs_search,
    "dfs": dfs_search,
    "iddfs": iddfs_search,
}

def print_solution(solution_path):
    """Prints the solution path in a readable format."""
    if not solution_path:
        print("No solution was found.")
        return
        
    print(f"\n--- Solution Found in {len(solution_path) - 1} moves ---")
    initial_state = solution_path[0][1]
    print("Initial State:")
    print(initial_state)

    for move, board in solution_path[1:]:
        move_map = {'L': 'Left', 'R': 'Right', 'U': 'Up', 'D': 'Down'}
        print(f"\nMove: {move_map[move]}")
        print(board)
    print("\n--- Goal Reached! ---")

def solve_with_algorithm(algo_name, initial, final, n):
    """Solves the puzzle with a single specified algorithm and prints the result."""
    print(f"\n--- Solving with {algo_name.upper()} ---")
    search_function = SEARCH_ALGORITHMS[algo_name]
    
    start_time = time.perf_counter()
    solution = search_function(initial, n, final)
    end_time = time.perf_counter()

    print(f"Time taken: {end_time - start_time:.6f} seconds")
    print_solution(solution)

def compare_algorithms(initial, final, n):
    """Runs all search algorithms and prints a comparison table."""
    print("\n--- Comparing Search Algorithms ---")
    print("Note: DFS is not optimal and can be very slow or fail on complex puzzles.\n")
    
    results = {}
    for name, func in SEARCH_ALGORITHMS.items():
        print(f"Running {name.upper()}...")
        start_time = time.perf_counter()
        solution = func(initial, n, final)
        end_time = time.perf_counter()
        
        results[name] = {
            "time": end_time - start_time,
            "moves": len(solution) - 1 if solution else "N/A",
            "found": "Yes" if solution else "No"
        }

    print("\n" + "-" * 50)
    print(f"{'Algorithm':<10} | {'Time (s)':<15} | {'Moves':<10} | {'Found':<5}")
    print("-" * 50)
    for name, data in results.items():
        print(f"{name.upper():<10} | {data['time']:<15.6f} | {str(data['moves']):<10} | {data['found']:<5}")
    print("-" * 50)

def main():
    """Main function to parse arguments and run the puzzle solver."""
    n = 4  # The puzzle is a 4x4 grid (15-puzzle)

    parser = argparse.ArgumentParser(
        description="Solve the 15-puzzle using various uninformed search algorithms.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--initial',
        required=True,
        type=int,
        nargs='+',
        help='The initial state of the 15-puzzle (16 numbers, 0 for blank).'
    )
    parser.add_argument(
        '--goal',
        required=True,
        type=int,
        nargs='+',
        help='The goal state of the 15-puzzle (16 numbers, 0 for blank).'
    )
    parser.add_argument(
        '--algorithm',
        required=True,
        choices=['bfs', 'dfs', 'iddfs', 'compare'],
        help="The search algorithm to use.\n"
             "bfs: Breadth-First Search (optimal)\n"
             "dfs: Depth-First Search (not optimal)\n"
             "iddfs: Iterative Deepening DFS (optimal)\n"
             "compare: Run all three and compare performance."
    )

    args = parser.parse_args()
    
    # --- Input Validation ---
    if len(args.initial) != n*n or len(args.goal) != n*n:
        parser.error(f"Both --initial and --goal must contain exactly {n*n} numbers.")

    initial_state = args.initial
    goal_state = args.goal
    
    # --- Solvability Check ---
    if not is_solvable(initial_state, goal_state, n):
        print("\nThis puzzle configuration is NOT SOLVABLE.")
        return

    print("\nPuzzle is solvable. Proceeding with search.")
    
    # --- Run selected algorithm ---
    if args.algorithm == 'compare':
        compare_algorithms(initial_state, goal_state, n)
    else:
        solve_with_algorithm(args.algorithm, initial_state, goal_state, n)

if __name__ == "__main__":
    main()
