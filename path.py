import json
from googlemaps import GoogleMaps
import csv
import sys, copy
import getopt
import matplotlib

def readData(train):
    END = int(train) - 1
    k = 1
    with open('data.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        #Skips the column headers --eg. latitude, longitude, crime location etc
        reader.next()
        #The columns we want to include
        included_cols = [0,1,5,6]
        #Read through all the entries and obtain the required training data
        for row in reader:
            if END >= 0:
                content = list(row[i] for i in included_cols)
                lat = float(content[2])
                long = float(content[3])
                print '[',content[2], ',',content[3] ,']'
                END = END - 1 ;
                k = k+1
            else: break


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        print '######ERROR#######'
        print '...Enter the number of train examples you desire to use. To run 500 examples, type:'
        print 'python path.py -train 500'
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            if len(argv) == 3 and argv[1] == '-train' and argv[2] != '':
                print '...reading ', argv[2], ' training examples'
                NUM = argv[2]
                readData(NUM)
            else:
                print '...enter the number of train examples you desire to use e.g: python path.py -train 500'
                print '...DEFAULT VALUE: 100 training examples'
                NUM = 100
                readData(NUM)

            #raise Usage(msg)
    # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

