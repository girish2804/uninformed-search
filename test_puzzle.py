import time
import argparse
import random
import numpy as np
import multiprocessing
from puzzle_model import bfs_search, bidirectional_search, iddfs_search, is_solvable

# --- Configuration ---
SEARCH_ALGORITHMS = {"bfs": bfs_search, "bidi": bidirectional_search, "iddfs": iddfs_search}
BENCHMARK_TIMEOUT_SECONDS = 15

# --- Puzzle Generation ---
def generate_solvable_puzzle(goal_state, n, shuffles=30):
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
        if move == 'L': state[gap_idx], state[gap_idx-1] = state[gap_idx-1], state[gap_idx]; last_move = 'L'
        elif move == 'R': state[gap_idx], state[gap_idx+1] = state[gap_idx+1], state[gap_idx]; last_move = 'R'
        elif move == 'U': state[gap_idx], state[gap_idx-n] = state[gap_idx-n], state[gap_idx]; last_move = 'U'
        elif move == 'D': state[gap_idx], state[gap_idx+n] = state[gap_idx+n], state[gap_idx]; last_move = 'D'
    return state

# --- Worker for Multiprocessing ---
def solve_puzzle_worker(queue, algo_func, initial_state, n, goal_state):
    solution = algo_func(initial_state, n, goal_state)
    queue.put(solution)

# --- Reporting ---
def print_solution(solution_path):
    if not solution_path: print("No solution was found."); return
    print(f"\n--- Solution Found in {len(solution_path) - 1} moves ---")
    print(f"Initial State:\n{solution_path[0][1]}")
    print(f"\n--- Goal Reached! ---\nFinal State:\n{solution_path[-1][1]}")

def print_benchmark_summary(results, num_puzzles):
    print("\n" + "="*70)
    print(f"Benchmark Summary ({num_puzzles} puzzles, {BENCHMARK_TIMEOUT_SECONDS}s timeout per run)")
    print("="*70)
    print(f"{'Algorithm':<10} | {'Avg Time (s)':<15} | {'Avg Moves':<12} | {'Goals Found (%)':<20}")
    print("-" * 70)
    for name, data in results.items():
        avg_time = np.mean(data['times']) if data['times'] else 0
        avg_moves = np.mean(data['moves']) if data['moves'] else 0
        found_percent = (data['found'] / num_puzzles) * 100
        print(f"{name.upper():<10} | {avg_time:<15.6f} | {avg_moves:<12.2f} | {found_percent:<20.1f}")
    print("-" * 70)

# --- Main Execution Logic ---
def run_benchmark(num_puzzles, n, goal_state):
    results = {name: {'times': [], 'moves': [], 'found': 0} for name in SEARCH_ALGORITHMS}
    for i in range(num_puzzles):
        print(f"\n--- Solving Puzzle {i + 1}/{num_puzzles} ---")
        initial_state = generate_solvable_puzzle(goal_state, n)
        for name, func in SEARCH_ALGORITHMS.items():
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=solve_puzzle_worker, args=(q, func, initial_state, n, goal_state))
            start_time = time.perf_counter()
            p.start()
            p.join(BENCHMARK_TIMEOUT_SECONDS)
            if p.is_alive():
                p.terminate(); p.join()
                print(f"{name.upper():<6} -> TIMEOUT")
                results[name]['times'].append(BENCHMARK_TIMEOUT_SECONDS)
            else:
                end_time = time.perf_counter()
                solution = q.get()
                if solution:
                    elapsed_time = end_time - start_time
                    moves = len(solution) - 1
                    print(f"{name.upper():<6} -> Found in {elapsed_time:.4f}s ({moves} moves)")
                    results[name]['times'].append(elapsed_time)
                    results[name]['moves'].append(moves)
                    results[name]['found'] += 1
                else:
                    print(f"{name.upper():<6} -> FAILED (No solution found)")
                    results[name]['times'].append(end_time - start_time)
    print_benchmark_summary(results, num_puzzles)

def main():
    n = 4
    parser = argparse.ArgumentParser(description="Solve or benchmark the 15-puzzle.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--initial', type=int, nargs='+', help='A single initial state to solve.')
    group.add_argument('--benchmark', type=int, metavar='N', help='Run a benchmark on N random puzzles.')
    parser.add_argument('--goal', type=int, nargs='+', help='The goal state (optional).')
    parser.add_argument('--algorithm', choices=SEARCH_ALGORITHMS.keys(), default='bidi', help="Algorithm for single solve.")
    
    args = parser.parse_args()
    goal_state = args.goal if args.goal else list(range(1, n*n)) + [0]
    
    if args.benchmark:
        run_benchmark(args.benchmark, n, goal_state)
    else:
        if len(args.initial) != n*n: parser.error(f"--initial must have {n*n} numbers.")
        if not is_solvable(args.initial, goal_state, n):
            print("\nThis puzzle is NOT SOLVABLE."); return
        
        search_function = SEARCH_ALGORITHMS[args.algorithm]
        print(f"\n--- Solving with {args.algorithm.upper()} ---")
        solution = search_function(args.initial, n, goal_state)
        print_solution(solution)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
