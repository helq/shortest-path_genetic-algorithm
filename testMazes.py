#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.definitions import *
from src.createMazes import createRandomMaze, deleteWalls, simplifyMaze
from src.pathsOfMaze import findPath, findIntersections, crossToPath
from src.printMazes import palette, createPNGfromMazeAndPaths, printMazePNG
from src.genetics import crossingPaths, mutatePath
import random
random.seed(11)

def testPNG():
    # la siguiente matriz representa los caminos, no las paredes del laberinto
    example1 = [
        u"┐    ┌──┐┌───┐     ┌──┐           ┌┐ ┌┐         ┌────┐ ┌─────┐  ",
        u"└┐   └─┐└┘   │   ┌┐│  └┐┌─┐      ┌┘└┐││ ┌┐      │┌─┐ └┐└─┐  ┌┘  ",
        u"┌┘    ┌┘     └───┘││   └┘ │      │  ││└┐│└─────┐└┘ │ ┌┘ ┌┘┌─┘   ",
        u"└─┐┌──┘┌─┐     ┌──┘│    ╶┬┘      │┌─┘└┐││ ┌──┐ │ ┌─┘┌┘  │ └┐ ┌─┐",
        u"  └┘  ┌┘ └──┐  └┐ ┌┘     │ ┌──┐ ┌┘└──┐│└┘┌┘┌─┘ └┐│  └─┐┌┘┌┐│ │ │",
        u" ┌────┘┌┐   │ ┌─┘ │     ┌┘ │┌┐│ └──┐ └┘┌┐│┌┘┌┐╷ └┘    └┘ │└┘ │ │",
        u" │   ┌─┘└─┐ │ └─┐ │┌┐   └┐ └┘││ ┌┐ │┌┐ │└┘│ │├┘      ┌──┐│┌┐ │ │",
        u"┌┘┌──┘┌┐ ┌┘┌┘  ┌┘ └┘│┌┐ ┌┘┌──┘│┌┘│ └┘│ │  │┌┘│       │┌┐│└┘│ │ │",
        u"└┐│  ┌┘└┐└┐│ ┌┐└─┐  └┘│ │ │ ┌┐└┘ └─┐ └─┘  └┘ └┐ ┌──┐ ││└┘  └─┘ │",
        u" ││  └─┐│┌┘└─┘└──┘   ┌┘ │ │ │└┐    └┐┌──┐    ┌┘┌┘ ┌┘┌┘│┌┐ ┌─┐  │",
        u" └┘┌───┘└┘┌──┐┌┐┌────┘  │ │ └┐│    ┌┘│  │    │ └┐ │ │┌┘│└┐│ └──┘",
        u"   └┐┌──┐┌┘┌─┘│││       │ │ ┌┘└┐┌┐ └┐│┌┐│    │  │ └─┘│┌┘ │└┐    ",
        u"┌┐  ││  ││ └──┘││ ┌─┐   │ │ │  └┘│  │└┘││  ┌─┘  │┌─┐┌┘│  └┐│    ",
        u"│└──┘└┐ ││┌┐   └┤ │┌┘   │┌┴─┘  ┌┐│  │┌─┘└──┘ ╷  │└┐│└─┘   └┘┌──┐",
        u"│ ┌───┘ │└┘│    │ │└┐┌┬─┼┘  ┌─┐││└──┘│      ╶┼╴ ├┐│└┐    ┌┐┌┘┌─┘",
        u"└─┘     └──┘    └─┘ └┘└─┴───┘╶┼┘└────┘       ╵  ╵└┘ └────┘└┘ └──",
    ]
    example2 = [
        u"┬─┬─┬───┬───┐",
        u"│ │ │┌┐ │┌┐ │",
        u"└┬┘ └┘│ └┘└─┘",
        u" └────┴──────"
    ]
    example3 = [
        u"─┬──┬───┐",
        u"┌┴┐ │┌┐ │",
        u"│ │ └┘└─┘",
        u"├─┼─┐    ",
        u"│ ├─┘  ╶┐",
        u"└┬┘     │",
        u" └──────┴"
    ]

    example = example1

    def pathToWalls(s):
        if   s == u" ": return 15 # LEFT & UP & RIGHT & DOWN
        elif s == u"╴": return 14 #        UP & RIGHT & DOWN
        elif s == u"╵": return 13 # LEFT      & RIGHT & DOWN
        elif s == u"╶": return 11 # LEFT & UP         & DOWN
        elif s == u"╷": return  7 # LEFT & UP & RIGHT
        elif s == u"─": return 10 #        UP &         DOWN
        elif s == u"│": return  5 # LEFT      & RIGHT
        elif s == u"┌": return  3 # LEFT & UP
        elif s == u"┐": return  6 #        UP & RIGHT
        elif s == u"┘": return 12 #             RIGHT & DOWN
        elif s == u"└": return  9 # LEFT &            & DOWN
        elif s == u"├": return  1 # LEFT
        elif s == u"┬": return  2 #        UP
        elif s == u"┤": return  4 #             RIGHT
        elif s == u"┴": return  8 #                     DOWN
        elif s == u"┼": return  0 # NOTHING

    exampleWalls = map(lambda x: map(pathToWalls, x), example)
    simple = simplifyMaze(exampleWalls)
    #print '\n'.join([' '.join([str(c).rjust(2) for c in x]) for x in simple])

    import pypng.png as png

    s = createPNGfromMazeAndPaths(exampleWalls)
    printMazePNG(s, "png1.png")
    s = createPNGfromMazeAndPaths(simple)
    printMazePNG(s, "png1simple.png")

