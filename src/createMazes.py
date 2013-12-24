#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from random import randint, random
from definitions import *
from operator import eq, gt
from collections import deque

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

    #print '\n'.join([' '.join([str(1 if c!=None else 0).rjust(2) for c
    #                in x]) for x in mazeDFS])
    #print
    #print '\n'.join([' '.join([str(1 if isMarked(c) else 0).rjust(2) for c
    #                in x]) for x in maze])

    for i in range(n):
        for j in range(m):
            if not isMarked(maze[i][j]):
                putAllWalls(maze, i, j)
            else:
                quitMark(maze, i, j)

    #print r
    return maze

