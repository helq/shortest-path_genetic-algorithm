from definitions import *
from random import randint, random
from pathsOfMaze import findIntersections, findPath
from math import floor
from heapq import heapify, heappush

def crossingPaths(height, width, path1, path2):
    crossPoints = findIntersections(height, width, path1, path2)

    lenCrossPoints = len(crossPoints)
    if lenCrossPoints <= 2:
        return None

    i = 0
    found = False
    while not found:
        if i > lenCrossPoints:
            return None

        if random() < 0.20:
            k = randint(0, lenCrossPoints-2)
            l = k+1
            reverse = False
        else:
            l = randint(0, lenCrossPoints-2)
            k = l+1
            reverse = True

        [(s1k,s2k), (f1k,f2k)] = crossPoints[k]
        [(s1l,s2l), (f1l,f2l)] = crossPoints[l]

        if s2l > s2k:
            found = True

        i+=1

    # creating the new path
    if not reverse:
        return path2[:f2k] + path1[f1k:s1l] + path2[s2l:], k, l
    else:
        return path2[:s2k] + path1[s1k:f1l:-1] + path2[f2l:], k, l

def mutatePath(maze0, path):
    maze = [x[:] for x in maze0]
    height = len(maze)
    width = len(maze[0])

    lenPath = len(path)
    sizeMutation = int(floor(max(0.05*lenPath, lenPath*(random()/5))))
    startMut = randint(1, lenPath-sizeMutation-2)
    endMut = startMut+sizeMutation

    for (i,j) in path[:startMut]:
        if i>=0 and i<height and j>=0 and j<width:
            addMark(maze, i, j)
    for (i,j) in path[endMut+1:]:
        if i>=0 and i<height and j>=0 and j<width:
            addMark(maze, i, j)

    startPoint = path[startMut] + (NOTHING,)
    endPoint   = path[endMut] + (NOTHING,)

    return path[:startMut] + findPath(maze, startPoint, endPoint) + path[endMut+1:]

def fitness(mazeWeight, path):
    height = len(mazeWeight)
    width = len(mazeWeight[0])

    w = 0
    for (i,j) in path:
        if i>=0 and i<height and j>=0 and j<width:
            w+=mazeWeight[i][j]
    return w

def evolutionAlgo( maze, mazeWeight, initialPopulation, mutPercent
                 , totalPopulation, totalIterations, numberOfBadIndividuals
                 , randomVariableFunction):

    def getTwoNumbers(n):
        b = a = int( n * randomVariableFunction(random()) )
        while a == b:
            b = int( n * randomVariableFunction(random()) )
        return a,b

    height = len(maze)
    width = len(maze[0])

    population = [
                    (fitness(mazeWeight, individual), individual[:])
                    for individual in initialPopulation
                 ]
    heapify(population)

    num_clones = 0
    num_mutated = 0
    for i in range(totalIterations):
        if len(population) >= totalPopulation:
            toKill = randint(totalPopulation-numberOfBadIndividuals, totalPopulation-1)
            population.sort()
            population.pop(toKill)

            # deleting repeated individuals (clones XD)
            j=0
            while j < len(population)-1:
                if population[j] == population[j+1]:
                    population.pop(j+1)
                    num_clones+=1
                else:
                    j+=1


        if random() < mutPercent:
            toMutate = population[randint(0, len(population)-1)]
            mutated = mutatePath(maze, toMutate[1])

            # is realy a mutation?
            if mutated != toMutate[1]:
                num_mutated += 1
                heappush( population, (fitness(mazeWeight, mutated), mutated) )
        else:
            n1, n2 = getTwoNumbers(len(population))
            path1 = population[n1][1]
            path2 = population[n2][1]
            newPath = crossingPaths(height, width, path1, path2)
            if newPath == None:
                continue
            else:
                heappush( population
                        , (fitness(mazeWeight, newPath[0]), newPath[0]) )

    population.sort()
    # killing clones
    j=0
    while j < len(population)-1:
        if population[j] == population[j+1]:
            population.pop(j+1)
            num_clones+=1
        else:
            j+=1

    return (
                [individual[1] for individual in sorted(population)]
              , num_clones
              , num_mutated
           )
