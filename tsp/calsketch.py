from matplotlib import pyplot
import sys
from pprint import pprint
import csv

def main(file):
    with open(file, 'rb') as csvfile:
        data = csv.reader(csvfile)
        x = []
        y = []
        first = True
        for row in data:
            if ( first ) :
                first = False
                continue
            x.append(row[0])
            y.append(row[1])
            
        pyplot.plot(x, y)
        pyplot.show()
    return



if __name__ == '__main__':
    fileLocation = 'calculation_2opt.csv'
    main(fileLocation)
        #inputDataFile = open(fileLocation, 'r')
        #inputData = ''.join(inputDataFile.readlines())
        #inputDataFile.close()
        #cProfile.run('solveIt(inputData)')
        #print solveIt(inputData)