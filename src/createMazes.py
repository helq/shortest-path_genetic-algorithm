#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from random import randint, random
from definitions import *

def detectValidMoves(i, j, n, m, prevMove):
    nextMoves = []

    if not (prevMove==LEFT  or j==m-1):
        nextMoves.append(RIGHT)
    if not (prevMove==UP    or i==n-1):
        nextMoves.append(DOWN)
    if not (prevMove==RIGHT or j==0):
        nextMoves.append(LEFT)
    if not (prevMove==DOWN  or i==0):
        nextMoves.append(UP)

    return nextMoves


# create a random Maze. Height `n' and Width `m'
# return a matriz with walls (numbers)
def createRandomMaze(n, m, entrance=None, exit=None):
    if entrance==None:
        entrance = (0,0, LEFT)
    if exit==None:
        exit = (n-1,m-1, RIGHT)

    # creating a maze with all the walls setted (is writte correctly?)
    maze = [[ALLWALLS]*m for i in range(n)]

    # better than recursion
    stack = [ (randint(0,n-1), randint(0,m-1),
                randomizeList([LEFT, UP, RIGHT, DOWN])) ]
    i,j = stack[0][:2]
    addMark(maze, i, j)

    while stack != []:
        (i,j, moves) = stack.pop()
        mov, moves = moves[0], moves[1:]

        # if there still paths from this position
        if moves != []:
            stack.append( (i,j, moves) )

        # which move now
        if   mov == LEFT:
            if j > 0 and not isMarked(maze[i][j-1]):
                quitWall(LEFT , maze, i, j)
                addMark(maze, i, j-1)
                quitWall(RIGHT, maze, i, j-1)
                ms = detectValidMoves(i, j, n, m, LEFT)
                stack.append( (i,j-1, randomizeList(ms)) )

        elif mov == UP:
            if i > 0 and not isMarked(maze[i-1][j]):
                quitWall(UP  , maze, i, j)
                addMark(maze, i-1, j)
                quitWall(DOWN, maze, i-1, j)
                ms = detectValidMoves(i, j, n, m, UP)
                stack.append( (i-1,j, randomizeList(ms)) )

        elif mov == RIGHT:
            if j < m-1 and not isMarked(maze[i][j+1]):
                quitWall(RIGHT, maze, i, j)
                addMark(maze, i, j+1)
                quitWall(LEFT , maze, i, j+1)
                ms = detectValidMoves(i, j, n, m, RIGHT)
                stack.append( (i,j+1, randomizeList(ms)) )

        elif mov == DOWN:
            if i < n-1 and not isMarked(maze[i+1][j]):
                quitWall(DOWN, maze, i, j)
                addMark(maze, i+1, j)
                quitWall(UP  , maze, i+1, j)
                ms = detectValidMoves(i, j, n, m, DOWN)
                stack.append( (i+1,j, randomizeList(ms)) )

        if random() < 0.05 and len(stack) > 6:
            from math import floor
            t = stack.pop( int(floor( len(stack)*random()**3 )) )
            stack.append( t )

    # quitting marks
    for i in range(n):
        for j in range(m):
            quitMark(maze, i, j)

    # walls of start and finish
    i, j, wall = entrance
    quitWall(wall, maze, i, j)
    i, j, wall = exit
    quitWall(wall, maze, i, j)

    return maze

WALL = 1
NO_WALL = 0
def createRandomWeight(n, m, height=4):
    # from printMazes import generateBasePNG

    np, mp = height, (height*m)/n
    mazeWeight = [[random() for j in range(m)] for i in range(n)]

##    from src.printMazes import generateBasePNG
##    mazeMask = createRandomMaze(np, mp)
##    bMask = [[1-r for r in x ]for x in generateBasePNG(mazeMask)]
    bMask = _generateBaseMask(np, mp)
    mask = _upscale2(bMask, n, m)

    for i in range(n):
        for j in range(m):
            mazeWeight[i][j] *= (1 + mask[i][j]*3)

    return mazeWeight, mask

