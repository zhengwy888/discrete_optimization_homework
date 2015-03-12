#!/usr/bin/python
# -*- coding: utf-8 -*-
# optimization ideas
# x cache length
# x bitarrays
# x searcn only nearest 5% nodes : right now using 0.1 as area
# x after half way evaluate avg length, if more than existing avg, reduce to 25%
# x crossing check - with lines crossing it's not going to be optimal

import math

def length_notCached(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

LengthCache = dict()
def length(point1, point2):
    if Cache:
        keypair = sorted([point1[2], point2[2]])
        if ( keypair[0] not in LengthCache ):
            LengthCache[keypair[0]] = dict()
        if ( keypair[1] not in LengthCache[keypair[0]] ):
            LengthCache[keypair[0]][keypair[1]] = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return LengthCache[keypair[0]][keypair[1]]
    else :
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # clean up global variables
    global LengthCache
    global Cache 
    LengthCache = dict()
    # parse the input
    Plotter = False
    
    Logger = False
    #optimizer switch
    Halfwasted = False
    Goodpal = False
    Cache = True
    CHP = True
    Doubleopt = True
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
        if ( Cache ):
            points.append((float(parts[0]), float(parts[1]), i-1))
        else :
            points.append((float(parts[0]), float(parts[1])))
    
    if ( Goodpal or 1 ):
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
    solution = range(0, nodeCount)
    '''
    randomSolution = range(0, nodeCount)
    # get a basic random algorithm
    random.shuffle(randomSolution)
    #pprint(randomSolution)
    solution = [None] * nodeCount
    randomUniq = set()
    for i in range(0, nodeCount):
        index = random.randint(0,nodeCount-1)
        while (index in randomUniq):
            index = random.randint(0, nodeCount-1)
        solution[i] = index
        randomUniq.add(index)
    print 'solution has ' + str(len(set(solution)))        
        for i in range(0, nodeCount):
            if ( nodetags[i] == nodetags[0] ):
                print 'premature loop at ' + str(i) + 'with ' + str(nodetags[i])
            if ( nodetags[i] == None ) :
                print 'none at ' + str(i)
                
        solution = [None]* nodeCount
        current = nodetags[0]
        for i in range(0, nodeCount):
            if solution[i] != None:
                print 'what are you doing with ' +str(i)
            if current == solution[0]:
                print 'loop started at ' + str(i)
                print 'current ' +str(current)
            solution[i] = current
            current = nodetags[current]
        print 'solution length '+str(len(solution))
        tracker = [0] * nodeCount
        counter = 0
        for tag in solution:
            counter += 1
            if tracker[tag] == 1:
                print str(tag) + ' has marked before'
            tracker[tag] = 1
        print 'for loop ' + str(counter)
        for key,t in enumerate(tracker):
            if t == 0:
                pass
        print 'it is not the SAME!!'
        #solution[-1] = nodetags[-1]
        if len(set(solution)) != nodeCount:
            print 'solution only have ' + str(len(set(solution))) + ' nodes'
    '''

    
    maxLength = solLength(solution, points)
    maxLength0 = maxLength
    #maxLength = 1000
    avgLength = maxLength/nodeCount
    if ( Doubleopt ):
        nodetags = [None] * nodeCount
        for i in range(0, nodeCount-1):
            current = solution[i]
            nodetags[current] = solution[i+1]
        nodetags[nodeCount-1] = solution[0]
        if len(set(nodetags)) != nodeCount:
            print 'solution only have ' + str(len(set(nodetags))) + ' nodes'

        terminator = 0
        running = True
        while (running):
            volunteer = random.randint(0, nodeCount-1)
            # optimize with neighbours
            if ( Goodpal ):
                volunteercandy = random.randint(0, len(candidates[volunteer])-1)
                while ( nodetags[volunteer] == candidates[volunteer][volunteercandy] ) :
                    volunteercandy -= 1;
                volunteertwo = candidates[volunteer][volunteercandy]
            else:
                randoming = True
                while ( randoming ):
                    volunteertwo = random.randint(0, nodeCount-1)
                    if ( volunteertwo != nodetags[volunteer] ) and (volunteertwo != volunteer) and ( nodetags[volunteertwo] != volunteer):
                        randoming = False
            workspace = [volunteer, nodetags[volunteer], volunteertwo, nodetags[volunteertwo]]
            lengths = []
            lengths.append(length(points[workspace[0]], points[workspace[1]]) + length(points[workspace[2]], points[workspace[3]]))
            lengths.append(length(points[workspace[0]], points[workspace[2]]) + length(points[workspace[1]], points[workspace[3]]))
            #lengths.append(length(points[workspace[0]], points[workspace[3]]) + length(points[workspace[2]], points[workspace[1]]))
            if lengths[0] <= lengths[1]:
                # original is the smallest
                #print 'not optimizing'
                pass
            else:
                nodetags[workspace[0]] = workspace[2]
                current = workspace[1]
                prev = workspace[3]
                #chaos = True
                while ( True ):
                    next = nodetags[current]
                    nodetags[current] = prev
                    if ( current == workspace[2] ):
                        break
                    prev = current
                    current = next 
                    
                maxLength = maxLength - (lengths[0] - lengths[1])
                #print 'optimized ' + str(lengths[0] - lengths[1])
                '''
                solution = []
                for i in nodetags:
                    solution.append(nodetags[i])
                print 'maxLength ' + str(maxLength) + ' actual ' + str(solLength(solution, points))
                '''
            terminator += 1
            if ( terminator == 20000 ):
                Goodpal = True
            if ( terminator == 40000):
                running = False

        print 'total optimized ' + str(maxLength - maxLength0) + ' from ' + str(maxLength0) + ' to ' + str(maxLength)
        solution = [None]* nodeCount
        current = 0
        for i in range(0, nodeCount):
            current = nodetags[current]
            solution[i] = current
        #solution[-1] = nodetags[-1]
        if len(set(solution)) != nodeCount:
            print 'solution only have ' + str(len(set(solution))) + ' nodes'
        if ( Plotter ):
            pyplot.scatter([p[0] for p in points], [p[1] for p in points])
            pyplot.plot([points[sol][0] for sol in solution], [points[sol][1] for sol in solution])
            pyplot.show()
        return
        
    if ( Logger ) :
        fh = open('calculation.csv', 'w')
        fh.write("time,length\n")
        fh.write(str(time.time() - startts)+','+str(maxLength)+"\n")
    print 'random solution starts with ' + str(maxLength)
    nodes = set(range(0, nodeCount))
    solutions = []
    tracker = []
    currentCity = {}
    currentCity['name'] = random.randint(0, nodeCount-1)
    currentCity['connected'] = [currentCity['name']]
    currentCity['length'] = 0
    currentCity['tried'] = []
    tracker.append(currentCity)
    
    
    # depth first search and bound
    terminator = 0
    running = True
    while ( running ):
        if ( Plotter ):
            pyplot.clf()
            idx = currentCity['name']
            pyplot.scatter([p[0] for p in points], [p[1] for p in points])
            pyplot.scatter(points[idx][0], points[idx][1], c='g')
            pyplot.plot([points[sol][0] for sol in currentCity['connected']], [points[sol][1] for sol in currentCity['connected']])
            if ( Goodpal ) :
                pyplot.scatter([points[p][0] for p in candidates[idx]], [points[p][1] for p in candidates[idx]], c='r')
            if ( len(currentCity['tried']) > 0):
                pyplot.scatter([points[sol][0] for sol in currentCity['tried']], [points[sol][1] for sol in currentCity['tried']], c='k')
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
        print str(len(currentCity['connected'])) + ' cities connected'
        #pprint(candidates[currentCity['name']])
        #pprint(nextStep)
        #pprint(currentCity['connected'])
        if nextStep != None:
            nextCity = {}
            if CHP:
                if testIntersect(points, currentCity['connected'], nextStep):
                    currentCity['tried'].append(nextStep)
                    continue
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
                    running = False
                    terminator += 1
                    if terminator > 10000:
                        running = False
                    solutions.append((list(nextCity['connected']), totalLength))
                    # this funciton should get rid of inferior solutions, sets maxLength
                    maxLength = pruneSolutions(solutions)
                    avgLength = maxLength/nodeCount
                    print 'choosing with length ' + str(maxLength)
                    if ( Logger ):
                        fh.write(str(time.time() - startts)+','+str(maxLength)+"\n")
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
    
    solution = solutions[0][0]
    
    if ( Plotter ) :
        # plotter
        pyplot.ion()
        figure = pyplot.figure()
        ax = figure.add_subplot(111)
        ax.scatter([p[0] for p in points], [p[1] for p in points])
        line1, = ax.plot([points[sol][0] for sol in solution], [points[sol][1] for sol in solution])
        while (1) :
            line1.set_data([points[sol][0] for sol in solution], [points[sol][1] for sol in solution])
            figure.canvas.draw()
            break
            #time.sleep(1)
        

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))
    if Logger:
        fh.close()
    return outputData

