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
    Uglypal = True
    Cache = True
    CHP = False
    Doubleopt = True
    startts = time.time()
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
    
    if ( Goodpal ):
        candidates = getCandidates(points, 0.1) # not used
    if ( Uglypal ):
        candidates = getCandidates(points)


    #solution = range(0, nodeCount)
    if Uglypal:
        solution = [None] * nodeCount
        used = [0] * nodeCount
        paling = random.randint(0, nodeCount-1)
        prev = paling
        solution[0] = paling
        used[paling] = 1
        for i in range(1, nodeCount):
            pal = 0
            paling = candidates[prev][pal]
            maxpal = len(candidates[prev])
            #print 'neighbours count' + str(maxpal)
            while used[paling] == 1:
                if pal < (maxpal-1):
                    pal += 1
                    paling = candidates[prev][pal]            
                else:
                    paling = used.index(0)
            solution[i] = paling
            prev = paling
            used[paling] = 1
        # got a good initial solution
        maxLength = solLength(solution, points)
        
        #print 'maxLength is '+ str(maxLength)

    
    #maxLength = solLength(solution, points)
    maxLength0 = maxLength

    if ( Logger ) :
        fh = open('calculation_2opt.csv', 'w')
        fh.write("time,length\n")
        fh.write(str(time.time() - startts)+','+str(maxLength)+"\n")
    if ( Doubleopt ):
        nodetags = [None] * nodeCount
        for i in range(0, nodeCount-1):
            current = solution[i]
            nodetags[current] = solution[i+1]
        nodetags[solution[-1]] = solution[0]
        if len(set(nodetags)) != nodeCount:
            print 'solution only have ' + str(len(set(nodetags))) + ' nodes'

        terminator = 0
        running = True
        doubleoptStart = time.time()
        durationmin = 150
        doubleoptStop = int(doubleoptStart)+ durationmin * 60
        
        uselesspass = 0
        counter = 0
        usefultracker = []
        initqueue = range(0, nodeCount)
        numKicks = 0
        #random.shuffle(initqueue)
        #initlen = nodeCount
        temp = getTemperature()
        initlen = 0
        bestNodetags = []
        bestLength = 99999999999999999
        kickratio = 5
        while (running):
            counter += 1
            #volunteer = random.randint(0, nodeCount-1)
            # optimize with neighbours
            if ( counter % (nodeCount*100) == 0 ):
                #print 'reshuffling'
                initlen = nodeCount
            if ( initlen > 0 ) :
                if (initlen == nodeCount) :
                    random.shuffle(initqueue)
                Uglypal = False
                Randoming = True
                volunteer = initqueue[nodeCount - initlen]
                initlen -= 1
            else :
                Uglypal = True
                volunteer = random.randint(0, nodeCount-1)
            if ( Uglypal ):
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
            #if lengths[0] < lengths[1]:
            temp = getTemperature(temp)
            if ( temp <= 0 ) :
                break
                
            #print 'temperature ' + str(temp) + ' annealing prob ' + str(annealingProb( lengths[0], lengths[1] , temp )) + ' length orig ' + str(lengths[0]) + ' testing ' + str(lengths[1])
            #time.sleep(1)
            if annealingProb( lengths[0], lengths[1] , temp ) < random.random():
                # original is the smallest
                #print 'not optimizing'
                
                uselesspass +=1
                if ( uselesspass > nodeCount * kickratio):
                    temp = getTemperature() * (0.8**numKicks)
                    numKicks += 1
                    kickratio = int(kickratio * 1.2)
                    uselesspass = 0
                    if numKicks == 30:
                        running = False
                    #pass
                
            else:
                #usefultracker.append(counter)
                nodetags[workspace[0]] = workspace[2]
                current = workspace[1]
                prev = workspace[3]
                #clean up nodetags' direction
                while ( True ):
                    next = nodetags[current]
                    nodetags[current] = prev
                    if ( current == workspace[2] ):
                        break
                    prev = current
                    current = next 
                    
                maxLength = maxLength - (lengths[0] - lengths[1])
                if ( lengths[0] < lengths[1] ) :
                    #print 'wrong move at ' + str(time.time() - startts)
                    uselesspass +=1
                    pass
                else:
                    uselesspass -= kickratio
                    if maxLength < bestLength:
                        bestNodetags = list(nodetags)
                        bestLength = maxLength
                if ( Logger ):
                    fh.write(str(time.time() - startts)+','+str(maxLength)+"\n")
                #print 'optimized ' + str(lengths[0] - lengths[1]) + ' to ' + str(maxLength)
            if ( time.time() > doubleoptStop ):
                #print 'elapsed time ' + str(time.time() - doubleoptStart)
                running = False

        #print 'total optimized ' + str(maxLength - maxLength0) + ' from ' + str(maxLength0) + ' to ' + str(maxLength)
        #print str(counter - uselesspass) + " out of " + str(counter) + " passes optimized"
        #print ','.join(map(str, usefultracker))

        solution = [None]* nodeCount
        current = 0
        for i in range(0, nodeCount):
            current = bestNodetags[current]
            solution[i] = current
        #solution[-1] = nodetags[-1]
        if ( Plotter ):
            pyplot.scatter([p[0] for p in points], [p[1] for p in points])
            pyplot.plot([points[sol][0] for sol in solution], [points[sol][1] for sol in solution])
            pyplot.show()
        if Logger:
            fh.close()
            # prepare the solution in the specified output format
        obj = solLength(solution, points)
        outputData = str(obj) + ' ' + str(0) + '\n'
        outputData += ' '.join(map(str, solution))
        return outputData

        
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

