#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

def length(customer1, customer2):
    return math.sqrt((customer1[1] - customer2[1])**2 + (customer1[2] - customer2[2])**2)

def solveIt(inputData):
    # Modify this code to run your optimization algorithm
    
    Plotter = False
    Polardivide = True
    TSP = True
    Shelter = True
    NeighbourWatch = True

    global DEBUG 
    DEBUG = True
    # parse the input
    lines = inputData.split('\n')

    parts = lines[0].split()
    customerCount = int(parts[0])
    vehicleCount = int(parts[1])
    vehicleCapacity = int(parts[2])
    depotIndex = 0

    customers = []
    for i in range(1, customerCount+1):
        line = lines[i]
        parts = line.split()
        customers.append((int(parts[0]), float(parts[1]),float(parts[2]), i-1))

    # plotter
    if ( Plotter and False):
        minsize = min([d[0] for d in customers[1:]])
        pprint(minsize)
        pyplot.scatter([d[1] for d in customers], [d[2] for d in customers], s=[d[0]/minsize*20 for d in customers])
        pyplot.scatter(customers[0][1], customers[0][2], c='r')
        pyplot.show()
    
    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands

    vehicleTours = []

    customerIndexs = set(range(1, customerCount))  # start at 1 to remove depot index
    
    for v in range(0, vehicleCount):
        # print "Start Vehicle: ",v
        vehicleTours.append([])
        capacityRemaining = vehicleCapacity
        while sum([capacityRemaining >= customers[ci][0] for ci in customerIndexs]) > 0:
            used = set()
            order = sorted(customerIndexs, key=lambda ci: -customers[ci][0])
            for ci in order:
                if capacityRemaining >= customers[ci][0]:
                    capacityRemaining -= customers[ci][0]
                    vehicleTours[v].append(ci)
                    # print '   add', ci, capacityRemaining
                    used.add(ci)
            customerIndexs -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicleTours]) == customerCount - 1

    if Polardivide:
        csxnp = np.array([d[1] - customers[0][1] for d in customers[1:]])
        csynp = np.array([d[2] - customers[0][2] for d in customers[1:]])
        csthetanp = np.arctan2(csynp, csxnp)
        csrnp = np.sqrt(np.power(csxnp, 2) + np.power(csynp,2))
        customerIndexs = set(range(1, customerCount))  # start at 1 to remove depot index
        ciSizeSorted = sorted(customerIndexs, key=lambda ci: -customers[ci][0])
        ciThetaSorted = sorted(customerIndexs, key=lambda ci: csthetanp[ci-1])
        
        vContainers = []
        capRemains = []
        cAdded = bitarray(customerCount)
        cAdded.setall(False)
        cAdded[0] = True #source
        running = True

        pprint(ciThetaSorted)
        for v in range(0, vehicleCount):
            if not running:
                break
            vContainer = []
            capRemain = vehicleCapacity
            leftpass = True
            rightpass = True
            
            idx = 0
            if ( False ): #size sorted
                c = ciSizeSorted[0]
                while cAdded[c]:
                    idx += 1
                    c = ciSizeSorted[idx]
                citheta = ciThetaSorted.index(c)
            else : #theta sorted
                # c = ciThetaSorted[0]
                # while cAdded[c]:
                    # idx += 1
                    # c = ciThetaSorted[idx]
                # citheta = ciThetaSorted.index(c)
                if cAdded.count(True) == 1:
                    citheta = random.randint(0, customerCount-2)
                    c = ciThetaSorted[citheta]
                else:
                    citheta = 1
                    c = ciThetaSorted[citheta]
                    while not cAdded[c]:
                        citheta += 1
                        citheta = (citheta % (customerCount-1))
                        c = ciThetaSorted[citheta]
                    while cAdded[c]:
                        citheta += 1
                        citheta = (citheta % (customerCount-1))
                        c = ciThetaSorted[citheta]
 
            vContainer.append(c)
            cAdded[c] = True
            capRemain -= customers[c][0]
            ciCounter = 1
            while leftpass or rightpass:  
                if cAdded.count(False) == 0:
                    running = False
                    break   
                if leftpass:
                    ci = ciThetaSorted[citheta-ciCounter]
                    if cAdded[ci] == False and capRemain >= customers[ci][0]:
                        #print 'left add ' + str(ci)
                        vContainer.append(ci)
                        capRemain -= customers[ci][0]
                        cAdded[ci] = True
                        if cAdded.count(False) == 0:
                            running = False
                            break
                    else:
                        leftpass = False
                if rightpass:
                    ciinsort = (citheta+ciCounter) % len(ciSizeSorted)
                    ci = ciThetaSorted[ciinsort]
                    if cAdded[ci] == False and capRemain >= customers[ci][0]:
                        #print 'right add ' + str(ci)
                        vContainer.append(ci)
                        capRemain -= customers[ci][0]
                        cAdded[ci] = True
                        if cAdded.count(False) == 0:
                            running = False
                            break
                    else:
                        rightpass = False
                ciCounter += 1
            vContainers.append(vContainer)
            capRemains.append(capRemain)
            if DEBUG: print 'vehicle ' +str(v) + ' remaining capacity ' + str(capRemain)
            
        allUnplaced = [idx for idx in range(0, customerCount) if not cAdded[idx]]
        if DEBUG :
            pprint(vContainers)
            print 'remaining customers ' + ','.join(map(str, allUnplaced))
            print 'capacities are ' + ','. join(map(str, [ customers[c][0] for c in range(1, customerCount) if cAdded[c] == False]))
            print 'total unplaced capacity' + str(sum([ customers[c][0] for c in range(1, customerCount) if cAdded[c] == False]))

        # TODO: this created extra vehicles.
        
        
        if ( NeighbourWatch ) :
            neighbourTried = dict()
            while (cAdded.count(False) != 0 ):
                if vioCap(vContainers, customers, vehicleCapacity):
                    print '!!!caonima vioCap'
                    return
                print 'total unplaced capacity' + str(sum([ customers[c][0] for c in range(1, customerCount) if cAdded[c] == False]))
                unplaced = int(cAdded.index(False))
                ciinsort = ciThetaSorted.index(unplaced)
                print 'unplaced %d ciinsort %d' % ( unplaced, ciinsort)
                ciright = ciinsort
                target = unplaced
                while not cAdded[target]:
                    ciright += 1
                    ciright = (ciright % (customerCount-1))
                    target = ciThetaSorted[ciright]
                rtarget = target
                
                cileft = ciinsort
                target = ciThetaSorted[cileft]
                while not cAdded[target]:
                    cileft -= 1
                    if cileft == -1: cileft = (customerCount-2)
                    target = ciThetaSorted[cileft]
                ltarget = target
                                
                vlTarget = None
                vrTarget = None
                for v, vContainer in enumerate(vContainers):
                    if ltarget in vContainer:
                        vlTarget = v
                    if rtarget in vContainer:
                        vrTarget = v
                
                if ( vlTarget == vrTarget ):
                    vrTarget += 1 
                    vrTarget = vrTarget % vehicleCount
    
                # try to insert directly
                if capRemains[vlTarget] >= customers[unplaced][0]:
                    vContainers[vlTarget].append(unplaced)
                    cAdded[unplaced] = True
                    capRemains[vlTarget] -= customers[unplaced][0]
                    continue
                elif capRemains[vrTarget] >= customers[unplaced][0]:
                    vContainers[vrTarget].append(unplaced)
                    cAdded[unplaced] = True
                    capRemains[vrTarget] -= customers[unplaced][0]
                    continue
                 
                # have to swap
                # find the smallest item that allow swap
                minCustomer = None
                minV = None
                counter = 0
                while minV == None:
                    counter += 1
                    if counter == 10: 
                        pprint(vContainers)
                        return
                    for c in vContainers[vlTarget]:
                        if ( capRemains[vlTarget] + customers[c][0] >= customers[unplaced][0] ):
                            if ( minCustomer == None or customers[c][0] < customers[minCustomer][0] ):
                                key = genKey(unplaced, c)
                                if key in neighbourTried:
                                    print 'key collide' + str(key)
                                    continue
                                minCustomer = c
                                minV = vlTarget
                    for c in vContainers[vrTarget]:
                        if ( capRemains[vrTarget] + customers[c][0] >= customers[unplaced][0] ):
                            if ( minCustomer == None or customers[c][0] < customers[minCustomer][0] ):
                                key = genKey(unplaced, c)
                                if key in neighbourTried:
                                    print 'key collide' + str(key)
                                    continue
                                minCustomer = c
                                minV = vrTarget
                    vlTarget -= 1
                    if vlTarget == 0: vlTarget = vehicleCount-1
                    vrTarget += 1
                    vrTarget = vrTarget % vehicleCount
                    
                if ( minV == None ):
                    print 'no solution, you SOB'
                    pprint(vContainers)
                    return
                else:
                    print 'find customer %d cap %d in vehicle %d to swap unplaced %d' % ( minCustomer, customers[minCustomer][0], minV, unplaced)
                    
                key = genKey(unplaced, minCustomer)
                if key in neighbourTried:
                    print 'bullshit, key already tried'
                    pprint(vContainers)
                    return
                neighbourTried[key] = 1
                
                removeCustomer(minCustomer, minV, capRemains, vContainers, cAdded, customers)
                addCustomer(unplaced, minV, capRemains, vContainers, cAdded, customers)
                #pprint(vContainers)
                #return
            pass
        
        if ( Shelter ):
            placed = []
        while (cAdded.count(False) != 0):
            unplaced = int(cAdded.index(False))
            ciinsort = ciThetaSorted.index(unplaced)
            #try place first
            # for v, cap in enumerate(capRemains):
                # if ( cap >= customers[unplaced][0] ):
                    # vContainers[v].append(unplaced)
                    # cAdded[unplaced] = True
                    # break
            counter = 1
            foundSwap = False
            #try swap
            while not cAdded[unplaced]:
                if ( ciinsort + counter > customerCount-2 ):
                    ciinsort = (ciinsort+counter) % (customerCount-1) - counter
                target = ciThetaSorted[ciinsort+counter]
                if cAdded[target] == True and target != 0 and target not in placed:
                    vTarget = None
                    for v, vContainer in enumerate(vContainers):
                        if target in vContainer:
                            vTarget = v
                            break
                    if vTarget != None:
                        if capRemains[vTarget] >= customers[unplaced][0]:
                            vContainers[vTarget].append(unplaced)
                            cAdded[unplaced] = True
                            capRemains[vTarget] -= customers[unplaced][0]
                            continue #equal to break
                        elif capRemains[vTarget] + customers[target][0] - customers[unplaced][0] >= 0:
                            vContainers[vTarget].pop(vContainers[vTarget].index(target))
                            cAdded[target] = False
                            vContainers[vTarget].append(unplaced)
                            cAdded[unplaced] = True
                            capRemains[vTarget] += (customers[target][0] - customers[unplaced][0])
                            if DEBUG: print 'swapped out %d, in %d' %(target, unplaced)
                            continue #equal to break
                #else
                if counter < 0:
                    counter = counter*-1 +1
                else:
                    counter = counter * -1
            placed.append(unplaced)
                
        if DEBUG:
            pprint(vContainers)
        counter = -1
        for vh in vContainers:
            caps = 0
            counter += 1
            for c in vh:
                caps += customers[c][0]
            if ( caps > vehicleCapacity ):
                print 'vehicle cap violation at '+ str(counter)
                pprint(capRemains)
                return
    
    if ( False ):
        minsize = min([d[0] for d in customers[1:]])
        pyplot.scatter([d[1] for d in customers], [d[2] for d in customers], s=[d[0]/minsize*20 for d in customers])
        pyplot.scatter(customers[0][1], customers[0][2], c='r')
        for vh in vContainers:
            cithetaIdx = [ciThetaSorted.index(d) for d in vh]
            ciextent = [min(cithetaIdx), max(cithetaIdx)]
            pyplot.plot([customers[0][1], customers[ciextent[0]+1][1]], [customers[0][2], customers[ciextent[0]+1][2]])
            pyplot.plot([customers[0][1], customers[ciextent[1]+1][1]], [customers[0][2], customers[ciextent[1]+1][2]])
        pyplot.show()
        
    # solve route
    if TSP:
        if DEBUG:
            print ' TSP starts ' 
        vehicleTours = [[]]* len(vContainers)
        for v in range(0, len(vContainers)):
            if DEBUG:
                print 'solving container ' + str(v) 
            vContainer = vContainers[v]
            vCustomer = [customers[c] for c in vContainer]
            vCustomer.append(customers[0])
            vehicleTours[v] = tsp(vCustomer)
            if DEBUG:
                print 'solution is '
                pprint(vehicleTours[v])
    if ( DEBUG ):
        minsize = min([d[0] for d in customers[1:]])
        pyplot.scatter([d[1] for d in customers], [d[2] for d in customers], s=[d[0]/minsize*20 for d in customers])
        pyplot.scatter(customers[0][1], customers[0][2], c='r')
        for vCustomer in vehicleTours:
            pyplot.plot([customers[c][1] for c in vCustomer], [customers[c][2] for c in vCustomer])
        pyplot.show()

        
    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicleCount):
        vehicleTour = vehicleTours[v]
        if len(vehicleTour) > 0:
            obj += length(customers[depotIndex],customers[vehicleTour[0]])
            for i in range(0, len(vehicleTour) - 1):
                obj += length(customers[vehicleTour[i]],customers[vehicleTour[i + 1]])
            obj += length(customers[vehicleTour[-1]],customers[depotIndex])

    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
    for v in range(0, vehicleCount):
        outputData += str(depotIndex) + ' ' + ' '.join(map(str,vehicleTours[v])) + ' ' + str(depotIndex) + '\n'

    return outputData

