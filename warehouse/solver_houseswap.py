#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    Bighole = False 
    Customerfirst = False # select lowest cost warehouse for all customers, failed
    Simplerank = True # good first guess
    Rankpeek = False
    Houseswap = True 
    Streetclean = True
    
    Logger = True
    startts = time.time()
    
    
    # parse the input
    lines = inputData.split('\n')

    parts = lines[0].split()
    warehouseCount = int(parts[0])
    customerCount = int(parts[1])

    warehouses = []
    for i in range(1, warehouseCount+1):
        line = lines[i]
        parts = line.split()
        warehouses.append((int(parts[0]), float(parts[1])))

    customerSizes = []
    customerCosts = []
    cCostsSorted = []

    lineIndex = warehouseCount+1
    for i in range(0, customerCount):
        customerSize = int(lines[lineIndex+2*i])
        customerCost = map(float, lines[lineIndex+2*i+1].split())
        customerSizes.append(customerSize)
        customerCosts.append(customerCost)
        sortedCosts = sorted( enumerate(customerCost), key = lambda item:item[1] )
        sortedCosts = [d[0] for d in sortedCosts]
        cCostsSorted.append(sortedCosts)
    minCsize = min(customerSizes)
    if Rankpeek:
        whRank = [0] * warehouseCount
        for c in range(0, customerCount):
            for k in range(0, 5):
                wh = cCostsSorted[c][k][0]
                whRank[wh] += 1
                
        whRank = sorted(whRank)
        print ", ".join(map(str,whRank))
        return

    if Customerfirst:
        whCustomers = [[] for x in xrange(warehouseCount)] 
        whUsed = bitarray(warehouseCount)
        whUsed.setall(False)
        capRemain = [w[0] for w in warehouses]
        solution = [-1] * customerCount
        initCost = 0
        for c in range(0, customerCount):
            #open the lowest cost warehouse for that customer
            for idx in range(0, warehouseCount+1):
                if ( idx == warehouseCount ) :
                    # overflow, not feasible
                    print 'no warehouse will fit this customer ' + str(idx) + ' size ' + str(customerSizes[c])
                    
                    pprint(capRemain)
                    exit()
                if capRemain[cCostsSorted[c][idx][0]] >= customerSizes[c]:
                    wh = cCostsSorted[c][idx][0]
                    break
            addCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes)
            solution[c] = wh
            initCost += cCostsSorted[c][0][1]
            
        for w in range(0, warehouseCount):
            if (whUsed[w]):
                initCost += warehouses[w][1]
               
        print 'initCost is ' + str(initCost)
        bestSolution = solution[:]
        bestCost = initCost
    
    if Bighole:
        running = True
        while ( running ):
            holeCostsNorm = [0]*warehouseCount
            for w in range(0, warehouseCount):
                if ( whUsed[w] ) :
                    wCap = capRemain[w]
                    holeCostsNorm[w] = warehouses[w][1] / wCap if (wCap != 0) else 0
                # 0 means don't optimize
                # full warehouse are not touched right now
            pprint(holeCostsNorm)
            maxHoleC = max(holeCostsNorm)
            maxHoleId = holeCostsNorm.index(maxHoleC)
            print 'most expensive hole costs ' + str(maxHoleC) + ' at ' + str(maxHoleId)
            # close down HoleId
            whUsed[maxHoleId] = False
            capRemain[maxHoleId] = warehouses[maxHoleId][1]
            pprint(whCustomers[maxHoleId])
            changed = False
            for c in whCustomers[maxHoleId]:
                for i in range(0, warehouseCount+1):
                    if ( i == warehouseCount ):
                        # overflow
                        #running = False
                        break
                    wh = cCostsSorted[c][i][0]
                    if ( whUsed[wh] == True and capRemain[wh] >= customerSizes[c] ):
                        addCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes)
                        whCustomers[maxHoleId].pop(whCustomers[maxHoleId].index(c))
                        changed = True
                        break
            if not changed:
                print 'this round nothing changed'
                pprint(whCustomers)
                running = False
            else:
                cost, solution = solutionResult(whCustomers, warehouses, customerCosts)
                if (cost < bestCost):
                    bestSolution = solution
        obj = bestCost
        solution = bestSolution
    
    if Simplerank:
        whPrice = [ wh[1]/wh[0] for wh in warehouses] 
        whPricerank = sorted(enumerate(whPrice), key = lambda item: item[1] )
        cSizesorted = sorted(enumerate(customerSizes), key = lambda item: item[1], reverse=True )
        whCustomers = [[] for x in xrange(warehouseCount)] 
        whUsed = bitarray(warehouseCount)
        whUsed.setall(False)
        capRemain = [w[0] for w in warehouses]
        solution = [-1] * customerCount
        customerPlaced = 0
        for whtemp in whPricerank:
            if customerPlaced == customerCount:
                break
            wh = whtemp[0]
            for ctemp in cSizesorted:
                c = ctemp[0]
                if ( solution[c] != -1 ):
                    continue
                size = ctemp[1]
                for i in range(0,5):
                    if (cCostsSorted[c][i] == wh and size <= capRemain[wh]):
                        addCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes)
                        solution[c] = wh
                        customerPlaced += 1
                        break
                if capRemain[wh] < cSizesorted[-1][1] :
                    break

                   
        obj = sum([warehouses[x][1]*whUsed[x] for x in range(0,warehouseCount)])
        for c in range(0, customerCount):
            obj += customerCosts[c][solution[c]]
        bestSolution = tuple(solution)
        bestCost = obj
        
    if ( Logger ) :
        fh = open('calculation.csv', 'w')
        fh.write("time,cost, warehousecount\n")
        fh.write(str(time.time() - startts)+','+str(bestCost)+ ',' + str(whUsed.count(True))"\n")
        
    if Houseswap:    
        whTracker = []
        whTracker.append(bitarray(whUsed))
        
        whRank = [0] * warehouseCount
        for c in range(0, customerCount):
            for k in range(0, 5):
                wh = cCostsSorted[c][k]
                whRank[wh] += 1
        whRanksorted = sorted(enumerate(whRank), key= lambda item: item[1], reverse = True)
        whRanksorted = [ d[0] for d in whRanksorted ]
        
        operation = 'open'
        prevCost = bestCost
        
        while True:
            #print 'operation is ' + str(operation)
            if ( operation == 'open' ):
                #do open step
                for i in range(0, warehouseCount+1):
                    if ( i == warehouseCount ):
                        #print 'pattern exhausted tested ' + str(len(whTracker));
                        operation = 'close';
                        break
                    wh = whRanksorted[i]
                    if not whUsed[wh]:
                        whUsed[wh] = True
                        if compareUsed(whTracker, whUsed):
                            #print 'pattern has been tested before'
                            whUsed[wh] = False
                        else:
                            break
                if (operation != 'open' ):
                    continue
                print 'opening warehouse ' + str(wh)
                cImprove = [0] * customerCount             
                for c in range(0, customerCount):
                    whzero = solution[c]
                    cImprove[c] = customerCosts[c][whzero] - customerCosts[c][wh]
                cImprovesorted = sorted(enumerate(cImprove), key = lambda item: item[1], reverse = True)
                
                for c, imp in cImprovesorted:
                    if imp <= 0 :
                        break
                    if customerSizes[c] <= capRemain[wh]:
                        whzero = solution[c]
                        removeCustomersol(whzero, c, solution, whUsed, capRemain, customerSizes)
                        addCustomersol(wh, c, solution, whUsed, capRemain, customerSizes)
                        if capRemain[wh] < minCsize:
                            break
                            
                cost = solutionCost(solution, whUsed, customerCosts, warehouses)
                
                pass
            elif( operation == 'close'):
                # TODO stop step
                # pick the normalized most expensive warehouse
                whCostsNorm = [0] * warehouseCount
                for c, wh in enumerate(solution):
                    whCostsNorm[wh] += customerCosts[c][wh]
                for wh in range(0, warehouseCount):
                    whCostsNorm[wh] += warehouses[wh][1] * whUsed[wh]
                    if warehouses[wh][0] != capRemain[wh]:
                        whCostsNorm[wh] = whCostsNorm[wh] / (warehouses[wh][0] - capRemain[wh])
                whClosing = whCostsNorm.index(max(whCostsNorm))
                
                whUsed[whClosing] = False
                capRemain[whClosing] = warehouses[wh][0]
                cQueue = getCustomers(solution, whClosing)
                for c in cQueue:
                    solution[c] = None
                
                while (len(cQueue) > 0):
                    #print 'cQueue size is ' + str(len(cQueue))
                    whTarget = random.randint(0, warehouseCount - 1)
                    if ( whUsed[whTarget] == False ):
                        continue
                    # else
                    cQueue = cQueue + getCustomers(solution, whTarget)
                    # out of all the opened warehouses, how many have a lower rank than the current one
                    cQueueImprovements = [0] * len(cQueue)
                    for idx, c in enumerate(cQueue):
                        for ele in cCostsSorted:
                            if ( ele[0] == whTarget ):
                                break
                            if ( whUsed[ele[0]] == True ):
                                cQueueImprovements[idx] += 1
                                
                    for c in cQueue:
                        solution[c] = None
                    capRemain[whTarget] = warehouses[whTarget][0]
                    
                    # take the customer with lowest chance of improvement, namely least number of better warehouses open
                    # try not filling this up first, see if there is a solution
                    # leaving empty warehouses make the program stuck
                    # try better
                    if Streetclean:
                        cPlaced = []
                        cQImprovsorted = sorted(enumerate(cQueueImprovements), key = lambda item:item[1])
                        for ele in cQImprovsorted:
                            c = cQueue[ele[0]]
                            if ( customerSizes[c] < capRemain[whTarget] ):
                                addCustomersol(whTarget, c, solution, whUsed, capRemain, customerSizes)
                                cPlaced.append(c)
                            else:
                                # skip this item
                                pass
                        for c in cPlaced:
                            cQueue.pop(cQueue.index(c))
                    else:      
                        while False:
                            if len(cQueue) == 0:
                                break
                            cidx = cQueueImprovements.index(min(cQueueImprovements))
                            c = cQueue[cidx]
                            if ( customerSizes[c] <= capRemain[whTarget] ):
                                addCustomersol(whTarget, c, solution, whUsed, capRemain, customerSizes)
                                cQueue.pop(cidx)
                                cQueueImprovements.pop(cidx)
                            
                            else:
                                break
                
                print 'solution is found after closing ' + str(whClosing)
                cost = solutionCost(solution, whUsed, customerCosts, warehouses)
               
                    
                
            else:
                break
            
            whTracker.append(bitarray(whUsed))
            print 'current cost is ' + str(cost) + ' best ' + str(bestCost)
            
            if ( cost < bestCost ) :
                bestCost = cost
                bestSolution = tuple(solution)
                #exit()
            if ( cost < prevCost):
                pass
            else:
                if ( operation == 'open'):
                    operation = 'close'
                elif( operation == 'close' ):
                    operation = 'open'
            prevCost = cost
        
        obj = bestCost
        solution = bestSolution
    # build a trivial solution
    # pack the warehouses one by one until all the customers are served
    '''
    capacityRemaining = [w[0] for w in warehouses]
    warehouseIndex = 0
    for c in range(0, customerCount):
        if capacityRemaining[warehouseIndex] >= customerSizes[c]:
            solution[c] = warehouseIndex
            capacityRemaining[warehouseIndex] -= customerSizes[c]
        else:
            warehouseIndex += 1
            assert capacityRemaining[warehouseIndex] >= customerSizes[c]
            solution[c] = warehouseIndex
            capacityRemaining[warehouseIndex] -= customerSizes[c]
    used = [0]*warehouseCount
    for wa in solution:
        used[wa] = 1
        used = whUsed
    # calculate the cost of the solution
    obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
    for c in range(0, customerCount):
        obj += customerCosts[c][solution[c]]
    '''


    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData

