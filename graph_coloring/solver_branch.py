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
    nodes = [Node() for _ in range(nodeCount)]

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
    # color it 0 and pop it out
    # repeat until counter is at the end of list
    # start from beginning with the first item in edgesTracker now.   
    colorNow = 0
    while ( len(edgesTracker) != 0 ):
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

    reduced = False
    print 'max color is ' + str(colorNow - 1)
    for node in nodes:
        if ( node.color == (colorNow - 1) ):
            print 'found max color node name '+ str(node.name)
            if node.branch(nodes, colorNow-1, None) == True:
                reduced = True
                break
    if reduced:
        print 'new solution found'
    else:
        print 'keeping old solution'
        
    solution = [n.color for n in nodes]
    # prepare the solution in the specified output format
    outputData = str(nodeCount) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))
    #outputData += "\n"+ 'colorCount ' + str(Node.colorCount) + ' actual color count '+ str(len(set(solution)))
    outputData += "\n"+ 'colorCount ' + str(colorNow) + ' actual color count '+ str(len(set(solution)))


    return outputData

def nodeprints(nodes):
    for node in nodes:
        print "Node: " + str(node.name) + " color: " + str(node.color);
        print ' '.join(map(str, node.getEdges()))

def allSolved(nodes):
    for node in nodes:
        if node.hasConflict():
            return False
    return True
    
class Node:
    nodeCount = 0
    #colorCount = 0
    def __init__(self):
        self.edges = []
        self.color = None
        self.name = Node.nodeCount
        self.colorPossible = []
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
                neighbourclean = False
            else:
                edgeColors.add(color)
        #pprint(edgeColors)
        '''
        if ( self.color != None ) and (neighbourclean == True) and not ( self.color in edgeColors ) :
            #print 'node '+str(self.name) + ' is clean with color ' + str(self.color)
            return True
        '''
        allColors = frozenset(range(0, Node.colorCount))
        #pprint(allColors)
        possibleColors = allColors.difference(edgeColors)
        #pprint(possibleColors)
        if ( len(possibleColors) > 0 ) :
            minColor = min(possibleColors)
            if ( self.color != minColor ) :
                self.color = minColor
            selfclean = True
        else :
            self.color = Node.colorCount
            Node.colorCount += 1
            selfclean = True
        return (selfclean and neighbourclean)
    
    def branch(self, nodes, colorCount, parent):
        # start this loop by reducing colorCount on a particular node
        # maximum recursion depth reached. FIXME
        if (not self.hasConflict()) and (self.color < colorCount):
            return True

        neighbourColors = [n.color for n in self.edges]
        colorCopy = [n.color for n in nodes]
        
        if ( len(self.colorPossible) == 0 ):
            self.colorPossible = range(0, colorCount)
            
        try:
            self.colorPossible.pop(self.colorPossible.index(parent))
        except:
            pass
        possibleCopy = [list(n.colorPossible) for n in nodes]

        while ( len(self.colorPossible) != 0 ):
            if ( len(self.colorPossible) == 1 and self.colorPossible[0] == self.color ):
                #has conflict, but no where to go
                return False
            colorCounter = []
            for color in self.colorPossible:
                colorCounter.append((color, neighbourColors.count(color)))
                
            min_color, min_count = min(colorCounter, key=lambda item:item[1])
            self.color = min_color
            # no conflict, resolved
            if min_count == 0:
                return True
            # otherwise propogate for more options
            flag = True
            for node in self.edges:
                # branch only works on nodes with conflicts
                # one fail would mark the branch invalid
                # reverse to old
                if node.branch(nodes, colorCount, self.color) == False :
                    flag = False
                    break
            
            if ( flag == True ):
                # new answers found (maybe)
                newColors = [n.color for n in nodes]
                maxcolor0 = max(colorCopy)
                maxcolor1 = max(newColors)
                if (( maxcolor0 > maxcolor1 )) or (colorCopy.count(maxcolor0) > newColors.count(maxcolor1)):
                    #new answer is real
                    return True
            # else (fake answer/ conflicted answer)
            # reset
            self.colorPossible.pop(self.colorPossible.index(self.color))
            for n in nodes:
                n.color = colorCopy[n.name]
                # restore selections other than myself, b/c i just kicked out a node
                if ( n.name != self.name ):
                    n.colorPossible = list(possibleCopy[n.name])
        
        # no more color can be tried
        print 'branch: while loop finished, something is wrong'
        return False


        
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