def annealingProb(length0, length1, temp):
    if length1 < length0 :
        return 1
    else:
        #print 'temp now is ' + str(temp)
        return math.exp( -1*(length1-length0)/temp) # falls off at half way

'''        
def getTemperature(maxtime, startts):
    # completely based on time
    now = time.time()
    elapsed = now - startts
    total = maxtime - startts
    maxtemp = 50 * (0.1)
    #return 50 ** (((maxtime + 1 - now)/ (maxtime - startts))) - 0.9999999999 # fall off too quickly
    #return 1 * (1.001 - (elapsed / total))
'''    
def getTemperature(temp=3000):
    alpha = 0.9999
    # alpha^n 30 sec stable
    # t - n*alpha is not usable, too much error to begin with
    # alpha / log(t) too much trouble, negative hits too easily
    return temp*alpha
    
    
def getCandidates(points):
    #area in a node count sense
    nodeCount = len(points)
    xsorted = sorted(enumerate(points), key = lambda item: item[1][0])
    ysorted = sorted(enumerate(points), key = lambda item: item[1][1])
    
    xsorted = [d[0] for d in xsorted]
    ysorted = [d[0] for d in ysorted]
    ptsSorted = [xsorted, ysorted]

    ptMargin = int(math.floor(math.log10(nodeCount) * 2) *10 - 1 )- 10
    orighalfMargin = ptMargin/2
    candidates = [[]]*nodeCount
    #pointsSet = set(range(0, nodeCount))
    
    for key in range(0, nodeCount):
        #print 'getting neighbours for ' + str(key+1) + ' of ' + str(nodeCount)
        #xkey = xsorted.index(key)
        #ykey = ysorted.index(key)
        keys = [xsorted.index(key), ysorted.index(key)]
        if keys[0] == -1 or keys[1] == -1:
            print 'index not found'
            exit()
        halfMargin = orighalfMargin
        candidate = []
        for skey, value in enumerate(keys):
            if (value+1) < halfMargin:
                keys[skey] = halfMargin
            elif ( value+1 ) > (nodeCount - halfMargin ):
                keys[skey] = nodeCount - halfMargin
        # pick #ptMargin of points, my keys consistently point to the left half's end
            #candidate[skey] = set(ptsSorted[skey][(keys[skey]-int(math.floor(halfMargin))):(keys[skey]+int(math.floor(halfMargin))+ marginEven)])
            #print 'range looking is ' + str(keys[skey]-halfMargin+1) +' '+ str(keys[skey]+halfMargin)
            for i in range((keys[skey]-halfMargin+1), (keys[skey]+halfMargin)):
                if ptsSorted[skey][i] != key:
                    candidate.append(ptsSorted[skey][i])
        lengths = []
        tracker = {}
        for can in candidate:
            if can not in tracker:
                lengths.append([length(points[can], points[key]), can])
                tracker[can] = True
        lengths = sorted(lengths, key = lambda item:item[0])
        candidates[key] = tuple([ele[1] for ele in lengths])
  
    return candidates
    