def tsptest():
    points = [[0,30.0,40.0,1],
        [19, 42.0 ,41.0,2],
        [29, 31.0, 32.0,0],
        [23, 5.0, 25.0,4]]
    #points = [[d[1], d[2]] for d in points]
    #pprint(points)
    tsp(points)
    
def vioCap(vContainers, customers, vehicleCapacity):
    counter = -1
    for vh in vContainers:
        caps = 0
        counter += 1
        for c in vh:
            caps += customers[c][0]
        if ( caps > vehicleCapacity ):
            print 'vehicle cap violation at '+ str(counter)
            pprint(capRemains)
            return True
    return False
                
def removeCustomer(c, v, capRemains, vContainers, cAdded, customers):
    size = customers[c][0]
    vContainers[v].pop(vContainers[v].index(c))
    capRemains[v] += size
    cAdded[c] = False
    
def addCustomer(c, v, capRemains, vContainers, cAdded, customers):
    size = customers[c][0]
    vContainers[v].append(c)
    capRemains[v] -= size
    cAdded[c] = True    
    
def genKey(a, b):
    keyarray = sorted([a, b])
    key = ','.join(map(str, keyarray))
    return key
                
def tsp(points):
    #pprint(points)
    nodeCount = len(points)
    solution = [None] * nodeCount
    used = bitarray(nodeCount)
    used.setall(False)
    paling = random.randint(0, nodeCount-1)
    prev = paling
    solution[0] = paling
    used[paling] = True
    for i in range(1, nodeCount):
        while used[paling] == True:
                paling = random.randint(0, nodeCount-1)       
        solution[i] = paling
        used[paling] = True
    # got a good initial solution
    bestLength = solLength(solution, points)
    maxLength = bestLength
    
    nodetags = [None] * nodeCount
    for i in range(0, nodeCount-1):
        current = solution[i]
        nodetags[current] = solution[i+1]
    nodetags[solution[-1]] = solution[0]
        
    if nodeCount > 3:
        running = True
    else:
        running = False
    doubleoptStart = time.time()
    global DEBUG
    if DEBUG: 
        durationmin = 0.1
    else: 
        durationmin = 2
    doubleoptStop = int(doubleoptStart)+ durationmin * 60
    
    uselesspass = 0
    counter = 0
    usefultracker = []
    initqueue = range(0, nodeCount)
    numKicks = 0
    temp = getTemperature()
    initlen = 0
    bestNodetags = tuple(nodetags)
    kickratio = 5
    while (running):
        counter += 1
        #volunteer = random.randint(0, nodeCount-1)
        # optimize with neighbours
        #if ( counter % (nodeCount*100) == 0 ):
        if ( initlen == 0 ):
            #print 'reshuffling'
            initlen = nodeCount
        if ( initlen > 0 ) :
            if (initlen == nodeCount) :
                random.shuffle(initqueue)
            volunteer = initqueue[nodeCount - initlen]
            initlen -= 1

        randoming = True
        while ( randoming ):
            volunteertwo = random.randint(0, nodeCount-1)
            if ( volunteertwo != nodetags[volunteer] ) and (volunteertwo != volunteer) and ( nodetags[volunteertwo] != volunteer):
                randoming = False
        workspace = [volunteer, nodetags[volunteer], volunteertwo, nodetags[volunteertwo]]
        lengths = []
        lengths.append(length(points[workspace[0]], points[workspace[1]]) + length(points[workspace[2]], points[workspace[3]]))
        lengths.append(length(points[workspace[0]], points[workspace[2]]) + length(points[workspace[1]], points[workspace[3]]))
        temp = getTemperature(temp)
        if ( temp <= 0 ) :
            break
            
        #print 'temperature ' + str(temp) + ' annealing prob ' + str(annealingProb( lengths[0], lengths[1] , temp )) + ' length orig ' + str(lengths[0]) + ' testing ' + str(lengths[1])
        #time.sleep(1)
        if annealingProb( lengths[0], lengths[1] , temp ) < random.random():
            # original is the smallest
            #print 'not optimizing'
            
            # uselesspass +=1
            # if ( uselesspass > nodeCount * kickratio):
                # temp = getTemperature() * (0.8**numKicks)
                # numKicks += 1
                # kickratio = int(kickratio * 1.2)
                # uselesspass = 0
                # if numKicks == 30:
                    # running = False
            pass        
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
                if maxLength <= bestLength:
                    bestNodetags = list(nodetags)
                    bestLength = maxLength

            #print 'optimized ' + str(lengths[0] - lengths[1]) + ' to ' + str(maxLength)
        if ( time.time() > doubleoptStop ):
            #print 'elapsed time ' + str(time.time() - doubleoptStart)
            running = False

    solution = [None]* nodeCount
    current = 0
    for i in range(0, nodeCount):
        current = bestNodetags[current]
        solution[i] = current
    if ( False ):
        pyplot.scatter([p[1] for p in points], [p[2] for p in points])
        pyplot.plot([points[sol][1] for sol in solution], [points[sol][2] for sol in solution])
        pyplot.show()
    
    idxSolution = [points[s][3] for s in solution]
    zeroidx = idxSolution.index(0)
    idxSolution = idxSolution[zeroidx+1:] + idxSolution[:zeroidx]
    return idxSolution
    
def solLength(solution, points):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, len(solution)-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def annealingProb(length0, length1, temp):
    if length1 < length0 :
        return 1
    else:
        return math.exp( -1*(length1-length0)/temp) # falls off at half way
        
def getTemperature(temp=3000):
    alpha = 0.99
    # alpha^n 30 sec stable
    # t - n*alpha is not usable, too much error to begin with
    # alpha / log(t) too much trouble, negative hits too easily
    return temp*alpha
    
def arctantest():
    xs = np.array([1, -1, -1, 1])
    ys = np.array([1,1,-1,-1])
    thetas = np.arctan2(ys, xs)
    pprint(thetas)
    pprint(np.power(ys,2))

import sys
from matplotlib import pyplot
from pprint import pprint
import numpy as np
from bitarray import bitarray
import time
import random

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        #print 'Solving:', fileLocation
        print solveIt(inputData)
        #print tsptest()
    else:

        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)'

