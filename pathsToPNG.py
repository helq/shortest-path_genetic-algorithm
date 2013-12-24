#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.printMazes import createPNGfromMazeAndPaths, saveMaze
from src.genetics import fitness, evolutionAlgo
from src.savePaths import loadListOfPaths

import os.path as path
import os, sys, pickle

mazeFile = 'data.bin'
folderInitialPop = 'initial/'
folderFinalPop = 'final/'

help_message = "usage: " + sys.argv[0] + " file" + """\n
  this program saves as images the paths saved in the folders `proyect'/initial
  and `proyect'/final in `proyect'/images

  example: """+sys.argv[0]+""" test/final/002-000
"""

def savePathsFromFile(pathsFile, folder):
    o = open(path.join(folder, pathsFile), 'rb')
    population = loadListOfPaths(o)
    o.close()

    o = open(path.join(folder, mazeFile), 'rb')
    n = pickle.load(o)          # unnecesary
    m = pickle.load(o)          # unnecesary
    wallsToDel = pickle.load(o) # unnecesary
    maze = pickle.load(o)
    mazeSimple = pickle.load(o) # unnecesary
    mazeWeigth = pickle.load(o)
    o.close()

    savePathsAsImage( maze, mazeWeigth, population,
                      path.join(folder, 'images', pathsFile) )

def savePathsAsImage(maze, mazeWeigth, paths, folder):
    if not path.exists(folder):
        os.makedirs(folder)
    for i in range(len(paths)):
        png = createPNGfromMazeAndPaths(maze, [paths[i]])
        fitnessPath = fitness(mazeWeigth, paths[i])
        saveMaze(png,
                   path.join(folder,
                             str(i).zfill(3)+'-'+str(fitnessPath)+'.png') )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print help_message
        exit(0)

    print path.abspath( sys.argv[1] )
    dir1, file1 = path.split( path.abspath( sys.argv[1] ) )
    folder, dir2 = path.split( dir1 )
    pathsFile = path.join(dir2, file1)

    savePathsFromFile(pathsFile, folder)
