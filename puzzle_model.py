from collections import deque
import numpy as np

class PuzzleNode:
    """Represents a state (node) in the N-puzzle problem."""

    def __init__(self, state, parent, move):
        self.state = state
        self.parent = parent
        self.move = move

    def generate_successors(self, n):
        """Generates all valid successor nodes from the current node."""
        successors = []
        gap_idx = self.state.index(0)
        
        valid_moves = []
        if (gap_idx % n) > 0: valid_moves.append('L')
        if (gap_idx % n) < n - 1: valid_moves.append('R')
        if (gap_idx // n) > 0: valid_moves.append('U')
        if (gap_idx // n) < n - 1: valid_moves.append('D')

        for move in valid_moves:
            new_state = self.state[:]
            if move == 'L': new_state[gap_idx], new_state[gap_idx-1] = new_state[gap_idx-1], new_state[gap_idx]
            elif move == 'R': new_state[gap_idx], new_state[gap_idx+1] = new_state[gap_idx+1], new_state[gap_idx]
            elif move == 'U': new_state[gap_idx], new_state[gap_idx-n] = new_state[gap_idx-n], new_state[gap_idx]
            elif move == 'D': new_state[gap_idx], new_state[gap_idx+n] = new_state[gap_idx+n], new_state[gap_idx]
            successors.append(PuzzleNode(new_state, self, move))
        
        return successors

def format_state(state, n):
    return np.array(state).reshape(n, n)

def is_solvable(initial_state, goal_state, n):
    def count_inversions(state):
        inversions = 0; puzzle = [i for i in state if i != 0]
        for i in range(len(puzzle)):
            for j in range(i + 1, len(puzzle)):
                if puzzle[i] > puzzle[j]: inversions += 1
        return inversions
    initial_inversions, goal_inversions = count_inversions(initial_state), count_inversions(goal_state)
    if n % 2 != 0: return initial_inversions % 2 == goal_inversions % 2
    else:
        initial_blank_row, goal_blank_row = initial_state.index(0)//n, goal_state.index(0)//n
        return (initial_inversions + initial_blank_row) % 2 == (goal_inversions + goal_blank_row) % 2

# --- Path Reconstruction ---
def get_path_from_node(node, n):
    """Traces back from a node to its root to get the path."""
    path = []
    current = node
    while current is not None:
        path.append((current.move, format_state(current.state, n)))
        current = current.parent
    path.reverse()
    return path

# --- Search Algorithms ---
def bfs_search(initial_state, n, goal_state):
    start_node = PuzzleNode(initial_state, None, None)
    q = deque([start_node])
    visited = {tuple(start_node.state)}
    while q:
        current_node = q.popleft()
        if current_node.state == goal_state: return get_path_from_node(current_node, n)
        for successor in current_node.generate_successors(n):
            if tuple(successor.state) not in visited:
                visited.add(tuple(successor.state))
                q.append(successor)
    return None

def bidirectional_search(initial_state, n, goal_state):
    """
    Performs Bidirectional Search, running two BFS searches simultaneously:
    one forward from the initial state, one backward from the goal state.
    """
    if initial_state == goal_state: return [(None, format_state(initial_state, n))]

    # Setup for forward search
    q_fwd = deque([PuzzleNode(initial_state, None, None)])
    visited_fwd = {tuple(initial_state): q_fwd[0]}

    # Setup for backward search
    q_bwd = deque([PuzzleNode(goal_state, None, None)])
    visited_bwd = {tuple(goal_state): q_bwd[0]}

    while q_fwd and q_bwd:
        # Expand forward
        for _ in range(len(q_fwd)):
            node_fwd = q_fwd.popleft()
            for succ in node_fwd.generate_successors(n):
                state_tuple = tuple(succ.state)
                if state_tuple in visited_bwd: # Meeting point found
                    node_bwd = visited_bwd[state_tuple]
                    return join_paths(node_fwd, node_bwd, n)
                if state_tuple not in visited_fwd:
                    visited_fwd[state_tuple] = succ
                    q_fwd.append(succ)
        
        # Expand backward
        for _ in range(len(q_bwd)):
            node_bwd = q_bwd.popleft()
            for succ in node_bwd.generate_successors(n):
                state_tuple = tuple(succ.state)
                if state_tuple in visited_fwd: # Meeting point found
                    node_fwd = visited_fwd[state_tuple]
                    return join_paths(node_fwd, node_bwd, n)
                if state_tuple not in visited_bwd:
                    visited_bwd[state_tuple] = succ
                    q_bwd.append(succ)
    return None

def join_paths(node_fwd, node_bwd, n):
    """Joins the paths from the initial and goal states at the meeting point."""
    path_fwd = get_path_from_node(node_fwd, n)
    
    # We need to construct the path from the meeting point to the goal
    path_bwd_to_goal = []
    curr = node_bwd
    inv_moves = {'L': 'R', 'R': 'L', 'U': 'D', 'D': 'U'}
    while curr.parent is not None:
        # The move stored is for the backward path, so we invert it for the final forward path
        inverted_move = inv_moves[curr.move]
        path_bwd_to_goal.append((inverted_move, format_state(curr.parent.state, n)))
        curr = curr.parent
        
    return path_fwd + path_bwd_to_goal

def iddfs_search(initial_state, n, goal_state):
    start_node = PuzzleNode(initial_state, None, None)
    def dls(node, depth, visited):
        if node.state == goal_state: return node
        if depth <= 0: return None
        visited.add(tuple(node.state))
        for successor in node.generate_successors(n):
            if tuple(successor.state) not in visited:
                found = dls(successor, depth - 1, visited)
                if found: return found
        return None
    for depth in range(100):
        visited = set()
        result_node = dls(start_node, depth, visited)
        if result_node: return get_path_from_node(result_node, n)
    return None
