#!/usr/bin/python3
import copy
import heapq
import json

from timeit import default_timer as timer
import os
import psutil

##  Helper Classes and variables
stats = {}

## ---> Profiling functions and decorator
def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

def profile(store):
    def prof_stor(func):
        def wrapper(*args, **kwargs):
            mem_before = get_process_memory()
            visited = set()
            itr = [0,0]
            start = timer()
            try:
                result = func(*args, visited, itr, **kwargs)
            except Exception as e:
                print(e)
                result = None
            elapsed_time = timer() - start
            mem_after = get_process_memory()
            
            if result and store:
                print('Final ', end='')
                result.print_state()
                stats[store]= {
                    'elapsed_time' : elapsed_time,
                    # 'memory' : mem_after - mem_before,
                    'iters' : itr[0],
                    'path_length': itr[1],
                    }
            else:
                print('No Soluton found !')
                stats[store]= {
                    'elapsed_time' : elapsed_time,
                    # 'memory' : mem_after - mem_before,
                    'iters' : 0,
                    'path_length': 0,
                    }
            return result
        return wrapper
    return prof_stor
## ^^ Simple decorator to make tracking execution time and other statistics easy

class Board:
    def __init__(self, n: int):
        self.size = n
        self.state = []

    def __eq__(self, other):
        return self.h() == other.h()
    def __lt__(self, other):
        return self.h() < other.h()

    def is_goal_state(self):
        # determine if the board is in the goal state currently
        return self.h() == 0

    def h(self):
        dist = 0
        val = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                dir_x = [1,0,-1,0]
                dir_y = [0,1,0,-1]
                for k in range(0, 4):
                    new_x = i+dir_x[k]
                    new_y = j+dir_y[k]
                    if new_x >=0 and new_x <self.size and new_y >=0 and new_y < self.size:
                        if self.state[new_x][new_y] == self.state[i][j]:
                            dist+=1
        return dist

    def input_state(self):
        n = self.size
        print('Enter the colour Board state as {0}x{0} matrix, elements separated by a {1}:'.format(n, '","'))
        for i in range(0, n):
            row = input().split(',')
            self.state.append(row)
        self.validate_input()

    def validate_input(self):
        vals = []
        for i in range(0, self.size):
            # print(self.state[i])
            if len(self.state[i]) != self.size:
                raise AssertionError('Board specified is not square')
        for i in range(0, self.size):
            for j in range(0, self.size):
                if str(self.state[i][j]).strip() not in ['R','G','B','Y']:
                    raise AssertionError('Invalid Colour')
                else:
                    self.state[i][j] = str(self.state[i][j]).strip()

    def print_state(self):
        n = self.size
        print('Board state: ')
        for i in range(0, n):
            print(self.state[i])

    def generate_states(self):
        n = self.size
        new_states = []
        for i in range(0, n):
            for j in range(0, n):
                dir_x = [1,0,-1,0]
                dir_y = [0,1,0,-1]
                bad = False
                for k in range(0, 4):
                    new_x = i+dir_x[k]
                    new_y = j+dir_y[k]
                    if new_x >=0 and new_x <self.size and new_y >=0 and new_y < self.size:
                        if self.state[new_x][new_y] == self.state[i][j]:
                            bad = True
                if not bad:
                    continue
                for k in range(0, 4):
                    new_x = i+dir_x[k]
                    new_y = j+dir_y[k]
                    if new_x >=0 and new_x <self.size and new_y >=0 and new_y < self.size:
                        if self.state[new_x][new_y] != self.state[i][j]:
                            nboard = Board(n)
                            nboard.state = copy.deepcopy(self.state)
                            nboard.state[new_x][new_y], nboard.state[i][j] = nboard.state[i][j], nboard.state[new_x][new_y]
                            new_states.append(nboard)
        return new_states

########################
##  Search Algorithms ##
########################

## BFS Algorithm
@profile(store='bfs')
def bfs(cur_state, visited, itr):
    print('BFS Initial ', end='')
    cur_state.print_state()

    qu = []
    qu.append((cur_state, 0))
    # parent = {}

    while(len(qu) != 0):
        itr[0]+=1
        cst, depth = qu.pop(0)
        if cst.is_goal_state():
            itr[1] = depth
            return cst
        for state in cst.generate_states():
            y = repr(state.state)
            if y not in visited:
                visited.add(y)
                # parent[y] = cst
                qu.append((state, depth+1))

    return None

# def print_path(parents, goal, initial):
#     # print(parents)
#     temp = goal
#     while repr(temp.state) in parents.keys() and repr(temp.state) != repr(initial.state):
#         temp.print_state()
#         temp = parents[repr(temp.state)]
#     temp.print_state()

## A* Algorithm
@profile(store='A*')
def a_star(cur_state, visited, itr):
    print('A* Initial ', end='')
    cur_state.print_state()

    hp = []
    heapq.heappush(hp, (0+cur_state.h(), 0, cur_state))
    # parent = {}
    while(len(hp) != 0):
        itr[0]+=1
        top_ele = heapq.heappop(hp)
        cst = top_ele[2]
        if cst.is_goal_state():
            itr[1] = top_ele[1]
            # print_path(parent, cst, cur_state)
            return cst
        cur_steps = top_ele[1]
        for state in cst.generate_states():
            y = repr(state.state)
            if y not in visited:
                visited.add(y)
                # parent[y] = cst
                cost = cur_steps+1+state.h()
                heapq.heappush(hp, (cost, cur_steps+1, state))

    return None

##  Main Functions and Input/Output routines

board = Board(int(input('Enter Board Size: ')))
board.input_state()
# print(board.h())
# for state in board.generate_states():
#     state.print_state()
bfs(board)
a_star(board)

print(json.dumps(stats, indent = 4))
