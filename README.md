AI Assignment 1
Name - Viresh Gupta
Roll No. - 2016118

##  Q1. N-puzzle for n=8,15,24
###  Assumptions:
    - The goal state has numbers in increasing order 
      Example goal state:
      0,1,2
      3,4,5
      6,7,8
    - Input is comma delimited

###  Methodology:
    Four algorithms are implemented:
        1. BFS
        2. DFS
        3. A*
        4. IDA*
    In each of the algorithm, a common state space representation is used so that the execution parameters can
    be compared only on the basis of the differences in the algorithm and get least affected by other parameters.

    i.e A boad class is used to represent the puzzle board configuration at any given point of time.
    In all functions, wherever necessary to keep track of visited nodes, I have used the string representation of
    row major format of the board matrix.


### Observation(s):
    Input state:
        1,4,2
        3,0,5
        6,7,8

    Output:
    {
        "bfs": {
            "elapsed_time": 0.0025424159975955263,
            "iters": 9,
            "path_length": 2
        },
        "dfs": {
            "elapsed_time": 4.680093126000429,
            "iters": 127975,
            "path_length": 54710
        },
        "A*": {
            "elapsed_time": 0.00021842400019522756,
            "iters": 3,
            "path_length": 2
        },
        "IDA*": {
            "elapsed_time": 0.00020356200184323825,
            "iters": 3,
            "path_length": 2
        }
    }



    Input:
        1,8,2
        0,4,3
        7,6,5

    Output:
    {
        "bfs": {
            "elapsed_time": 3.3275238839996746,
            "iters": 71952,
            "path_length": 21
        },
        "dfs": {
            "elapsed_time": 4.241534632001276,
            "iters": 115693,
            "path_length": 61473
        },
        "A*": {
            "elapsed_time": 0.05477593199975672,
            "iters": 869,
            "path_length": 21
        },
        "IDA*": {
            "elapsed_time": 0.15475486300056218,
            "iters": 2842,
            "path_length": 29
        }
    }


    Input:
        0,1,2
        4,7,8
        3,5,6

    Output:
    No Solution found !
    {
        "bfs": {
            "elapsed_time": 8.118177871998341,
            "iters": 0,
            "path_length": 0
        },
        "dfs": {
            "elapsed_time": 6.584858198999427,
            "iters": 0,
            "path_length": 0
        },
        "A*": {
            "elapsed_time": 18.829530777999025,
            "iters": 0,
            "path_length": 0
        },
        "IDA*": {
            "elapsed_time": 39.71716351700161,
            "iters": 0,
            "path_length": 0
        }
    }

    Input:
        4,1,3,0
        8,6,2,7
        9,5,10,11
        12,13,14,15
    Output:
    {
        "bfs": {
            "elapsed_time": 0.05562116700093611,
            "iters": 340,
            "path_length": 7
        },
        "A*": {
            "elapsed_time": 0.0006580589979421347,
            "iters": 8,
            "path_length": 7
        },
        "IDA*": {
            "elapsed_time": 0.0007906860009825323,
            "iters": 9,
            "path_length": 7
        }
    }

Also for more complicated inputs of higher dimensions (15 puzzle and 24 puzzle), (especially where no solution exists)
the algorithms are taking unreasonable amounts of time to complete and hence only simple cases were tested.


### Results:
    From the above observations, clearly the order of efficiency in case a solution exists can be
    said as
    A* > IDA* > BFS > DFS

    DFS often gets lost in the depths of a branch and fails to find an easily available solution at a
    lower depth

    BFS Always finds the optimal path, but it is not checking for paths effectively.

    Graph A* performs very well in all the algorithms, since the heuristic used is admissible and consistent.
    Thus it usually needs to perform very less iterations to find a solution.

    Graph IDA* also performs better than BFS in the number of intermediate solutions it needs to examine, but still
    is not as good as A* because it revisits several nodes repeatedly.


##  Q2. Modify an nxn coloured board so that no two neighbouring colours are same

### Strategies used:
    I have impelemented A* search and BFS search for this problem.

    The heuristic used is the number of tiles that have a matching neighbouring colour.

    Sample Input:
    4
    R,R,B,B
    Y,R,G,Y
    R,Y,B,Y
    Y,B,G,R

    Sample output stats:
    {
        "bfs": {
            "elapsed_time": 0.03545345800012001,
            "iters": 24,
            "path_length": 2
        },
        "A*": {
            "elapsed_time": 0.0023412629998347256,
            "iters": 3,
            "path_length": 2
        }
    }

### Observation:

    Just like the previous problem, A* can solve this problem with the help of heuristics efficiently
    and is better than a BFS.
