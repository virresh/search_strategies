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
        self.blank_tile = None

    def __eq__(self, other):
        return self.find_manhattan_dist() == other.find_manhattan_dist()
    def __lt__(self, other):
        # return self.size < other.size
        return self.find_manhattan_dist() < other.find_manhattan_dist()

    def is_goal_state(self):
        # determine if the board is in the goal state currently
        val = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.state[i][j] != val:
                    return False
                val+=1
        return True

    def find_manhattan_dist(self):
        # return 50
        dist = 0
        val = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.state[i][j] != val:
                    hypo_i = self.state[i][j]-1 // self.size
                    hypo_j = self.state[i][j]-1 % self.size
                    dist += abs(hypo_i-i) + abs(hypo_j-j)
                val += 1
        return dist

    def input_state(self):
        n = self.size
        print('Enter the puzzle Board state as {0}x{0} matrix, elements separated by a {1}:'.format(n, '","'))
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
                if str(self.state[i][j]).strip() == '':
                    self.state[i][j] = 0
                else:
                    self.state[i][j] = int(str(self.state[i][j]).strip())
                vals.append(self.state[i][j])
                if self.state[i][j] == 0:
                    self.blank_tile = (i,j)
        for i in range(0, self.size * self.size):
            if i not in vals:
                raise AssertionError('Invalid values in the Board')

    def print_state(self):
        n = self.size
        print('Board state: ')
        for i in range(0, n):
            print(self.state[i])
        # for i in range(0, n):
        #   for j in range(0, n):
        #       print(self.state[i][j], end=' ')
        #   print('')

    def generate_states(self):
        curr = self.blank_tile
        n = self.size
        new_states = []
        if curr[0]+1 < n :
            # down state
            nboard = Board(n)
            nboard.state = copy.deepcopy(self.state)
            n_blank = (curr[0]+1, curr[1])
            nboard.blank_tile = n_blank
            nboard.state[curr[0]][curr[1]], nboard.state[n_blank[0]][n_blank[1]] = nboard.state[n_blank[0]][n_blank[1]], nboard.state[curr[0]][curr[1]]
            new_states.append(nboard)
        if curr[0]-1 >= 0 :
            # up state
            nboard = Board(n)
            nboard.state = copy.deepcopy(self.state)
            n_blank = (curr[0]-1, curr[1])
            nboard.blank_tile = n_blank
            nboard.state[curr[0]][curr[1]], nboard.state[n_blank[0]][n_blank[1]] = nboard.state[n_blank[0]][n_blank[1]], nboard.state[curr[0]][curr[1]]
            new_states.append(nboard)
        if curr[1]-1 >= 0 :
            # left state
            nboard = Board(n)
            nboard.state = copy.deepcopy(self.state)
            n_blank = (curr[0], curr[1]-1)
            nboard.blank_tile = n_blank
            nboard.state[curr[0]][curr[1]], nboard.state[n_blank[0]][n_blank[1]] = nboard.state[n_blank[0]][n_blank[1]], nboard.state[curr[0]][curr[1]]
            new_states.append(nboard)
        if curr[1]+1 < n :
            # right state
            nboard = Board(n)
            nboard.state = copy.deepcopy(self.state)
            n_blank = (curr[0], curr[1]+1)
            nboard.blank_tile = n_blank
            nboard.state[curr[0]][curr[1]], nboard.state[n_blank[0]][n_blank[1]] = nboard.state[n_blank[0]][n_blank[1]], nboard.state[curr[0]][curr[1]]
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
    parent = {}

    while(len(qu) != 0):
        itr[0]+=1
        cst, depth = qu.pop(0)
        if cst.is_goal_state():
            itr[1] = depth
            # print_path(parent, cst, cur_state)
            return cst
        for state in cst.generate_states():
            y = repr(state.state)
            if y not in visited:
                visited.add(y)
                parent[y] = cst
                qu.append((state, depth+1))

    return None

## DFS Algorithm
@profile(store='dfs')
def dfs(cur_state, visited, itr):
    print('DFS Initial ', end='')
    cur_state.print_state()

    stk = []
    stk.append((cur_state, 0))

    while(len(stk) != 0):
        itr[0]+=1
        cst, depth = stk.pop()
        if cst.is_goal_state():
            itr[1] = depth
            return cst
        for state in cst.generate_states():
            y = repr(state.state)
            if y not in visited:
                visited.add(y)
                stk.append((state, depth+1))

    return None

def print_path(parents, goal, initial):
    # print(parents)
    temp = goal
    while repr(temp.state) in parents.keys() and repr(temp.state) != repr(initial.state):
        temp.print_state()
        temp = parents[repr(temp.state)]
    temp.print_state()

## A* Algorithm
@profile(store='A*')
def a_star(cur_state, visited, itr):
    print('A* Initial ', end='')
    cur_state.print_state()

    hp = []
    heapq.heappush(hp, (0+cur_state.find_manhattan_dist(), 0, cur_state))
    parent = {}
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
                parent[y] = cst
                cost = cur_steps+1+state.find_manhattan_dist()
                heapq.heappush(hp, (cost, cur_steps+1, state))

    return None

## IDA* Algorithm
@profile(store='IDA*')
def ida_star(cur_state, visited, itr):
    print('IDA* Initial ', end='')
    cur_state.print_state()
    hp = [cur_state.find_manhattan_dist()]
    thresh = hp[0]
    print(thresh)
    while(len(hp) != 0 and thresh <= ((cur_state.size)**4) ):
        stack = [(cur_state, 0)]
        visited = set()
        visited.add(repr(cur_state.state))
        thresh = min(hp)
        print(thresh)
        hp = []
        while(len(stack) != 0):
            itr[0]+=1
            cst, depth = stack.pop()
            if cst.is_goal_state():
                itr[1] = depth
                return cst
            for state in cst.generate_states()[::-1]:
                y = repr(state.state)
                fcost = state.find_manhattan_dist() + depth
                if y not in visited and fcost <= thresh:
                    visited.add(repr(state.state))
                    stack.append((state, depth+1))
                elif fcost > thresh:
                    hp.append(fcost)
    return None

##  Main Functions and Input/Output routines

board = Board(int(input('Enter Board Size: ')))
board.input_state()

bfs(board)
dfs(board)
a_star(board)
ida_star(board)

print(json.dumps(stats, indent = 4))
