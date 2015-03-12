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
    nodes = [Node() for _ in range(nodeCount)];

    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()
        nodes[int(parts[0])].addEdge(nodes[int(parts[1])])
        nodes[int(parts[1])].addEdge(nodes[int(parts[0])])
    
    #nodeprints(nodes)

    nodes[0].color = 0
    Node.colorCount += 1
    solved = False
    
    while (not solved):
        solved = True
        for n in nodes:
            solved = solved & n.resolveConflict()
        #nodeprints(nodes)
    
    
    solution = [n.color for n in nodes]
    # prepare the solution in the specified output format
    outputData = str(nodeCount) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))
    outputData += "\n"+ 'colorCount ' + str(Node.colorCount) + ' actual color count '+ str(len(set(solution)))

    return outputData

def nodeprints(nodes):
    for node in nodes:
        print "Node: " + str(node.name) + " color: " + str(node.color);
        print ' '.join(map(str, node.getEdges()))

class Node:
    nodeCount = 0
    colorCount = 0
    def __init__(self):
        self.edges = []
        self.color = None
        self.name = Node.nodeCount
        Node.nodeCount += 1
       
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
    
    def resolveConflict(self):
        edgeColors = set()
        selfclean = True
        neighbourclean = True
        for node in self.edges:
            color = node.color
            if (color == None):
                neirghbourclean = False
            else:
                edgeColors.add(color)
        #pprint(edgeColors)
        '''
        if ( self.color != None ) and (clean == True) and not ( self.color in edgeColors ) :
            #print 'node '+str(self.name) + ' is clean with color ' + str(self.color)
            clean = True
        ''' 
        allColors = frozenset(range(0, Node.colorCount))
        #pprint(allColors)
        possibleColors = allColors.difference(edgeColors)
        #pprint(possibleColors)
        if ( len(possibleColors) > 0 ) :
            minColor = min(possibleColors)
            if ( self.color != minColor ) :
                self.color = minColor
                selfclean = False
            else:
                selfclean = True
        else :
            self.color = Node.colorCount
            Node.colorCount += 1
            selfclean = False
        return selfclean & neighbourclean
        
import sys
from pprint import pprint
import cProfile

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        cProfile.run('print solveIt(inputData)')
        #print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

