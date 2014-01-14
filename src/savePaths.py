#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import array
import pickle

def saveListOfPaths(paths, f):
    pickle.dump(len(paths), f)
    for i in paths:
        savePath(i, f)

def loadListOfPaths(f):
    lenPaths = pickle.load(f)
    paths = []
    for i in range(lenPaths):
        paths.append(loadPath(f))

    return paths

def savePath(path, f):
    a = _compressPath(path)
    lenA, lenPath = len(a), len(path)
    pickle.dump(lenPath, f)
    pickle.dump(lenA, f)
    pickle.dump(path[0], f)
    a.tofile(f)

def loadPath(f):
    lenPath = pickle.load(f)
    lenA = pickle.load(f)
    point0 = pickle.load(f)
    a = array.array('B')
    a.fromfile(f, lenA)
    return _decompressPath(lenPath, point0, a)

pLEFT = 0
pUP = 1
pRIGHT = 2
pDOWN = 3
pNO_MORE = 4

def _getMove(point1, point2):
    if point2 == None: return pNO_MORE

    i, j = point1
    k, l = point2

    if (i, j-1) == (k, l): return pLEFT
    if (i-1, j) == (k, l): return pUP
    if (i, j+1) == (k, l): return pRIGHT
    if (i+1, j) == (k, l): return pDOWN

def _compressPath(path0):
    path = [x[:] for x in path0]
    mod = (len(path)-1)%4
    if mod != 0:
        path.extend([None]*(4-mod))

    a = array.array('B')
    for i in range(len(path)/4):
        b = 0
        for j in range(4*i, 4*i+4):
            m = _getMove(path[j], path[j+1])
            if m == pNO_MORE:
                break
            b <<= 2
            b |= m
        a.append(b)

    return a

def _moveToPoint((i,j), m):
    if m == pLEFT  : return (i,j-1)
    if m == pUP    : return (i-1,j)
    if m == pRIGHT : return (i,j+1)
    if m == pDOWN  : return (i+1,j)

def _decompressPath(lenPath, point0, a):
    path = [point0]
    k = 1
    for i in a:
        tmp = []
        for j in range(4):
            tmp.append(i&3)
            i>>=2
            k+=1
            if k >= lenPath:
                break
        for m in reversed(tmp):
            path.append( _moveToPoint(path[-1], m) )
    return path
