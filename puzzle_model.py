from collections import deque
import numpy as np

class PuzzleNode:
    """Represents a state (node) in the N-puzzle problem."""

    def __init__(self, state, parent, move, goal_state):
        self.state = state
        self.parent = parent
        self.move = move
        self.goal_state = goal_state
        self.depth = parent.depth + 1 if parent else 0

    def is_goal(self):
        """Check if the current state is the goal state."""
        return self.state == self.goal_state

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
            if move == 'L':
                new_state[gap_idx], new_state[gap_idx - 1] = new_state[gap_idx - 1], new_state[gap_idx]
            elif move == 'R':
                new_state[gap_idx], new_state[gap_idx + 1] = new_state[gap_idx + 1], new_state[gap_idx]
            elif move == 'U':
                new_state[gap_idx], new_state[gap_idx - n] = new_state[gap_idx - n], new_state[gap_idx]
            elif move == 'D':
                new_state[gap_idx], new_state[gap_idx + n] = new_state[gap_idx + n], new_state[gap_idx]
            
            successors.append(PuzzleNode(new_state, self, move, self.goal_state))
        
        return successors

    def get_solution_path(self, n):
        """Traces back from the goal node to the start node to find the solution path."""
        path = []
        current = self
        while current is not None:
            path.append((current.move, format_state(current.state, n)))
            current = current.parent
        path.reverse()
        return path

def format_state(state, n):
    """Converts a state list into a formatted numpy array for display."""
    return np.array(state).reshape(n, n)

def is_solvable(initial_state, goal_state, n):
    """Checks if the N-puzzle is solvable using inversion count."""
    def count_inversions(state):
        inversions = 0
        puzzle = [i for i in state if i != 0]
        for i in range(len(puzzle)):
            for j in range(i + 1, len(puzzle)):
                if puzzle[i] > puzzle[j]:
                    inversions += 1
        return inversions

    initial_inversions = count_inversions(initial_state)
    goal_inversions = count_inversions(goal_state)

    if n % 2 != 0:
        return initial_inversions % 2 == goal_inversions % 2
    else:
        initial_blank_row = initial_state.index(0) // n
        goal_blank_row = goal_state.index(0) // n
        return (initial_inversions + initial_blank_row) % 2 == (goal_inversions + goal_blank_row) % 2

# --- Search Algorithms ---

def bfs_search(initial_state, n, goal_state):
    """Performs Breadth-First Search (BFS)."""
    start_node = PuzzleNode(initial_state, None, None, goal_state)
    q = deque([start_node])
    visited = {tuple(start_node.state)}

    while q:
        current_node = q.popleft()
        if current_node.is_goal():
            return current_node.get_solution_path(n)
        
        for successor in current_node.generate_successors(n):
            if tuple(successor.state) not in visited:
                visited.add(tuple(successor.state))
                q.append(successor)
    return None

def dfs_search(initial_state, n, goal_state):
    """Performs Depth-First Search (DFS). Not optimal and can be very slow."""
    start_node = PuzzleNode(initial_state, None, None, goal_state)
    stack = [start_node]
    visited = {tuple(start_node.state)}

    while stack:
        current_node = stack.pop()
        if current_node.is_goal():
            return current_node.get_solution_path(n)
        
        for successor in reversed(current_node.generate_successors(n)):
            if tuple(successor.state) not in visited:
                visited.add(tuple(successor.state))
                stack.append(successor)
    return None

def iddfs_search(initial_state, n, goal_state):
    """Performs Iterative Deepening Depth-First Search (IDDFS)."""
    start_node = PuzzleNode(initial_state, None, None, goal_state)
    
    def dls(node, depth, visited):
        """Depth-Limited Search helper."""
        if node.is_goal(): return node
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
        if result_node:
            return result_node.get_solution_path(n)
    return None
