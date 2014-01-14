#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.createMazes import createRandomMaze, deleteWalls, simplifyMaze
from src.pathsOfMaze import findPath
from src.genetics import fitness, evolutionAlgo
import src.savePaths as savePaths
from src.shortestPath import shortestPath
import argv

from random import random
#from time import clock
import os, pickle, sys
import os.path as path

mazeFile = 'data.bin'
folderInitialPop = 'initial'
folderFinalPop = 'final'

options = argv.parse(sys.argv)

help_message = "usage: " + ' '.join(options['_']) + " [option] " + """\n
options:
GLOBAL DEFINED:
  -F --folder=name           (mandatory) folder to save the results
     --dim=n,m               * dimensions of the maze (default: 60,70)
  -d --wallsToDel=float      * percent of the walls to delete (default: 0.10)
  -m --mutationPercent=float percent of mutation, probability of mutate in a
                             determined cycle (iteration) (default: 0.10)

  -t --totalPopulation=num   maximum size of the population (default: 50)
  -i --totalIterations=num   number of iterations (default: 200)
  -b --badIndividuals=num    number of `bad' individuals, they have the worst
                             fitness value (default: 10)
  -c --chooseFunction=funct  the individuals for mutation are elected randomly
                             according to this function (have to be writed in
                             python syntax. ex: `-f "lambda x: x"')

  -M --multiplesExec=num     exec `num' times the main function, loading the
                             maze data only once (default: 1)
  -P --manyFinalPop=num      create `num' final populations, negative number
                             posible (default: 1)

  -I --initialPop=num        use an exisisting population (num of the
                             population in """+folderInitialPop+""")
                             This overwrite the option `-s'
                             Deactivated when `-M' is setted

PER POPULATION DEFINED:
  -s --sizeInitial=num       size of initial population (is a global option
                             but if the population exists before (SEE: option
                             -I) then is overwrited) (default: 15)


MISCELLANEOUS:
  -h --help                  Show this help

* setted only when the folder doesn't exist (SEE: --folder)

  examples:
    """+sys.argv[0]+""" --folder test
    """+sys.argv[0]+""" -F test --dim 100,120 -d 0.4
    """+sys.argv[0]+""" -F test -I 000
    """+sys.argv[0]+""" -F test -M 10 -P=-1

to save paths in a PNG see `pathsToPNG.py'
"""

def getParameter(names, default, funct=lambda x:x):
    for i in names:
        if i in options:
            return funct( options[i] )
    return default

