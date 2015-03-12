#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    Bighole = False
    Customerfirst = False # select lowest cost warehouse for all customers, failed
    Simplerank = True
    Rankpeek = False
    Houseswap = True
    
    
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
        cCostsSorted.append(sortedCosts)
     
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
                    if (cCostsSorted[c][i][0] == wh and size <= capRemain[wh]):
                        addCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes)
                        solution[c] = wh
                        customerPlaced += 1
                        break
                if capRemain[wh] < cSizesorted[-1][1] :
                    break

                   
        obj = sum([warehouses[x][1]*whUsed[x] for x in range(0,warehouseCount)])
        for c in range(0, customerCount):
            obj += customerCosts[c][solution[c]]
            
    if Houseswap:    
        bestSolution = tuple(solution)
        bestCost = obj
        whTracker = []
        whTracker.append(whUsed)
        
        operation = 'open'
        
        while True:
            if ( operation == 'open' ):
                #do open step
                pass
            elif( operation == 'close'):
                # do stop step
            else:
                break
                
        
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
        
        
def addCustomer(wh, c, whCustomers, whUsed, capRemain, customerSizes):
    whCustomers[wh].append(c)
    whUsed[wh] = True
    capRemain[wh] -= customerSizes[c]

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
        
import sys
from bitarray import bitarray
from pprint import pprint

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

