from definitions import *
import heapq, time

def shortestPath(maze, mazeW, start=None, end=None):
    n, m = len(maze),len(maze[0])
    if start == None: i0,j0, entrWall = (0,0, LEFT)
    else:             i0,j0, entrWall = start
    if end == None:   iF,jF, exitWall = (n-1,m-1, RIGHT)
    else:             iF,jF, exitWall = end

    weights = {}
    hweights = [(0, (i0, j0))]

    for i in range(n):
        for j in range(m):
            #Set all weights to infinite excluding pos (i0,j0)
            if i != i0 or j != j0:
                weights[(i,j)] = float("inf")
            else:
                # Rewrite weight of vertex (i0,j0) to simplify
                # shortest path code
                weights[(i0,j0)] = 0

    parent = {}
    parent [(i0,j0)] = None

    ##Relaxation
    while weights: # total loops = n*m
        u = heapq.heappop(hweights)[1]
        uW = weights.pop(u)

        for v in detectMoves(u, maze):
            vi, vj = v
            if weights.get(v) > uW + mazeW[vi][vj]:
                weights[v] = uW + mazeW[vi][vj]
                heapq.heappush(hweights,(weights[v],v))
                parent[v] = u



    # some horrible code, sorry :/
    if exitWall != NOTHING:
        if exitWall == LEFT:  path = [(iF,   jF-1), (iF, jF)]
        if exitWall == UP:    path = [(iF-1, jF),   (iF, jF)]
        if exitWall == RIGHT: path = [(iF,   jF+1), (iF, jF)]
        if exitWall == DOWN:  path = [(iF+1, jF),   (iF, jF)]
    else: path = [(iF, jF)]
    #

    p = parent[path[-1]]
    while p is not None:
        path.append(p)
        p = parent[path[-1]]

    # continuation of the horrible code, sorry :/
    if entrWall != NOTHING:
        if entrWall == LEFT:  path.append( (i0,   j0-1) )
        if entrWall == UP:    path.append( (i0-1, j0  ) )
        if entrWall == RIGHT: path.append( (i0,   j0+1) )
        if entrWall == DOWN:  path.append( (i0+1, j0  ) )
    #

    path.reverse()

    return path

def detectMoves((i, j), maze):
    n,m = len(maze),len(maze[0])
    nextMoves = []
    if j>0   and not existWall(LEFT,  maze[i][j]): nextMoves.append( (i,j-1) )
    if i>0   and not existWall(UP,    maze[i][j]): nextMoves.append( (i-1,j) )
    if j<m-1 and not existWall(RIGHT, maze[i][j]): nextMoves.append( (i,j+1) )
    if i<n-1 and not existWall(DOWN,  maze[i][j]): nextMoves.append( (i+1,j) )

    return nextMoves
