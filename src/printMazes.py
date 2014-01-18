#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from definitions import *

BLACK  = 0
WHITE  = 1
PINK   = 2
GREEN  = 3
PURPLE = 4
RED    = 5

palette=[ (0x0,0x0,0x0)    # 0  BLACK
        , (0xff,0xff,0xff) # 1  WHITE
        , (0xff,0x99,0x99) # 2  PINK
        , (0x4e,0xba,0x75) # 3  GREEN
        , (0xa1,0x50,0xc0) # 4  PURPLE
        , (0xff,0x0,0x0)]  # 5  RED

# create from a maze (matrix) a "PNG", well the base of a "PNG"
def generateBasePNG(maze):
    m = len(maze[0])
    n = len(maze)
    png = [ [BLACK]*(2*m+1) for i in range(2*n+1)]

    # destroying walls
    for i in range(n):
        for j in range(m):
            if not existWall(UP, maze[i][j]):
                png[2*i][2*j+1] = WHITE
            if not existWall(LEFT, maze[i][j]):
                png[2*i+1][2*j] = WHITE

            # if the the celd have all the walls, then put black
            if not allWalls(maze, i, j):
                png[2*i+1][2*j+1] = WHITE

    for i in range(n):
        if not existWall(RIGHT, maze[i][m-1]):
            png[2*i+1][2*m] = WHITE
    for j in range(m):
        if not existWall(DOWN, maze[n-1][j]):
            png[2*n][2*j+1] = WHITE

    return png

def _coloring(png, i, j, color):
    if png[i][j] == PINK: png[i][j] = PURPLE
    else:                 png[i][j] = color

def createPNGfromMazeAndPaths(maze, paths=[], red_paths=[]):
    n, m = len(maze), len(maze[0])
    if len(paths)>2: paths = paths[:2]

    def addpathToPNG(png, path, color):
        i1, j1 = path[0]
        if i1>=0 and j1>=0 and i1<n and j1<m:
            _coloring(png, 2*i1+1, 2*j1+1, RED)

        for i,j in path[1:]:
            if i>=0 and j>=0 and i<n and j<m:
                _coloring(png, 2*i+1, 2*j+1, color)
            _coloring( png, (2*i+1) + (i1-i), (2*j+1) + (j1-j), color )
            i1, j1 = i, j

        if i>=0 and j>=0 and i<n and j<m:
            png[2*i+1][2*j+1] = RED

    png = generateBasePNG(maze)

    # máximo dos rutas
    c = PINK
    for path in paths:
        addpathToPNG(png, path, c)
        c+=1

    for path in red_paths:
        addpathToPNG(png, path, RED)

    return png

def printMazePNG(mazePNG, name):
    import pypng.png as png

    writterPNG = png.Writer( len(mazePNG[0])
                           , len(mazePNG)
                           , palette=palette
                           , bitdepth=4)

    f = open(name, 'wb')
    writterPNG.write(f, mazePNG)
    f.close()
