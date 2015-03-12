#!/usr/bin/python
# -*- coding: utf-8 -*-
# optimization ideas
# - cache length
# - bitarrays
# - searcn only nearest 5% nodes : FIXME: grabbing to few poitns. 
# x after half way evaluate avg length, if more than existing avg, reduce to 25%
# - crossing check - with lines crossing it's not going to be optimal
# - use bitarray

import math

def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    Plotter = False
    
    #optimizer switch
    Halfwasted = False
    Goodpal = True
    # TODO: remember to turn this off
    #fh = open('calculation.csv', 'w')
    startts = time.time()
    #fh.write("time,length\n")
    lines = inputData.split('\n')

    nodeCount = int(lines[0])
    if ( Halfwasted ):
        halfnodeCount = int(math.ceil(nodeCount/2))
        quarternodeCount = int(math.ceil(nodeCount/4))
    
    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))
    
    if ( Goodpal ):
        candidates = getCandidates(points, 0.1)
        ''' # used for looking at possible points
        idx = 0
        while (1) :
            pyplot.clf()
            pyplot.scatter([p[0] for p in points], [p[1] for p in points])
            pyplot.scatter(points[idx][0], points[idx][1], c='g')
            pyplot.scatter([points[p][0] for p in candidates[idx]], [points[p][1] for p in candidates[idx]], c='r')
            pyplot.show()
            idx += 1
            #time.sleep(2)
        '''

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    randomSolution = range(0, nodeCount)

    # get a basic random algorithm
    random.shuffle(randomSolution)
    
    solution = randomSolution
    
    maxLength = solLength(solution, points)
    #maxLength = 1000
    avgLength = maxLength/nodeCount

    print 'random solution starts with ' + str(maxLength)
    nodes = set(range(0, nodeCount))
    solutions = []
    tracker = []
    currentCity = {}
    # may start from a random point later
    currentCity['name'] = random.randint(0, nodeCount-1)
    currentCity['connected'] = [currentCity['name']]
    currentCity['length'] = 0
    currentCity['tried'] = []
    tracker.append(currentCity)
    
    
    # depth first search and bound
    terminator = 0
    running = True
    print 'solving start'
    while ( running ):
        if ( Plotter ):
            pyplot.clf()
            idx = currentCity['name']
            pyplot.scatter([p[0] for p in points], [p[1] for p in points])
            pyplot.scatter(points[idx][0], points[idx][1], c='g')
            pyplot.scatter([points[p][0] for p in candidates[idx]], [points[p][1] for p in candidates[idx]], c='r')
            pyplot.plot([points[sol][0] for sol in currentCity['connected']], [points[sol][1] for sol in currentCity['connected']])
            pyplot.show()

        '''
        choice = [0] * nodeCount
        nextStep = None
        #choice = nodes.difference(currentCity['tried']).difference(set(currentCity['connected']))
        if ( Goodpal ):
            choice = [1] * nodeCount
            for i in candidates[currentCity['name']]:
                choice[i] = 0
        for i in currentCity['tried']:
            choice[i] = 1
        for i in currentCity['connected']:
            choice[i] = 1
        for key, value in enumerate(choice):
            if value == 0:
                nextStep = key
        '''
        # True is marking candidates
        choice = bitarray(nodeCount)
        nextStep = None
        if ( Goodpal ) :
            choice.setall(False)
            for i in candidates[currentCity['name']]:
                choice[i] = True
        else:
            choice.setall(True)
        for i in currentCity['tried']:
            choice[i] = False
        for i in currentCity['connected']:
            choice[i] = False
        if choice.any() == True:
            nextStep = int(choice.index(True)) #int for cosmetic
        #pprint(candidates[currentCity['name']])
        #pprint(nextStep)
        #pprint(currentCity['connected'])
        if nextStep != None:
            nextCity = {}
            nextCity['name'] = nextStep
            nextCity['connected'] = list(currentCity['connected'])
            nextCity['connected'].append(nextCity['name'])
            nextCity['length'] = currentCity['length'] + length(points[nextCity['name']], points[currentCity['name']])
            nextCity['tried'] = []
            currentCity['tried'].append(nextCity['name'])
            progress = len(nextCity['connected'])
            # solution quality evaluation
            if ( nextCity['length'] >= maxLength ):
                currentCity = currentCity
                # continue
            elif Halfwasted and( (progress == halfnodeCount) and ((nextCity['length']/progress) > avgLength) ):
                # roll back to quarter
                #print 'avg at half way is ' + str(nextCity['length']/progress) + ', ' + str((nextCity['length']/progress)-avgLength) + ' more'
                currentCity = tracker[quarternodeCount]
                currentCity['tried'].append(tracker[quarternodeCount+1]['name'])
                del tracker[(quarternodeCount+1):]
            else:
                if ( len(nextCity['connected']) == nodeCount ):
                    # found a solution
                    totalLength = nextCity['length'] + length(points[nextCity['name']], points[nextCity['connected'][0]])
                    print 'found a solution with length ' + str(totalLength)
                    terminator += 1
                    running = False
                    if terminator > 10000:
                        print 'hitting terminator count ' + str(totalLength)
                        running = False
                    solutions.append((list(nextCity['connected']), totalLength))
                    # this funciton should get rid of inferior solutions, sets maxLength
                    maxLength = pruneSolutions(solutions)
                    avgLength = maxLength/nodeCount
                    print 'choosing with length ' + str(maxLength)
                    #fh.write(str(time.time() - startts)+','+str(maxLength)+"\n")
                    # FIXME: restart from the last point with possible branches
                    currentCity = tracker[-2]
                    tracker.pop(-1)
                    continue
                else :
                    # not a solution yet, keep going
                    tracker.append(nextCity)
                    currentCity = nextCity
        else:
            # search exhausted on the current level
            # backtrack to a city with options, while loop will do the job
            # slice everything below
            if ( len(tracker) == 1 ):
                print 'loop finished b/c search exsausted'
                running = False
            else :
                print 'backtracking: connected ' + str(len(currentCity['connected'])) + ' points'
                currentCity = tracker[-2]
                tracker.pop(-1)
        #currentCity = nextCity
    
    #pprint(solutions)
    solution = solutions[0][0]
    
    pyplot.scatter([p[0] for p in points], [p[1] for p in points])
    pyplot.plot([points[sol][0] for sol in solution], [points[sol][1] for sol in solution])
    pyplot.show()
    
    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))
    #fh.close()
    return outputData