def _upscale2(reticula, n, m):
    np, mp = len(reticula), len(reticula[0])
    toRet = [[0]*m for i in range(n)]

    factorN, factorM = float(np-1)/(n-1), float(mp-1)/(m-1)
    for i in range(n):
        for j in range(m):
            iN, jM = i*factorN, j*factorM
            x, y = int(iN), int(jM)
            if i == n-1: x = np-2
            if j == m-1: y = mp-2
            ul = (x,   y,   reticula[x][y])
            ur = (x,   y+1, reticula[x][y+1])
            dl = (x+1, y,   reticula[x+1][y])
            dr = (x+1, y+1, reticula[x+1][y+1])
            toRet[i][j] = bilinear_interpolation(iN, jM, [ul, ur, dl, dr])

    return toRet

def bilinear_interpolation(x, y, points):
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

def _generateBaseMask(np, mp):
    mazeMask = createRandomMaze(np, mp)

    bMask = [ [WALL]*(2*mp-1) for i in range(2*np-1)]

    # destroying walls
    for i in range(np-1):
        for j in range(mp-1):
            if not existWall(DOWN, mazeMask[i][j]):
                bMask[2*i+1][2*j] = NO_WALL
            if not existWall(RIGHT, mazeMask[i][j]):
                bMask[2*i][2*j+1] = NO_WALL

            bMask[2*i][2*j] = NO_WALL

    for i in range(np-1):
        if not existWall(DOWN, mazeMask[i][mp-1]):
            bMask[2*i+1][2*(mp-1)] = NO_WALL
        bMask[2*i][2*(mp-1)] = NO_WALL
    for j in range(mp-1):
        if not existWall(RIGHT, mazeMask[np-1][j]):
            bMask[2*(np-1)][2*j+1] = NO_WALL
        bMask[2*(np-1)][2*j] = NO_WALL

    bMask[2*(np-1)][2*(mp-1)] = NO_WALL

    return bMask

def deleteWalls(maze0, quant):
    maze = [x[:] for x in maze0]
    n, m = len(maze), len(maze[0])

    numWallsToDel = int( (n-1)*(m-1)*quant )

    # getting walls
    walls = []
    for i in range(1,n):
        for j in range(1,m):
            if existWall(UP, maze[i][j]):
                walls.append( (i, j, UP) )
            if existWall(LEFT, maze[i][j]):
                walls.append( (i, j, LEFT) )
    for i in range(1,n):
        if existWall(UP, maze[i][0]):
            walls.append( (i, 0, UP) )
    for j in range(1,m):
        if existWall(LEFT, maze[0][j]):
            walls.append( (0, j, LEFT) )

    toDel = []
    for i in range(numWallsToDel):
        toDel.append( walls.pop( randint(0, len(walls)-1) ) )

    for i,j,mov in toDel:
        if mov == LEFT:
            quitWall(LEFT, maze, i, j)
            quitWall(RIGHT, maze, i, j-1)
        if mov == UP:
            quitWall(UP, maze, i, j)
            quitWall(DOWN, maze, i-1, j)

    return maze


def getAllMoves((i, j), maze):
    n, m = len(maze), len(maze[0])
    moves = []
    if j>0   and not existWall(LEFT,  maze[i][j]): moves.append( (i,j-1) )
    if i>0   and not existWall(UP,    maze[i][j]): moves.append( (i-1,j) )
    if j<m-1 and not existWall(RIGHT, maze[i][j]): moves.append( (i,j+1) )
    if i<n-1 and not existWall(DOWN,  maze[i][j]): moves.append( (i+1,j) )
    return moves

