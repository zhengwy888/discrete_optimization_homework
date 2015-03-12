#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))
    
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    randomSolution = range(0, nodeCount)

    # get a basic random algorithm
    random.shuffle(randomSolution)
    
    solution = randomSolution
    
    maxLength = solLength(solution, points)
    print 'random solution starts with ' + str(maxLength)
    nodes = set(range(0, nodeCount))
    solutions = []
    tracker = []
    currentCity = {}
    # may start from a random point later
    currentCity['name'] = random.randint(0, nodeCount-1)
    currentCity['connected'] = [currentCity['name']]
    currentCity['length'] = 0
    currentCity['tried'] = set()
    tracker.append(currentCity)
    
    # depth first search and bound
    terminator = 0
    running = True
    while ( running ):
        choice = nodes.difference(currentCity['tried']).difference(set(currentCity['connected']))
        #pprint(choice)
        #pprint(currentCity['connected'])
        if len(choice) != 0:
            nextCity = {}
            nextCity['name'] = choice.pop()
            nextCity['connected'] = list(currentCity['connected'])
            nextCity['connected'].append(nextCity['name'])
            nextCity['length'] = currentCity['length'] + length(points[nextCity['name']], points[currentCity['name']])
            nextCity['tried'] = set()
            currentCity['tried'].add(nextCity['name'])
            if ( nextCity['length'] >= maxLength ):
                currentCity = currentCity
                # continue
            else:
                if ( len(nextCity['connected']) == nodeCount ):
                    # found a solution
                    totalLength = nextCity['length'] + length(points[nextCity['name']], points[nextCity['connected'][0]])
                    print 'found a solution with length ' + str(totalLength)
                    ## TODO: turn this off
                    error = abs(totalLength - solLength(nextCity['connected'], points))
                    if error > 0.01:
                        print 'length differ from ' + str(totalLength) + ' to ' + str(solLength(nextCity['connected'], points))
                        exit(1)
                    solutions.append((list(nextCity['connected']), totalLength))
                    # this funciton should get rid of inferior solutions, sets maxLength
                    maxLength = pruneSolutions(solutions)
                    print 'staying with length ' + str(maxLength)
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
                currentCity = tracker[-2]
                tracker.pop(-1)
        #currentCity = nextCity
    
    solution = solutions[0][0]
    # plotter
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

    return outputData

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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