def getCandidates(points, area):
    #area in a node count sense
    nodeCount = len(points)
    xsorted = sorted(enumerate(points), key = lambda item: item[1][0])
    ysorted = sorted(enumerate(points), key = lambda item: item[1][1])
    
    xsorted = [d[0] for d in xsorted]
    ysorted = [d[0] for d in ysorted]
    ptsSorted = [xsorted, ysorted]
    
    margin = math.sqrt(area)
    ptMargin = int(math.ceil(margin * nodeCount))
    orighalfMargin = ptMargin/2
    marginEven = 1 if ptMargin % 2 == 0 else 0

    candidates = [None]*nodeCount
    pointsSet = set(range(0, nodeCount))
    
    for key, pt in enumerate(points):
        #xkey = xsorted.index(key)
        #ykey = ysorted.index(key)
        keys = [xsorted.index(key), ysorted.index(key)]
        if keys[0] == -1 or keys[1] == -1:
            print 'index not found'
            exit()
        candidate = [None] * len(keys)
        halfMargin = orighalfMargin
        filled = False
        while ( not filled ) :
            for skey, value in enumerate(keys):
                if (value+1) < halfMargin:
                    keys[skey] = int(math.ceil(halfMargin))
                elif ( value+1 ) > (nodeCount - halfMargin ):
                    keys[skey] = int(math.ceil(nodeCount - halfMargin))
            # pick #ptMargin of points, my keys consistently point to the left half's end
                candidate[skey] = set(ptsSorted[skey][(keys[skey]-int(math.floor(halfMargin))):(keys[skey]+int(math.floor(halfMargin))+ marginEven)])
            prunedC = candidate[0].intersection(candidate[1])
            if len(prunedC) >= ( area*nodeCount ):
                filled = True
            else:
                #print 'halfMargin ' + str(halfMargin) + ' too small. Got only number ' + str(len(prunedC)) + want
                halfMargin += int(math.floor(nodeCount*0.05))
        prunedC.remove(key)
        candidates[key] = prunedC
        
    return candidates
    
    
    
def pruneSolutions(solutions):
    foo, minlength = min(solutions, key = lambda item:item[1])
    solutions[:] = (sol for sol in solutions if abs(sol[1] - minlength) < 0.01) # this is ugly, i am learning
    return minlength
    
        
def solLength(solution, points):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, len(solution)-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

import sys
import random
from matplotlib import pyplot
from pprint import pprint
import cProfile
import time
from bitarray import bitarray

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        #cProfile.run('solveIt(inputData)')
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