def fakeSolve():
    global Cache 
    Cache = True
    global LengthCache
    print str(length([1,1,1], [1,2,1]))
    pprint(LengthCache)
    LengthCache = dict()
    print 'lengthcache cleaned'
    print str(length([1,1,1], [1,2,1]))
    pprint(LengthCache)

    
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
        candidates[key] = list(prunedC)
        
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

# return:
#   False - no intersection
#   True - has intersection
def testIntersect(points, connected, next):
    cpoints = []
    cpoints[:] = [(idx, points[idx]) for idx in connected]
    cpoints.append((next, points[next]))
    #simple sort, if both end points is on the sameside then 
    xsorted = sorted(cpoints, key = lambda item: item[1][0])
    xsorted = [d[0] for d in xsorted]
    boundone = xsorted.index(connected[-1])
    boundtwo = xsorted.index(next)
    boundleft, boundright = sorted([boundone, boundtwo])
    # minus 2 to skip the directly connected section
    for i in range(0, len(connected)-2) :
        idone = xsorted.index(connected[i])
        idtwo = xsorted.index(connected[i+1])
        if idone <= boundleft and idtwo <= boundleft:
            continue;
        elif idone >= boundright and idtwo >= boundright :
            continue;
        else:
            if ( isIntersect(points[connected[i]], points[connected[i+1]], points[connected[-1]], points[next] )):
                return True

    return False
    
    
# one* are line one, two* are line two
# algorithm comes from http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
def isIntersect(onel, oner, twol, twor):
    # t = (q - p) �� s / (r �� s)
    # u = (q - p) �� r / (r �� s)
    #  if 0 �� t �� 1 and 0 �� u �� 1, the two line intersect
    s = [(twor[i] - twol[i]) for i in range(0,2)]
    r = [(oner[i] - onel[i]) for i in range(0,2)]
    q = twol
    p = onel
    
    qmp = ((q[0] - p[0]), (q[1] - p[1]))
    rxs = r[0]*s[1] - r[1]*s[0]
    if ( rxs == 0 ):
        #two lines are parallel or colinear, but tsp, can only be parallel
        return False
    else :
        t = (qmp[0] * s[1] - qmp[1]*s[0]) / rxs
        u = (qmp[0] * r[1] - qmp[1]*r[0]) / rxs
        if ( 0 <= t) and ( t <= 1 ) and (0<=u) and (u<=1):
            return True
    return False
    
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
        cProfile.run('solveIt(inputData)')
        #print solveIt(inputData)
        #print isIntersect([42.0, 57.0], [43.0, 67.0], [43.0, 67.1], [37.0, 69.0])
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