def test2():
    import pypng.png as png
    n, m = 30, 40

    maze = createRandomMaze(n, m)
    mazeSimple = simplifyMaze(maze)

    s = createPNGfromMazeAndPaths(maze)
    printMazePNG(s, "png2.png")
    s = createPNGfromMazeAndPaths(mazeSimple)
    printMazePNG(s, "png2simple.png")

def test3():
    n, m = 100, 120

    if True:
        mazePerfect = createRandomMaze(n, m)
        maze = deleteWalls(mazePerfect, 0.10)

        # maze without dead-ends
        mazeSimple = simplifyMaze(maze)

        from random import random
        mazeWeight = [[random() for j in range(m)] for i in range(n)]

        sol = findPath(maze)
        sol2 = findPath(maze)

        # Saving
        import pickle
        o = open('test.bin', 'wb')
        #pickle.dump(mazePerfect, o)
        pickle.dump(maze, o)
        pickle.dump(mazeSimple, o)
        pickle.dump(mazeWeight, o)
        # this is a simple save, without using the optimized procedure
        # savePath from src.savePaths
        pickle.dump(sol, o)
        pickle.dump(sol2, o)

    else:
        # Loading
        import pickle
        o = open('test.bin', 'rb')
        #mazePerfect = pickle.load(o)
        maze = pickle.load(o)
        mazeSimple = pickle.load(o)
        mazeWeight = pickle.load(o)
        sol = pickle.load(o)
        sol2 = pickle.load(o)

    # saving
    # maze clean
    #s = createPNGfromMazeAndPaths(mazePerfect)
    #printMazePNG(s, "test3-Perfect.png")

    #s = createPNGfromMazeAndPaths(maze)
    #printMazePNG(s, "test3.png")

    #s = createPNGfromMazeAndPaths(maze, [sol, sol2])
    #printMazePNG(s, "test3-paths.png")

    #s = createPNGfromMazeAndPaths(mazeSimple)
    #printMazePNG(s, "test3-simple.png")

    #solSon,k,l = crossingPaths(n, m, sol, sol2)
    #s = createPNGfromMazeAndPaths(maze, [solSon])
    #printMazePNG(s, "test3-son.png")

    # mutating
    solMut, p1, p2 = mutatePath(maze, sol)
    s = createPNGfromMazeAndPaths(maze, [sol, solMut], [[p1,p1], [p2, p2]])
    printMazePNG(s, "test3-original-and-mutated.png")

    # finding shortest path
    #from src.shortestPath import shortestPath
    #solMut = shortestPath(maze, mazeWeight)
    #s = createPNGfromMazeAndPaths(maze, [sol, solMut])
    #printMazePNG(s, "test3-shortest-path.png")

def test4():
    import pypng.png as png
    n, m = 30, 40
    entrance, exit = (12,0, LEFT), (21,m-1, RIGHT)

    maze = createRandomMaze(n, m, entrance, exit)
    sol = findPath(maze, entrance, exit)

    s = createPNGfromMazeAndPaths(maze, [sol])

    writterPNG = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=2)

    f = open('png4.png', 'wb')
    writterPNG.write(f, s)
    f.close()

def test5():
    import pypng.png as png
    n, m = 30, 40
    entrance, exit = (5,10, NOTHING), (21,37, NOTHING)

    maze = createRandomMaze(n, m, entrance, exit)
    sol = findPath(maze, entrance, exit)

    s = createPNGfromMazeAndPaths(maze, [sol])

    writterPNG = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=4)

    f = open('png5.png', 'wb')
    writterPNG.write(f, s)
    f.close()

def test6():
    n, m = 300,400

    if True:
        mazePerfect = createRandomMaze(n, m)
        maze = deleteWalls(mazePerfect, 0.07)
        mazeSimple, per = simplifyMaze(maze)
        from src.createMazes import createRandomWeight
        mazeWeight, mask = createRandomWeight(n, m, 70)

        # Saving
        import pickle
        o = open('test.bin', 'wb')
        pickle.dump(maze, o)
        pickle.dump(mazeWeight, o)

    # outdated
    #else:
        ## Loading
        #import pickle
        #o = open('test.bin', 'rb')
        ##mazePerfect = pickle.load(o)
        #maze = pickle.load(o)
        #mazeWeight = pickle.load(o)

    print per # total unrearcheable cells

    # finding shortest path
    from src.shortestPath import shortestPath
    sol = shortestPath(maze, mazeWeight)
    s = createPNGfromMazeAndPaths(mazeSimple, [sol])
    printMazePNG(s, "test5.png")


    toPNG = [[int(255*(1-j)) for j in i] for i in mask]
    import pypng.png as png
    writterPNG = png.Writer( len(toPNG[0]), len(toPNG)
                           , greyscale=True
                           , bitdepth=8)
    f = open("testing.png", 'wb')
    writterPNG.write(f, toPNG)
    f.close()


#testPNG()
#test2()
test3()
#test4()
#test5()
#test6()
