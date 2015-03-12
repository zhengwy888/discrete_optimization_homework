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

    value = 0
    weight = 0
    total_weight = 0
    #tracker = Matrix(capacity, items)
    tracker = []
    pcolumn = [0]*capacity

    # i is column(item), k is row(capacity)
    for item in range(0,items):
        column = [0]*capacity
        capkey = []
        total_weight += weights[item]
        for cap in range(0,capacity):
            rowCap = cap+1
            if ( rowCap > total_weight ):
                column[cap:-1] = [column[cap-1]]*(capacity-cap)
                break
            # first column
            if (weights[item] <= rowCap):
                #tracker[k][i] = values[i]
                column[cap] = values[item]
            if ( item != 0 ):
                # subsequent columns
                previous_cap = rowCap - weights[item] - 1
                if ( previous_cap < 0):
                    #current weight doesn't fit at all
                    #print 'item ' + str(item-1) + ' cap ' + str(cap)
                    #column[cap] = max(tracker[item-1][cap], column[cap])
                    column[cap] = max(pcolumn[cap], column[cap])
                else:
                    valueCurrent = pcolumn[previous_cap] + values[item]
                    #valuePrevious = tracker[k][i-1]
                    valuePrevious = pcolumn[cap]
                    column[cap] = max(valueCurrent, valuePrevious)
            if (pcolumn[cap] != column[cap] ):
                capkey.append(cap)
        #tracker.append(tuple(column))
        tracker.append(tuple(capkey))
        pcolumn = tuple(column)

    #pprint(tracker)
    taken = []
    room_left = capacity - 1
    
    for i2 in range(0, items):
        i = (items-1) - i2
        if (room_left < 0) or not inTuple(room_left, tracker[i]) :
            taken.insert(0, 0)        
        else:
            taken.insert(0, 1)
            value += values[i]
            weight += weights[i]
            room_left -= weights[i]            

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

def inTuple(needle, haystack):
    return (needle in haystack)
    
def Matrix(row, column):
    return [[0 for x in xrange(column)] for x in xrange(row)]
    
import sys
from pprint import pprint
import cProfile

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        #cProfile.run('solveIt(inputData)')
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