def getCloseish(points):
    #area in a node count sense
    nodeCount = len(points)
    xsorted = sorted(enumerate(points), key = lambda item: item[1][0])
    ysorted = sorted(enumerate(points), key = lambda item: item[1][1])
    
    xsorted = [d[0] for d in xsorted]
    ysorted = [d[0] for d in ysorted]
    ptsSorted = [xsorted, ysorted]
    
    candidates = [None]*nodeCount
    pointsSet = set(range(0, nodeCount))
    
    for key, pt in enumerate(xsorted):
        tracker = [None]* nodeCount
        if key == 0:
            xkeys = [key+1, key+2]
        elif key == nodeCount-1:
            xkeys = [key-2, key-1]
        else:
            xkeys = [key+1, key-1]
        ykey = ysorted.index(pt)
        if ykey == 0:
            ykeys = [ykey+1, ykey+2]
        elif ykey == nodeCount-1:
            ykeys = [ykey-2, ykey-1]
        else:
            ykeys = [ykey+1, ykey-1]

        candidates[pt] = [xsorted[xkeys[0]], xsorted[xkeys[1]], ysorted[ykeys[0]], ysorted[ykeys[1]]]
        
    return candidates

def getClosesorted_notused(points):
    nodeCount = len(points)
    candidates = [None] * nodeCount
    #xcoor = np.empty([nodeCount, nodeCount], dtype=int)
    #ycoor = np.empty([nodeCount, nodeCount], dtype=int)
    lengthcoor = Matrix(nodeCount, nodeCount)
    #ycoor = Matrix(nodeCount, nodeCount)
    for i in range(0, nodeCount):
        for k in range(i+1, nodeCount):
            distance = length(points[i], points[k])
            lengthcoor[i][k] = distance
            lengthcoor[k][i] = distance
    
    for i in range(0, nodeCount):
        sortedlength = sorted(enumerate(lengthcoor[i]), key = lambda item:item[1])
        candidates[i] = tuple([ d[0] for d in sortedlength[1:] ])
    return candidates
    
def getClosesorted(points):
    # doesn't work, too much memory
    nodeCount = int(len(points))
    candidates = [None] * nodeCount
    #xcoor = np.empty([nodeCount, nodeCount], dtype=int)
    #ycoor = np.empty([nodeCount, nodeCount], dtype=int)
    lengthcoor = np.eye(nodeCount/4, nodeCount/4, dtype=float)
    np.multiply(lengthcoor, -1.0)
    print 'done allocating array'
    #ycoor = Matrix(nodeCount, nodeCount)
    for i in range(0, nodeCount):
        for k in range(i+1, nodeCount):
            distance = length(points[i], points[k])
            lengthcoor[i,k] = distance
            lengthcoor[k,i] = distance
    
    for i in range(0, nodeCount):
        sortedlength = sorted(enumerate(lengthcoor[i]), key = lambda item:item[1])
        candidates[i] = tuple([ d[0] for d in sortedlength[1:] ])
    return candidates
    
def Matrix(row, column, value=-1):
    return [[value for x in xrange(column)] for x in xrange(row)]

    
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
    # t = (q - p) ¡Á s / (r ¡Á s)
    # u = (q - p) ¡Á r / (r ¡Á s)
    #  if 0 ¡Ü t ¡Ü 1 and 0 ¡Ü u ¡Ü 1, the two line intersect
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
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        #cProfile.run('solveIt(inputData)')
        print solveIt(inputData)
        #print isIntersect([42.0, 57.0], [43.0, 67.0], [43.0, 67.1], [37.0, 69.0])
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

