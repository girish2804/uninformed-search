# test_puzzle.py

import time
import argparse
import random
import numpy as np
from puzzle_model import bfs_search, dfs_search, iddfs_search, is_solvable

# Map algorithm names to their functions in the model
SEARCH_ALGORITHMS = {
    "bfs": bfs_search,
    "dfs": dfs_search,
    "iddfs": iddfs_search,
}

# --- Puzzle Generation ---

def generate_solvable_puzzle(goal_state, n, shuffles=30):
    """
    Generates a solvable puzzle by starting from the goal state
    and making a number of random moves.
    """
    state = goal_state[:]
    last_move = None

    for _ in range(shuffles):
        gap_idx = state.index(0)
        valid_moves = []
        if (gap_idx % n) > 0 and last_move != 'R': valid_moves.append('L')
        if (gap_idx % n) < n - 1 and last_move != 'L': valid_moves.append('R')
        if (gap_idx // n) > 0 and last_move != 'D': valid_moves.append('U')
        if (gap_idx // n) < n - 1 and last_move != 'U': valid_moves.append('D')

        move = random.choice(valid_moves)
        
        if move == 'L':
            state[gap_idx], state[gap_idx - 1] = state[gap_idx - 1], state[gap_idx]
            last_move = 'L'
        elif move == 'R':
            state[gap_idx], state[gap_idx + 1] = state[gap_idx + 1], state[gap_idx]
            last_move = 'R'
        elif move == 'U':
            state[gap_idx], state[gap_idx - n] = state[gap_idx - n], state[gap_idx]
            last_move = 'U'
        elif move == 'D':
            state[gap_idx], state[gap_idx + n] = state[gap_idx + n], state[gap_idx]
            last_move = 'D'

    return state

# --- Reporting Functions ---

def print_solution(solution_path):
    """Prints a single solution path in a readable format."""
    if not solution_path:
        print("No solution was found.")
        return
        
    print(f"\n--- Solution Found in {len(solution_path) - 1} moves ---")
    print(f"Initial State:\n{solution_path[0][1]}")
    # To keep output concise, we don't print every step for a single solve anymore,
    # but you can uncomment the loop below if you want to see the full path.
    # for move, board in solution_path[1:]:
    #     move_map = {'L': 'Left', 'R': 'Right', 'U': 'Up', 'D': 'Down'}
    #     print(f"\nMove: {move_map[move]}")
    #     print(board)
    print(f"\n--- Goal Reached! ---\nFinal State:\n{solution_path[-1][1]}")


def print_benchmark_summary(results, num_puzzles):
    """Prints the final summary table for a benchmark run."""
    print("\n" + "="*65)
    print(f"Benchmark Summary ({num_puzzles} puzzles)")
    print("="*65)
    print(f"{'Algorithm':<10} | {'Avg Time (s)':<15} | {'Avg Moves':<12} | {'Goals Found (%)':<20}")
    print("-" * 65)

    for name, data in results.items():
        avg_time = np.mean(data['times']) if data['times'] else 0
        avg_moves = np.mean(data['moves']) if data['moves'] else 0
        found_percent = (data['found'] / num_puzzles) * 100
        
        print(f"{name.upper():<10} | {avg_time:<15.6f} | {avg_moves:<12.2f} | {found_percent:<20.1f}")
    print("-" * 65)

# --- Main Execution Logic ---

def run_single_solve(args, n):
    """Handles logic for solving a single, user-defined puzzle."""
    initial_state = args.initial
    goal_state = args.goal if args.goal else list(range(1, n*n)) + [0]
    
    if not is_solvable(initial_state, goal_state, n):
        print("\nThis puzzle configuration is NOT SOLVABLE.")
        return
    
    print("\nPuzzle is solvable. Proceeding with search.")
    
    if args.algorithm == 'compare':
        # This functionality is now part of the benchmark report style
        print("\n--- Comparing Algorithms on a Single Puzzle ---")
        run_benchmark(1, n, goal_state, initial_state)
    else:
        print(f"\n--- Solving with {args.algorithm.upper()} ---")
        search_function = SEARCH_ALGORITHMS[args.algorithm]
        start_time = time.perf_counter()
        solution = search_function(initial_state, n, goal_state)
        end_time = time.perf_counter()
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        print_solution(solution)

def run_benchmark(num_puzzles, n, goal_state, predefined_initial=None):
    """Handles logic for the benchmark mode."""
    results = {name: {'times': [], 'moves': [], 'found': 0} for name in SEARCH_ALGORITHMS}

    for i in range(num_puzzles):
        if predefined_initial:
            initial_state = predefined_initial
            print(f"--- Solving Predefined Puzzle ---")
        else:
            print(f"\n--- Solving Puzzle {i + 1}/{num_puzzles} ---")
            initial_state = generate_solvable_puzzle(goal_state, n)

        for name, func in SEARCH_ALGORITHMS.items():
            start_time = time.perf_counter()
            solution = func(initial_state, n, goal_state)
            end_time = time.perf_counter()
            
            if solution:
                results[name]['times'].append(end_time - start_time)
                results[name]['moves'].append(len(solution) - 1)
                results[name]['found'] += 1
            print(f"{name.upper()} finished in {end_time - start_time:.4f}s.")
            
    print_benchmark_summary(results, num_puzzles)

def main():
    n = 4
    parser = argparse.ArgumentParser(
        description="Solve or benchmark the 15-puzzle using various uninformed search algorithms.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--initial',
        type=int,
        nargs='+',
        help='The initial state of the 15-puzzle (16 numbers).'
    )
    group.add_argument(
        '--benchmark',
        type=int,
        metavar='N',
        help='Run a benchmark on N randomly generated, solvable puzzles.'
    )
    parser.add_argument(
        '--goal',
        type=int,
        nargs='+',
        help=f'The goal state (optional, defaults to 1,2,...,15,0).'
    )
    parser.add_argument(
        '--algorithm',
        choices=['bfs', 'dfs', 'iddfs', 'compare'],
        default='compare',
        help="The search algorithm to use for a single solve (default: compare)."
    )

    args = parser.parse_args()
    
    if args.benchmark:
        goal_state = args.goal if args.goal else list(range(1, n*n)) + [0]
        run_benchmark(args.benchmark, n, goal_state)
    else:
        if len(args.initial) != n*n:
            parser.error(f"--initial must contain exactly {n*n} numbers.")
        if args.goal and len(args.goal) != n*n:
            parser.error(f"--goal must contain exactly {n*n} numbers.")
        run_single_solve(args, n)

if __name__ == "__main__":
    main()
