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

def mutatePath(maze0, path, border=5):
    maze = [x[:] for x in maze0]
    height = len(maze)
    width = len(maze[0])

    lenPath = len(path)
    sizeMutation = int(floor(max(0.05*lenPath, lenPath*(random()/5))))
    startMut = randint(1, lenPath-sizeMutation-2)
    endMut = startMut+sizeMutation

    maxI, maxJ = -1, -1
    minI, minJ = height, width
    for i,j in path[startMut:endMut+1]:
        if i > maxI: maxI = i
        if j > maxJ: maxJ = j
        if i < minI: minI = i
        if j < minJ: minJ = j
    minI = max(minI-border, -1)
    minJ = max(minJ-border, -1)
    maxI = min(maxI+border, height)
    maxJ = min(maxJ+border, width)

    for i in range(minI, maxI+1):
        if i>=0 and i<height:
            if minJ>=0:    addMark(maze, i, minJ)
            if maxJ<width: addMark(maze, i, maxJ)
    for j in range(minJ, maxJ+1):
        if j>=0 and j<width:
            if minI>=0:     addMark(maze, minI, j)
            if maxI<height: addMark(maze, maxI, j)

    for (i,j) in path[:startMut]:
        if i>=0 and i<height and j>=0 and j<width:
            addMark(maze, i, j)
    for (i,j) in path[endMut+1:]:
        if i>=0 and i<height and j>=0 and j<width:
            addMark(maze, i, j)

    startPoint = path[startMut] + (NOTHING,)
    endPoint   = path[endMut] + (NOTHING,)

    mutated = path[:startMut] + findPath(maze, startPoint, endPoint) + path[endMut+1:]

    return mutated, path[startMut], path[endMut]

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
                 , isInitPopInmut, randomVariableFunction):

    lenInitPop = len(initialPopulation)
    def getTwoNumbers(n):
        b = a = int( n * randomVariableFunction(random()) )
        while a == b:
            b = int( n * randomVariableFunction(random()) )
        return a,b

    height = len(maze)
    width = len(maze[0])

    population = [
                    (fitness(mazeWeight, individual), individual[:], isInitPopInmut)
                    for individual in initialPopulation
                 ]
    heapify(population)

    num_clones = 0
    num_mutated = 0
    i = 0
    while i < totalIterations:
        if len(population) >= totalPopulation:
            population.sort()
            someone_killed = False
            k = 0
            while not someone_killed:
                if initialPopulation and numberOfBadIndividuals + k <= lenInitPop + 1:
                    k+=1
                toKill = randint(
                            totalPopulation-numberOfBadIndividuals-k,
                            totalPopulation-1
                            )
                if not population[toKill][2]:
                    population.pop(toKill)
                    someone_killed = True

            # deleting repeated individuals (clones XD)
            j=0
            while j < len(population)-1:
                if population[j] == population[j+1]:
                    population.pop(j+1)
                    num_clones+=1
                else:
                    j+=1

        # mutate
        if random() < mutPercent:
            toMutate = population[randint(0, len(population)-1)]
            mutated, p1, p2 = mutatePath(maze, toMutate[1])

            # is really a mutation?
            if mutated != toMutate[1]:
                num_mutated += 1
                heappush( population, (fitness(mazeWeight, mutated), mutated, False) )
                i+=1
        # combine
        else:
            n1, n2 = getTwoNumbers(len(population))
            path1 = population[n1][1]
            path2 = population[n2][1]
            newPath = crossingPaths(height, width, path1, path2)
            # is really a new path
            if newPath != None:
                heappush( population
                        , (fitness(mazeWeight, newPath[0]), newPath[0], False) )
                i+=1

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
