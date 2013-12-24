#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from definitions import *

def detectMoves((i, j), (ip,jp), (n, m), maze):
    nextMoves = []

    if (        j>0
            and (i,j-1) != (ip,jp)
            and not existWall(LEFT, maze[i][j])
            and not isMarked(maze[i][j-1])
       ):
        nextMoves.append( (i,j-1) )
    if (        i>0
            and (i-1,j) != (ip,jp)
            and not existWall(UP, maze[i][j])
            and not isMarked(maze[i-1][j])
       ):
        nextMoves.append( (i-1,j) )
    if (        j<m-1
            and (i,j+1) != (ip,jp)
            and not existWall(RIGHT, maze[i][j])
            and not isMarked(maze[i][j+1])
       ):
        nextMoves.append( (i,j+1) )
    if (        i<n-1
            and (i+1,j) != (ip,jp)
            and not existWall(DOWN, maze[i][j])
            and not isMarked(maze[i+1][j])
       ):
        nextMoves.append( (i+1,j) )

    return nextMoves

# resolve a maze
# return a list of points (tuples=(x,y))
def findPath(maze0, entrance=None, exit=None):
    maze = [x[:] for x in maze0]
    n, m = len(maze), len(maze[0])

    if entrance==None: (i0, j0, entrWall) = (0, 0, LEFT)
    else:              (i0, j0, entrWall) = entrance
    if exit==None:     (k, l, exitWall) = (n-1, m-1, RIGHT)
    else:              (k, l, exitWall) = exit

    ms = detectMoves((i0, j0), (i0,j0), (n, m), maze)
    stack = [(i0,j0, randomizeList(ms))]
    addMark(maze, i0, j0)

    while not( stack == [] or stack[-1][:2] == (k,l) ):
        i, j, moves = stack[-1]

        if moves == []:
            stack.pop()
        else:
            i1,j1 = moves.pop()

            ms = detectMoves((i1, j1), (i,j), (n, m), maze)
            stack.append( (i1,j1, randomizeList(ms)) )
            addMark(maze, i1, j1)

    if stack == []: return []
    else:
        if entrWall != NOTHING:
            i,j = stack[0][:2]
            if entrWall == LEFT:  stack.insert(0, (i,j-1, NOTHING))
            if entrWall == UP:    stack.insert(0, (i-1,j, NOTHING))
            if entrWall == RIGHT: stack.insert(0, (i,j+1, NOTHING))
            if entrWall == DOWN:  stack.insert(0, (i+1,j, NOTHING))

        if exitWall != NOTHING:
            i,j = stack[-1][:2]
            if exitWall == LEFT:  stack.append( (i,j-1, NOTHING) )
            if exitWall == UP:    stack.append( (i-1,j, NOTHING) )
            if exitWall == RIGHT: stack.append( (i,j+1, NOTHING) )
            if exitWall == DOWN:  stack.append( (i+1,j, NOTHING) )

        return map(lambda x: x[:2], stack)

def findIntersections(height, width, path1, path2):
    maze = [[None for j in range(width)] for i in range(height)]

    for k in range(len(path2)):
        (i,j) = path2[k]
        if i>=0 and i<height and j>=0 and j<width:
            maze[i][j] = k

    cross = []
    isInABlock = False
    for k in range(len(path1)):
        (i,j) = path1[k]

        if i>=0 and i<height and j>=0 and j<width:
            mazeij = maze[i][j]
            if mazeij != None:
                if isInABlock:
                    cross[-1][-1] = (k, mazeij)
                else:
                    cross.append( [(k, mazeij), (k, mazeij)] )
                isInABlock = True
            else:
                isInABlock = False

    return cross

def crossToPath( cross, path1 ):
    [(s1,s2), (f1,f2)] = cross
    return [path1[k] for k in range(s1, f1+1)]
