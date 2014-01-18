# defines
from random import randint

LEFT  = 1
UP    = 2
RIGHT = 4
DOWN  = 8
NOTHING = 0
ALLWALLS = LEFT | UP | RIGHT | DOWN

MARK = 16


existWall = lambda tW, c: bool(tW & c)
def putWall(wall, maze, i, j):
    maze[i][j] = wall | maze[i][j]
def quitWall(wall, maze, i, j):
    maze[i][j] = wall ^ maze[i][j]
allWalls = lambda maze, i, j: ALLWALLS & maze[i][j] == ALLWALLS


isMarked = lambda c: bool(c & MARK)
def addMark(maze, i, j):
    maze[i][j] = maze[i][j] | MARK
def quitMark(maze, i, j):
    maze[i][j] = maze[i][j] ^ MARK


# reareange all the positions randomly
def randomizeList( l ):
    if len(l) > 1:
        for i in range(len(l)-1, 0, -1):
            tmp = randint(0,i)
            l[i], l[tmp] = l[tmp], l[i]
    return l
