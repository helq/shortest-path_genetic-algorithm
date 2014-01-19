#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.createMazes import createRandomMaze, deleteWalls, simplifyMaze, createRandomWeight
from src.pathsOfMaze import findPath, canFindSolutionFromPaths
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
  -V --initPopInvulnrb=bool  make Initial Population Invulnerable (default: 1)
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
  toBool = lambda s: False if s in ["False", "false", "f", "F", "0"] else bool(s)
  initPopInvulnrb = getParameter(['initPopInvulnrb', 'V'], True      , toBool)
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
      inaccesibleCellsPercent = pickle.load(o)
      shortPath = savePaths.loadPath(o)
      o.close()
  else:
      maze = deleteWalls(createRandomMaze(n, m), wallsToDel)
      mazeSimple, inaccesibleCellsPercent = simplifyMaze(maze)

      mazeWeight, _ = createRandomWeight(n, m)
      shortPath = shortestPath(mazeSimple, mazeWeight)

      o = open( path.join(folder, mazeFile), 'wb')
      pickle.dump(n, o)
      pickle.dump(m, o)
      pickle.dump(wallsToDel, o)
      pickle.dump(maze, o)
      pickle.dump(mazeSimple, o)
      pickle.dump(mazeWeight, o)
      pickle.dump(inaccesibleCellsPercent, o)
      savePaths.savePath(shortPath, o)
      o.close()

  print "Starting ..."
  print "Maze dimensions:", (n, m)
  print "Walls Deleted (percentage):", wallsToDel
  print "Inaccesible cells (percentage):", inaccesibleCellsPercent
  fitnessShortPath = fitness(mazeWeight, shortPath)
  print "Shortest Path: ", fitnessShortPath
  print
  print "=== Global variables setted to: ==="
  print "Mutation (percentage):", mutPercent
  print "Total iterations:", totalIterations
  print "Number of bad individuals:", badIndividuals
  print "Initial Population Invulnerable:", initPopInvulnrb
  print

  print "== Statistics =="
  print

  nameStatisticFinal = path.join(folder, "final.csv")
  if not os.path.exists(nameStatisticFinal):
      statistics_final = open(nameStatisticFinal, 'a')
      statistics_final.write("Name; ")
      statistics_final.write("% mutation; ")
      statistics_final.write("total iterations; ")
      statistics_final.write("bad Individuals; ")
      statistics_final.write("invulnerable initPop; ")
      statistics_final.write("Len Initial Population; ")
      statistics_final.write("Total Population; ")
      statistics_final.write("Best Init Path; ")
      statistics_final.write("Worst Init Path; ")
      statistics_final.write("Can be made from Init paths?; ")
      statistics_final.write("clones; ")
      statistics_final.write("mutations; ")
      statistics_final.write("Best final Path; ")
      statistics_final.write("Worst final Path; ")
      statistics_final.write("Ratio best-shortest paths; ")
      statistics_final.write("improvement from initial; ")
      statistics_final.write("Can me made from Final paths?\n")
  else:
      statistics_final = open(nameStatisticFinal, 'a')

  statistics_initial = open( path.join(folder, "initial.csv"), 'a' )

  for i in range(multiplesExec):
    ######################## initial Population #######################
    if initialPop == None:
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
        if os.path.exists( path.join(folder, folderInitialPop, 'counter')):
            initialPop = str(counter+1).zfill(3)

    ##################################################################

    ############################ statistics ############################
    def printSave(t, d, others="", final=False):
        print t, d, others
        statistics_initial.write(str(d) + ("\n" if final else "; "))

    bestInitPop = fitness(mazeWeight, initialPopulation[0])
    ratioBestShortPathInitPop = float(bestInitPop)/fitnessShortPath
    worstInitPop = fitness(mazeWeight, initialPopulation[-1])
    canInit = canFindSolutionFromPaths(n, m, shortPath, initialPopulation)
    printSave("Initial Population",           nameInitialPop)
    printSave("  initial size population:",   len(initialPopulation))
    printSave("  total population:",          totalPopulation)
    printSave("  best path: ",                bestInitPop)
    printSave("  worst path:",                worstInitPop)
    printSave("  ratio best-shortest paths:", ratioBestShortPathInitPop)
    printSave("  Is posible find the Shortest-Path from paths:", canInit, final=True)
    print
    ####################################################################

    ####################### final population #######################
    o_counters = open( path.join(folder, folderFinalPop, 'counters'),'rb')
    counters = eval(o_counters.read())
    o_counters.close()
    if len(counters) <= counter:
        counters.extend( [-1]*(counter-len(counters)+1) )

    def printSave(t, d, others="", final=False):
        print t, d, others
        statistics_final.write(str(d) + ("\n" if final else "; "))

    for i in range(manyFinalPop):
        finalPopulation, num_clones, num_mutated = evolutionAlgo(
                mazeSimple, mazeWeight, initialPopulation , mutPercent,
                totalPopulation, totalIterations , badIndividuals,
                initPopInvulnrb, chooseFunction)

        counters[counter] += 1

        ############################ statistics ############################
        nameFinalPop = str(counter).zfill(3)+'-'+str(counters[counter]).zfill(3)
        best = fitness(mazeWeight, finalPopulation[0])
        ratioBestShortPath = float(best)/fitnessShortPath
        can = canFindSolutionFromPaths(n, m, shortPath, finalPopulation)

        printSave("  Final Population #", nameFinalPop)
        statistics_final.write(str(mutPercent)+"; ")
        statistics_final.write(str(totalIterations)+"; ")
        statistics_final.write(str(badIndividuals)+"; ")
        statistics_final.write(str(initPopInvulnrb)+"; ")
        statistics_final.write(str(len(initialPopulation))+"; ")
        statistics_final.write(str(totalPopulation)+"; ")
        statistics_final.write(str(bestInitPop)+"; ")
        statistics_final.write(str(worstInitPop)+"; ")
        statistics_final.write(str(canInit)+"; ")
        printSave("    num of clones in the execution:", num_clones,
                  str(100*float(num_clones)/totalIterations)+"%")
        printSave("    num of mutations in the execution:", num_mutated,
                  str(100*float(num_mutated)/totalIterations)+"%")
        printSave("    best path: ", best)
        printSave("    worst path:", fitness(mazeWeight, finalPopulation[-1]))
        printSave("    ratio best-shortest paths:", ratioBestShortPath)
        printSave("    improvement:", ratioBestShortPathInitPop -
                                      ratioBestShortPath)
        printSave("    Is posible find the Shortest-Path from paths:", can, final=True)
        print

        o = open( path.join(folder, folderFinalPop, nameFinalPop), 'wb')
        savePaths.saveListOfPaths(finalPopulation, o)
        pickle.dump(num_clones, o)
        pickle.dump(num_mutated, o)
        o.close()
        ####################################################################

    # increment counters
    o_counters = open( path.join(folder, folderFinalPop, 'counters'),'wb')
    o_counters.write(str(counters))
    o_counters.close()

  statistics_initial.close()
  statistics_final.close()


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
