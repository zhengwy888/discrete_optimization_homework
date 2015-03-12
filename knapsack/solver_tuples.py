#!/usr/bin/python
# -*- coding: utf-8 -*-


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    #tracker = Matrix(capacity, items)
    tracker = []

    # i is column(item), k is row(capacity)
    for item in range(0,items):
        column = [0]*capacity
        for cap in range(0,capacity):
            rowCap = cap+1
            # first column
            if (weights[item] <= rowCap):
                #tracker[k][i] = values[i]
                column[cap] = values[item]
            if ( item == 0 ):
                continue
            # subsequent columns
            previous_cap = rowCap - weights[item] - 1
            if ( previous_cap < 0):
                #current weight doesn't fit at all
                #print 'item ' + str(item-1) + ' cap ' + str(cap)
                column[cap] = max(tracker[item-1][cap], column[cap])
            else:
                valueCurrent = tracker[item-1][previous_cap] + values[item]
                #valuePrevious = tracker[k][i-1]
                valuePrevious = tracker[item-1][cap]
                column[cap] = max(valueCurrent, valuePrevious)
                
        tracker.append(tuple(column))
            
    taken = []
    taken_reversed = []
    room_left = capacity - 1
    
    for i2 in range(0, items):
        i = (items-1) - i2
        if (room_left < 0) or (tracker[i][room_left] == tracker[i-1][room_left]) :
            taken_reversed.append(0)           
        else:
            taken_reversed.append(1)
            value += values[i]
            weight += weights[i]
            room_left -= weights[i]            
    
    taken = taken_reversed[::-1]

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

def Matrix(row, column):
    return [[0 for x in xrange(column)] for x in xrange(row)]
    
import sys
from pprint import pprint

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

