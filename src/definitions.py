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
putWall = lambda tW, c: tW | c
quitWall = lambda tW, c: tW ^ c

addMark = lambda c: c | MARK
quitMark = lambda c: c ^ MARK
isMark = lambda c: bool(c & MARK)

# generate random sequence of moves
def randomizeMoves( moves = [LEFT, UP, RIGHT, DOWN] ):
    if len(moves) > 1:
        for i in range(len(moves)-1, 0, -1):
            tmp = randint(0,i)
            moves[i], moves[tmp] = moves[tmp], moves[i]
    return moves
