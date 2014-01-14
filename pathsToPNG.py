#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.printMazes import createPNGfromMazeAndPaths, printMazePNG
from src.genetics import fitness, evolutionAlgo
from src.savePaths import loadListOfPaths, loadPath

import os.path as path
import os, sys, pickle

dataBin = 'data.bin'
folderInitialPop = 'initial/'
folderFinalPop = 'final/'
folderImages = 'images'

help_message = "usage: " + sys.argv[0] + " file" + """\n
  this program saves as images the paths saved in the folders
  `proyect'/initial, `proyect'/final and `proyect'/data.bin
  in `proyect'/images

  -c   compare with the shortestPath

  example: """+sys.argv[0]+""" test/final/002-000
           """+sys.argv[0]+""" -c test/final/002-000 test/initial/000

"""

def main(pathsFiles, rootFolder, printDataBin, compareWithShortPath):
    # getting maze
    dataBinPath = path.join(rootFolder, dataBin)
    o = open(dataBinPath, 'rb')
    n = pickle.load(o)          # unnecesary
    m = pickle.load(o)          # unnecesary
    wallsToDel = pickle.load(o) # unnecesary
    maze = pickle.load(o)
    mazeSimple = pickle.load(o)
    mazeWeigth = pickle.load(o)
    shortPath = loadPath(o)
    o.close()

    if printDataBin:
        printFolder = path.join(rootFolder, folderImages, dataBin)
        if not path.exists(printFolder): os.makedirs(printFolder)

        png = createPNGfromMazeAndPaths(maze)
        nameMazePNG = path.join(printFolder, "Maze.png")
        printMazePNG(png, nameMazePNG)

        png = createPNGfromMazeAndPaths(mazeSimple)
        nameMazeSimplePNG = path.join(printFolder, "MazeSimple.png")
        printMazePNG(png, nameMazeSimplePNG)

        png = createPNGfromMazeAndPaths(maze, [shortPath])
        fitnessPath = str(fitness(mazeWeigth, shortPath))
        nameMazePNG = path.join(printFolder, "Maze-Shortest_Path-"+fitnessPath+".png")
        printMazePNG(png, nameMazePNG)

    for p in pathsFiles:
        # getting paths
        o = open(path.join(rootFolder, p), 'rb')
        population = loadListOfPaths(o)
        o.close()

        if not compareWithShortPath: shortPath = None
        nameFile = path.join(rootFolder, folderImages, p)
        savePathsAsPNG(maze, mazeWeigth, population, nameFile, shortPath)

def savePathsAsPNG(maze, mazeWeigth, paths, folder, cmpPath=None):
    if not path.exists(folder):
        os.makedirs(folder)
    for i in range(len(paths)):
        if cmpPath != None:
            png = createPNGfromMazeAndPaths(maze, [paths[i], cmpPath])
        else:
            png = createPNGfromMazeAndPaths(maze, [paths[i]])

        fitnessPath = fitness(mazeWeigth, paths[i])
        nameMazePNG = path.join(folder, str(i).zfill(3)+'-'+str(fitnessPath)+'.png')
        printMazePNG(png, nameMazePNG)

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print help_message
        exit(0)

    if sys.argv[1] == "-c":
        compareWithShortPath = True
        sys.argv.pop(1)
    else:
        compareWithShortPath = False

    pathsFiles = []

    printDataBin = False
    print "File(s) selected:"
    for p in [path.abspath(i) for i in sys.argv[1:]]:
        print p
        dir1, fname = path.split( p )

        if fname == dataBin:
            folder = dir1
            printDataBin = True
        else:
            folder, dir2 = path.split( dir1 )
            pathsFiles.append( path.join(dir2, fname) )

    print "... printing ..."
    main(pathsFiles, folder, printDataBin, compareWithShortPath)
