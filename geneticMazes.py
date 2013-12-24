#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from src.createMazes import createRandomMaze, deleteWalls, simplifyMaze
from src.pathsOfMaze import findPath
from src.genetics import fitness, evolutionAlgo
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
      --dim=n,m              dimensions of the maze *
  -d --wallsToDel=float      percent of the walls to delete *
  -s --sizeInitial=num       size of initial population
  -m --mutationPercent=float percent of mutation, probability of mutate in a
                             determined cycle (iteration)
  -t --totalPopulation=num   maximum size of the population
  -i --totalIterations=num   number of iterations
  -b --badIndividuals=num    number of `bad' individuals, they have the worst
                             fitness value
  -c --chooseFunction=funct  the individuals for mutation are elected randomly
                             according to this function (have to be writed in
                             python syntax. ex: `-f "lambda x: x"')

  -F --folder=name           folder to save the results
  -I --initialPop=num        use an exisisting population (num of the
                             population in """+folderInitialPop+""")
                             This overwrite the option `-s'

  * setted only when the folder doesn't exist

to save paths in a PNG see `pathsToPNG.py'
"""

def main(folder):
    if 'initialPop' in options: initialPop = options['totalIterations']
    elif        'I' in options: initialPop = options['I']
    else:                       initialPop = None

    if             'dim' in options: n, m = eval('('+options['dim']+')')
    else:                            n, m = 60, 70

    if      'wallsToDel' in options: wallsToDel = float(options['wallsToDel'])
    elif             'd' in options: wallsToDel = float(options['d'])
    else:                            wallsToDel = 0.10

    if     'sizeInitial' in options: sizeInitial = int(options['sizeInitial'])
    elif             's' in options: sizeInitial = int(options['s'])
    else:                            sizeInitial = 15

    if 'mutationPercent' in options: mutPercent = float(options['mutationPercent'])
    elif             'm' in options: mutPercent = float(options['m'])
    else:                            mutPercent = 0.10

    if 'totalPopulation' in options: totalPopulation = int(options['totalPopulation'])
    elif             't' in options: totalPopulation = int(options['t'])
    else:                            totalPopulation = 50

    if 'totalIterations' in options: totalIterations = int(options['totalIterations'])
    elif             'i' in options: totalIterations = int(options['i'])
    else:                            totalIterations = 200

    if  'badIndividuals' in options: badIndividuals = int(options['badIndividuals'])
    elif             'i' in options: badIndividuals = int(options['b'])
    else:                            badIndividuals = 10

    if  'chooseFunction' in options: chooseFunction = eval(options['chooseFunction'])
    elif             'c' in options: chooseFunction = eval(options['c'])
    else:                            chooseFunction = lambda x: x
    #chooseFunction = lambda x: (0.6/0.5)*x if x<0.6 else (x-1)*((1-0.5)/(1-0.6)) + 1

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
        mazeWeigth = pickle.load(o)
        o.close()
    else:
        maze = deleteWalls(createRandomMaze(n, m), wallsToDel)
        mazeSimple = simplifyMaze(maze)
        mazeWeigth = [[random() for j in range(m)] for i in range(n)]

        o = open( path.join(folder, mazeFile), 'wb')
        pickle.dump(n, o)
        pickle.dump(m, o)
        pickle.dump(wallsToDel, o)
        pickle.dump(maze, o)
        pickle.dump(mazeSimple, o)
        pickle.dump(mazeWeigth, o)
        o.close()

    print "variables setted to:"
    print "dimensions: ("+str(n)+", "+str(m)+")"
    print "walls deleted (percentage):", wallsToDel

    ######################## initial Population #######################
    if initialPop == None:
        counter = int(open( path.join(folder, folderInitialPop, 'counter'),'rb').read())

        initialPopulation = [findPath(mazeSimple) for i in range(sizeInitial)]
        initialPopulation.sort(key=lambda i: fitness(mazeWeigth, i))
        nameInitialPop = str(counter).zfill(3)
        o = open( path.join(folder, folderInitialPop, nameInitialPop), 'wb')
        pickle.dump(initialPopulation, o)
        o.close()

        open( path.join(folder, folderInitialPop, 'counter'),'wb').write(str(counter+1))
    else:
        counter = int(initialPop, 10)
        nameInitialPop = str(counter).zfill(3)
        o = open( path.join(folder, folderInitialPop, nameInitialPop), 'rb')
        initialPopulation = pickle.load(o)
        o.close()

    ##################################################################

    print "initial size Population:", len(initialPopulation)
    print "mutation (percentage):", mutPercent
    print "total population:", totalPopulation
    print "total iterations:", totalIterations
    print "number of bad individuals:", badIndividuals
    print

    print "statistics"
    print "initial population", nameInitialPop
    print "best path: ", fitness(mazeWeigth, initialPopulation[0])
    print "worst path:", fitness(mazeWeigth, initialPopulation[-1])
    print


    ####################### final population #######################
    finalPopulation, num_clones = evolutionAlgo(
            maze, mazeWeigth, initialPopulation , mutPercent,
            totalPopulation, totalIterations , badIndividuals,
            chooseFunction)

    counters = eval(open( path.join(folder, folderFinalPop, 'counters'),'rb').read())
    if len(counters) <= counter:
        counters.extend( [-1]*(counter-len(counters)) )
        counters.append(0)
    else:
        counters[counter] += 1

    print "num of clones in the ejecution:", num_clones
    print

    nameFinalPop = str(counter).zfill(3)+'-'+str(counters[counter]).zfill(3)
    print "final population", nameFinalPop
    print "best path: ", fitness(mazeWeigth, finalPopulation[0])
    print "worst path:", fitness(mazeWeigth, finalPopulation[-1])

    o = open( path.join(folder, folderFinalPop, nameFinalPop), 'wb')
    pickle.dump(finalPopulation, o)
    o.close()
    open( path.join (folder, folderFinalPop, 'counters'),'wb').write(str(counters))


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
