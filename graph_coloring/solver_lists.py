#!/usr/bin/python
# -*- coding: utf-8 -*-


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []
    colors = [None]*nodeCount;
    linkers = [[]]*nodeCount;
    colorCount = 0;
    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        addLink(linkers, parts)
        

    # build a trivial solution
    # every node has its own color
    solution = range(0, nodeCount)

    # prepare the solution in the specified output format
    outputData = str(nodeCount) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData

class Node:
    nodeCount = 0
    colorCount = 0
    def __init__(self):
        self.edges = []
        self.color = None
        self.name = nodeCount
        Node.nodeCount += 1
       
    def addEdge(self, node):
        if not (name in self.edges):
            self.edges.append(node)
     
    def hasConflict(self):
        for (node in self.edges):
            if node.color == self.color:
                return True
        return False
    
    def resolveColor(self):
        edgeColors = []
        for ( node in self.edges):
            color = node.color
            if (not ( color in edgeColors )) and (color != None):
                edgeColors.append(node.color)
        allColors = range(0, Node.colorCount)
        possibleColors = allColors.difference(edgeColors)
        if ( len(possibleColors) ) :
            self.color = min(possibleColors)
        else :
            self.color = Node.colorCount
            Node.colorCount += 1
        return self.color
            
def addLink(linkers, parts):
    one = int(parts[0])
    two = int(parts[1])
    linkers[one].append(two)
    linkers[two].append(one)

def hasConflict(linkers, colors, item):
    return True
    
def minColor(linkers, colors, item):
    return 0
    

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