def getMoves((i, j), maze, mazeDFS):
    n, m = len(maze), len(maze[0])
    moves = []
    if (    j>0
            and not existWall(LEFT,  maze[i][j])
            and mazeDFS[i][j-1] == None
            #and not isMarked(maze[i][j-1])
            #and mazeDFS[i][j-1] != (i,j)
       ):
        moves.append( (i,j-1) )
    if (    i>0
            and not existWall(UP,    maze[i][j])
            and mazeDFS[i-1][j] == None
            #and not isMarked(maze[i-1][j])
            #and mazeDFS[i-1][j] != (i,j)
       ):
        moves.append( (i-1,j) )
    if (    j<m-1
            and not existWall(RIGHT, maze[i][j])
            and mazeDFS[i][j+1] == None
            #and not isMarked(maze[i][j+1])
            #and mazeDFS[i][j+1] != (i,j)
       ):
        moves.append( (i,j+1) )
    if (    i<n-1
            and not existWall(DOWN,  maze[i][j])
            and mazeDFS[i+1][j] == None
            #and not isMarked(maze[i+1][j])
            #and mazeDFS[i+1][j] != (i,j)
       ):
        moves.append( (i+1,j) )
    return moves

def putAllWalls(maze, i, j):
    n, m = len(maze), len(maze[0])
    maze[i][j] = ALLWALLS
    if j>0:   putWall(RIGHT, maze, i,   j-1)
    if i>0:   putWall(DOWN,  maze, i-1, j)
    if j<m-1: putWall(LEFT,  maze, i,   j+1)
    if i<n-1: putWall(UP,    maze, i+1, j)

def simplifyMaze(maze0, entrance=None, exit=None):
    maze = [x[:] for x in maze0]
    n, m = len(maze), len(maze[0])
    mazeDFS = [[None]*m for i in range(n)]

    if entrance==None: (i0, j0, entrWall) = (0, 0, LEFT)
    else:              (i0, j0, entrWall) = entrance
    if exit==None:     (k, l, exitWall) = (n-1, m-1, RIGHT)
    else:              (k, l, exitWall) = exit

    mazeDFS[i0][j0] = (i0,j0)
    stack = [(c, (i0,j0)) for c in getMoves((i0,j0), maze, mazeDFS)]
    #print stack

    r = 0
    while len(stack) > 0:
        (i,j),(ip,jp) = me = stack.pop()
        if mazeDFS[i][j] == None:
            mazeDFS[i][j] = (ip,jp)

        #if (i,j) in [(11,0), (10,0), (9,0)]:
        #    print "here", getMoves((i,j), maze, mazeDFS), stack
        #    print '\n'.join([' '.join([str(1 if c!=None else 0).rjust(2) for c
        #                    in x]) for x in mazeDFS])
        #    print

        if i==k and j==l:
            continue

        allMoves = getAllMoves((i,j), maze)
        lenAllMoves = len(allMoves)
        moves = getMoves((i,j), maze, mazeDFS)
        lenMoves = len(moves)

        if lenAllMoves == 1 and i!=i0 and j!=j0:
            putAllWalls(maze, i, j)
        elif lenMoves > 0:
            stack.append(me)
            for i1,j1 in moves:
                stack.append( ((i1,j1), (i,j)) )
        r+=1

    stack = [(k,l)]

    while len(stack) != 0:
        i,j = stack.pop()
        addMark(maze, i, j)
        iN,jN = mazeDFS[i][j]

        for i1,j1 in getAllMoves((i, j), maze):
            if (
                        None != mazeDFS[i1][j1]
                    and (i,j) != mazeDFS[i1][j1]
                    and not isMarked(maze[i1][j1])
               ):
                stack.append( (i1,j1) )

        r+=1

    for i in range(n):
        for j in range(m):
            if not isMarked(maze[i][j]):
                putAllWalls(maze, i, j)
            else:
                quitMark(maze, i, j)

    # total unrearcheable cells
    totalUnrearcheable = 0
    for i in range(n):
        for j in range(m):
            if allWalls(maze, i, j):
                totalUnrearcheable+=1

    return maze, totalUnrearcheable/float(n*m)