def main(folder):
  initialPop      = getParameter(['initialPop',      'I'], None)
  n, m            = getParameter(['dim']                 , (60, 70)  , eval)
  wallsToDel      = getParameter(['wallsToDel',      'd'], 0.10      , float)
  mutPercent      = getParameter(['mutationPercent', 'm'], 0.10      , float)
  totalPopulation = getParameter(['totalPopulation', 't'], 50        , int)
  totalIterations = getParameter(['totalIterations', 'i'], 200       , int)
  badIndividuals  = getParameter(['badIndividuals',  'b'], 10        , int)
  chooseFunction  = getParameter(['chooseFunction',  'c'], lambda x:x, eval)
  sizeInitial     = getParameter(['sizeInitial',     's'], 15        , int)
  multiplesExec   = getParameter(['multiplesExec',   'M'], 1         , int)
  manyFinalPop    = getParameter(['manyFinalPop',    'P'], 1         , int)
  #chooseFunction = lambda x: (0.6/0.5)*x if x<0.6 else (x-1)*((1-0.5)/(1-0.6)) + 1

  # If the folder doesn't exisit
  if not os.path.exists(folder):
      os.makedirs(folder)
      os.makedirs( path.join(folder, folderInitialPop) )
      os.makedirs( path.join(folder, folderFinalPop) )
      open( path.join(folder, folderInitialPop, 'counter'),'wb').write('0')
      open( path.join(folder, folderFinalPop, 'counters'),'wb').write('[]')

  ######################## Maze #######################
  if os.path.exists( path.join(folder, mazeFile) ):
      o = open( path.join(folder, mazeFile), 'rb')
      n = pickle.load(o)
      m = pickle.load(o)
      wallsToDel = pickle.load(o)
      maze = pickle.load(o)
      mazeSimple = pickle.load(o)
      mazeWeight = pickle.load(o)
      shortPath = savePaths.loadPath(o)
      o.close()
  else:
      maze = deleteWalls(createRandomMaze(n, m), wallsToDel)
      mazeSimple = simplifyMaze(maze)

      # an ellipse, well ... an elliptic paraboloid
      ellipse = lambda i,j: ( ((i - float(n)/2)**2 / (5*float(n)/7)**2)
                            + ((j - float(m)/2)**2 / (5*float(m)/7)**2)
                            )
      mazeWeight = [[2*random()/(ellipse(i,j)+1) for j in range(m)] for i in range(n)]
      shortPath = shortestPath(mazeSimple, mazeWeight)

      o = open( path.join(folder, mazeFile), 'wb')
      pickle.dump(n, o)
      pickle.dump(m, o)
      pickle.dump(wallsToDel, o)
      pickle.dump(maze, o)
      pickle.dump(mazeSimple, o)
      pickle.dump(mazeWeight, o)
      savePaths.savePath(shortPath, o)
      o.close()

  print "Starting ..."
  print "Maze dimensions:", (n, m)
  print "Walls Deleted (percentage):", wallsToDel
  print "Shortest Path: ", fitness(mazeWeight, shortPath)
  print
  print "=== Global variables setted to: ==="
  print "Mutation (percentage):", mutPercent
  print "Total iterations:", totalIterations
  print "Number of bad individuals:", badIndividuals
  print

  print "== Statistics =="
  print

  for _ in range(multiplesExec):
    ######################## initial Population #######################
    if initialPop == None or multiplesExec > 1:
        o_counter = open( path.join(folder, folderInitialPop, 'counter'),'rb')
        counter = int(o_counter.read())
        o_counter.close()

        initialPopulation = [findPath(mazeSimple) for i in range(sizeInitial)]
        initialPopulation.sort(key=lambda i: fitness(mazeWeight, i))
        nameInitialPop = str(counter).zfill(3)

        o = open( path.join(folder, folderInitialPop, nameInitialPop), 'wb')
        savePaths.saveListOfPaths(initialPopulation, o)
        o.close()

        o_counter = open( path.join(folder, folderInitialPop, 'counter'),'wb')
        o_counter.write(str(counter+1))
        o_counter.close()
    else:
        counter = int(initialPop, 10)
        nameInitialPop = str(counter).zfill(3)
        o = open( path.join(folder, folderInitialPop, nameInitialPop), 'rb')
        initialPopulation = savePaths.loadListOfPaths(o)
        o.close()

    ##################################################################

    print "Initial Population", nameInitialPop
    print "  initial size population:", len(initialPopulation)
    print "  total population:", totalPopulation
    print "  best path: ", fitness(mazeWeight, initialPopulation[0])
    print "  worst path:", fitness(mazeWeight, initialPopulation[-1])
    print


    ####################### final population #######################
    o_counters = open( path.join(folder, folderFinalPop, 'counters'),'rb')
    counters = eval(o_counters.read())
    o_counters.close()
    if len(counters) <= counter:
        counters.extend( [-1]*(counter-len(counters)+1) )

    for i in range(manyFinalPop):
        finalPopulation, num_clones, num_mutated = evolutionAlgo(
                mazeSimple, mazeWeight, initialPopulation , mutPercent,
                totalPopulation, totalIterations , badIndividuals,
                chooseFunction)

        counters[counter] += 1
        nameFinalPop = str(counter).zfill(3)+'-'+str(counters[counter]).zfill(3)
        print "  Final Population #", nameFinalPop
        print "    num of clones in the execution:", num_clones
        print "    num of mutations in the execution:", num_mutated
        print "    best path: ", fitness(mazeWeight, finalPopulation[0])
        print "    worst path:", fitness(mazeWeight, finalPopulation[-1])
        print

        o = open( path.join(folder, folderFinalPop, nameFinalPop), 'wb')
        savePaths.saveListOfPaths(finalPopulation, o)
        pickle.dump(num_clones, o)
        pickle.dump(num_mutated, o)
        o.close()

    # increment counters
    o_counters = open( path.join(folder, folderFinalPop, 'counters'),'wb')
    o_counters.write(str(counters))
    o_counters.close()


if __name__ == "__main__":
    if  'folder' in options: folder = options['folder']
    elif     'F' in options: folder = options['F']
    else:
        print "you need set a folder"
        print help_message
        exit(1)

    if 'h' in options or 'help' in options:
        print help_message
    else:
        main(folder)