class WarehouseCustomers:
    def __init__(self):
        self.customerSizes = []
        
def getCustomers(solution, wh):
    customers = []
    for i in range(0, len(solution)):
        if solution[i] == wh:
            customers.append(i)
    return customers
    
def compareUsed(whTracker, pattern):
    for heystack in whTracker:
        if heystack == pattern:
            return True
    return False
    
def addCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes):
    whCustomers[wh].append(c)
    whUsed[wh] = True
    capRemain[wh] -= customerSizes[c]

def addCustomersol(wh, c, solution, whUsed, capRemain, customerSizes):
    solution[c] = wh
    whUsed[wh] = True
    capRemain[wh] -= customerSizes[c]
    
def removeCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes):
    whCustomers[wh].pop(whCustomers[wh].index(c))
    if len(whCustomers[wh]) == 0 :
        whUsed[wh] = False
    capRemain[wh] += customerSizes[c]

def removeCustomersol(wh, c, solution, whUsed, capRemain, customerSizes):
    solution[c] = None
    try:
        found = solution.index(wh)
    except ValueError:
        found = -1
    if found == -1:
        whUsed[wh] = False
    capRemain[wh] += customerSizes[c]
    
def solutionResult(whCustomers, warehouses, customerCosts):
    warehouseCount = len(warehouses)
    customerCount = len(customerCosts)
    solution = [-1] * customerCount
    used = bitarray(warehouseCount)
    used.setall(False)
    for wh in range(0, warehouseCount):
        for c in whCustomers[wh]:
            solution[c] = wh
            used[wh] = True
            

    # calculate the cost of the solution
    obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
    for c in range(0, customerCount):
        obj += customerCosts[c][solution[c]]
        
    return obj, solution
    
def solutionCost(solution, whUsed, customerCosts, warehouses):
    customerCount = len(solution)
    warehouseCount = len(whUsed)
    obj = sum([warehouses[x][1]*whUsed[x] for x in range(0,warehouseCount)])
    for c in range(0, customerCount):
        obj += customerCosts[c][solution[c]]
        
    return obj
        
import sys
from bitarray import bitarray
from pprint import pprint
import random

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        #print 'Solving:', fileLocation
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/wl_16_1)'

