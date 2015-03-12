#!/usr/bin/python
# -*- coding: utf-8 -*-


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = [0]*nodeCount
    nodes = [Node(_) for _ in range(nodeCount)]

    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()
        nodes[int(parts[0])].addEdge(nodes[int(parts[1])])
        nodes[int(parts[1])].addEdge(nodes[int(parts[0])])
        edges[int(parts[0])] += 1
        edges[int(parts[1])] += 1
    
    #nodeprints(nodes)
    edgeIdx = range(0, nodeCount)
    edgesTracker = sorted(zip(edgeIdx, edges), key=lambda edge: edge[1], reverse=True)
    # list of tuple of (nodename, number of edges)

    # try the welsh-powell algorithm
    # i will have to implement two more to solve this, hopefully 
    colorNow = 0
    nodecounter = 0
    while ( len(edgesTracker) != 0 ):
        #print 'coloring now '+ str(colorNow)
        # color the first one with 0
        neighbours = set()
        popList = []
        for item in range(0, len(edgesTracker)):
            nodename = edgesTracker[item][0]
            if nodename not in neighbours:
                # pop it out of list
                popList.append(item)
                node = nodes[nodename]
                node.color = colorNow
                # skip to the next one that is not connected to first one
                neighbours.update(node.getEdges())
        colorNow += 1
        popList.reverse()
        for idx in popList:
            edgesTracker.pop(idx)
        # edgesTracker automatically updated
        #edgesTracker = list(eTcopy)
            
        # color it 0 and pop it out
        # repeat until counter is at the end of list
        # start from beginning with the first item in edgesTracker now.

            
    
    solution = [n.color for n in nodes]
    # prepare the solution in the specified output format
    outputData = str(nodeCount) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))
    #outputData += "\n"+ 'colorCount ' + str(colorNow) + ' actual color count '+ str(len(set(solution)))


    return outputData

def nodeprints(nodes):
    for node in nodes:
        print "Node: " + str(node.name) + " color: " + str(node.color);
        print ' '.join(map(str, node.getEdges()))

class Node:
    def __init__(self,nodename):
        self.edges = []
        self.color = None
        self.name = nodename
       
    def addEdge(self, node):
        self.edges.append(node)
     
    def hasConflict(self):
        for node in self.edges:
            if (node.color == None) or (self.color == None) or (node.color == self.color):
                return True
        return False
    
    def resolveColor(self):
        edgeColors = []
        for node in self.edges:
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
    
    def getEdges(self):
        return [e.name for e in self.edges]
    
    def resolveConflict(self, colorNow):
        edgeColors = set()
        selfclean = True
        neighbourclean = True
        for node in self.edges:
            color = node.color
            if (color == None):
                neighbourclean = False
            else:
                edgeColors.add(color)
        #pprint(edgeColors)
        '''
        if ( self.color != None ) and (neighbourclean == True) and not ( self.color in edgeColors ) :
            #print 'node '+str(self.name) + ' is clean with color ' + str(self.color)
            return True
        '''
        allColors = frozenset(range(0, colorNow))
        #pprint(allColors)
        possibleColors = allColors.difference(edgeColors)
        #pprint(possibleColors)
        if ( len(possibleColors) > 0 ) :
            minColor = min(possibleColors)
            if ( self.color != minColor ) :
                self.color = minColor
            selfclean = True
        else :
            self.color = colorNow
            selfclean = False
        return (selfclean and neighbourclean)
        
import sys
from pprint import pprint
import cProfile
import time

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        #cProfile.run('print solveIt(inputData)')
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

