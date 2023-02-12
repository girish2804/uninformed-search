from queue import Queue
import numpy as np
import random

def search(initial, n, goal):
    start = node(initial,None,None,goal)
    visited = []
    if start.goal_():
        return start.solution()
    q = Queue()
    q.put(start)

    while q.empty() == False:
        nd = q.get()
        visited.append(nd.state)
        suc = nd.succ(n)
        for i in suc:
            if i.state not in visited:
                #display(i,n)
                if i.goal_():
                    return i.solution()
                q.put(i) 
    return

def nxt(gap,n):
    available_moves = ['L','R','U','D']
    if (gap % n) == 0:
        available_moves.remove('L')
    if gap % n == n-1:
        available_moves.remove('R')
    if gap - n < 0:
        available_moves.remove('U')
    if (gap + n) > (n*n - 1):
        available_moves.remove('D')
    
    return available_moves

class node:
    goal = []
    state = []

    def solution(self):
        sol = []
        sol.append(display(self,n))
        sol.append(self.prev_move)
        x = self
        while x.parent != None:
            x= x.parent
            sol.append(display(x,n))
            sol.append(x.prev_move)
        sol.pop()
        sol.reverse()
        return sol
    
    def set_goal(self,g):
        self.goal = g

    def __init__(self,st,prev_mov,par,final):
        self.state = st
        self.prev_move = prev_mov
        self.parent = par
        self.goal = final

    def goal_(self):
        if self.state == self.goal:
            return True
        else:
            return False
    
    def path(self):
        pat = []
        pat.append()
    
    def succ(self, n):
        successors = []
        gap_idx = self.state.index(0)
        moves = nxt(gap_idx,n)

        for i in moves:
            new = self.state.copy()
            prev = ''
            if i == 'L':
                new[gap_idx]=new[gap_idx-1]
                new[gap_idx-1]=0
                prev = 'left'
            elif i == 'R':
                new[gap_idx]=new[gap_idx+1]
                new[gap_idx+1]=0
                prev = 'rigt'
            elif i == 'U':
                new[gap_idx]=new[gap_idx-n]
                new[gap_idx-n]=0
                prev = 'up'
            elif i == 'D':
                new[gap_idx]=new[gap_idx+n]
                new[gap_idx+n]=0
                prev = 'down'

            successors.append(node(new,prev,self,self.goal))
        
        return successors

def display(x,n):
    res = np.zeros([n,n], dtype=int)
    for i in range(0,n*n):
        r = int(i/n)
        c = i%n
        res[r][c] = x.state[i]
    
    return res

def is_solvable(ins,n):
    puzzle = ins.state
    f = ins.goal
    count = 0
    count2 = 0
    for i in range(0,n*n-1):
        for j in range(i+1,n*n):
            if((puzzle[i]>puzzle[j]) and puzzle[i] and puzzle[j]):
                count += 1
    if(count%2 == 0):
        init_parity = 1
    else:
        init_parity = 0
    
    for i in range(0,n*n-1):
        for j in range(i+1,n*n):
            if((puzzle[i]>puzzle[j]) and puzzle[i] and puzzle[j]):
                count += 1
    if(count%2 == 0):
        g_parity = 1
    else:
        g_parity = 0
    
    if n%2!=0 and init_parity!=g_parity:
        return False
    else:
        return True

n = 4

# initial = random.sample(range(16),16)
# initial = [5, 1, 3, 4, 0, 2, 6, 8, 9, 10, 7, 11, 13, 14, 15, 12]
initial = []
print('enter initial board row wise \n --input all the numbers in first row then move to next rows)')
for i in range(0,n*n):
    initial.append(int(input()))

final = []
print('enter final board row wise \n --input all the numbers in first row then move to next rows)')
for i in range(0,n*n):
    final.append(int(input()))

# print('initial board: \n')
# display(initial,n)
root = node(initial,None,None,final)
# print('goal board: ')
# display(final,n)

if initial == final:
    print('puzzle')

if is_solvable(root,n):
    sol = search(initial,n,final)
    print('solution to the puzzle is:\n')
    print(*sol, sep = '- \n')
    print('goal reached')
else:
    print('puzzle is not sovable\n')