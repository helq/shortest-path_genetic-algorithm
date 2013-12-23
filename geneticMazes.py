#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.definitions import *
from src.createMazes import createRandomMaze, deleteWalls, simplifyMaze
from src.pathsOfMaze import findPath, findIntersections, crossToPath
from src.printMazes import palette, createPNGfromMazeAndPaths, saveMaze
from src.genetics import crossingPaths, mutatePath, fitness, evolutionAlgo

from random import random
import pickle
from time import clock

n, m = 300, 400
sizeInitialPopulation = 30
mutPercent = 0.40
totalPopulation = 50
totalIterations = 500
numberOfBadIndividuals = 5
randomVariableFunction = lambda x: (0.6/0.5)*x if x<0.6 else (x-1)*((1-0.5)/(1-0.6)) + 1

folder = "testFindings/"
nameFile = "test"
useOldTest = False
useOldInitialPopulation = False
useOldFinalPopulation = False

def savePaths(maze, mazeWeigth, paths, folder):
    for i in range(len(paths)):
        png = createPNGfromMazeAndPaths(maze, [paths[i]])
        fitnessPath = fitness(mazeWeigth ,paths[i])
        saveMaze(png, folder+str(i).zfill(3)+'-'+str(fitnessPath)+'.png')

def saveTest(name, maze, mazeSimple, mazeWeigth, initialPopulation, finalPopulation):
    o = open(folder+name+'.bin', 'wb')
    pickle.dump(maze, o)
    pickle.dump(mazeSimple, o)
    pickle.dump(mazeWeigth, o)
    pickle.dump(initialPopulation, o)
    pickle.dump(finalPopulation, o)
    o.close()



if useOldTest:
    o = open(folder+nameFile+'.bin', 'rb')
    maze = pickle.load(o)
    mazeSimple = pickle.load(o)
    mazeWeigth = pickle.load(o)

    if useOldInitialPopulation:
        initialPopulation = pickle.load(o)

        if useOldFinalPopulation:
            finalPopulation = pickle.load(o)
        else:
            finalPopulation, num_clones = evolutionAlgo(
                    maze, mazeWeigth, initialPopulation , mutPercent,
                    totalPopulation, totalIterations , numberOfBadIndividuals,
                    randomVariableFunction)

            saveTest( nameFile+"2", maze, mazeSimple, mazeWeigth
                    , initialPopulation , finalPopulation)

    else:
        initialPopulation = [findPath(maze) for i in range(sizeInitialPopulation)]
        initialPopulation.sort(key=lambda i: fitness(mazeWeigth, i))

        finalPopulation, num_clones = evolutionAlgo(
                maze, mazeWeigth, initialPopulation , mutPercent,
                totalPopulation, totalIterations , numberOfBadIndividuals,
                randomVariableFunction)

        saveTest( nameFile+"2", maze, mazeSimple, mazeWeigth
                , initialPopulation , finalPopulation)


else:
    # creating maze
    maze = deleteWalls(createRandomMaze(n, m), 0.010)
    mazeSimple = simplifyMaze(maze)
    mazeSimple = maze
    mazeWeigth = [[random() for j in range(m)] for i in range(n)]

    # creating initial population
    initialPopulation = [findPath(mazeSimple) for i in range(sizeInitialPopulation)]
    initialPopulation.sort(key=lambda i: fitness(mazeWeigth, i))

    print "initialPopulation created"

    finalPopulation, num_clones = evolutionAlgo(
            maze, mazeWeigth, initialPopulation , mutPercent,
            totalPopulation, totalIterations , numberOfBadIndividuals,
            randomVariableFunction)

    # saving population and images
    saveTest(nameFile, maze, mazeSimple, mazeWeigth, initialPopulation, finalPopulation)

print num_clones

savePaths(maze, mazeWeigth, initialPopulation, folder+'initial/')
savePaths(maze, mazeWeigth, finalPopulation, folder+'final/')
