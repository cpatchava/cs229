import json
from googlemaps import GoogleMaps
from pygeocoder import Geocoder
import csv
import sys, copy
import getopt
import random
import time

#Plotting and Math Libraries/Tools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.mlab import griddata

def plot2(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')

    ax.scatter(X,Y,Z, c ='r', marker = 'o')

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    
    plt.show()

################################################
#FUNCTION: plot
        #:Plots the Crime Data on a meshgrid
################################################
def plot(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
                           linewidth=0,antialiased=True)

    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf)

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Crime Stats')

    plt.show()

###########################################
#FUNCTION: readData
        #:Reads in the training Data and arguments
###########################################
def readData(train, plot_Bool):
    END = int(train) - 1
    k = 1
    with open('data.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        #Skips the column headers --eg. latitude, longitude, crime location etc
        reader.next()
        #The columns we want to include
        included_cols = [0,1,5,6]
        #Read through all the entries and obtain the required training data
        X = []
        Y = []
        Z = []
        for row in reader:
            if END >= 0:
                content = list(row[i] for i in included_cols)
                lat = float(content[2])
                long = float(content[3])
                #results = Geocoder.reverse_geocode(lat, long);
                #print results[0]
                #print '[',content[2], ',',content[3] ,']'
                END = END - 1 ;
                k = k+1
                X.append(lat)
                Y.append(long)
                Z.append(random.randint(0,5))
                #time.sleep(.2) #so I don't get a timeout when I send too many requests to Google per second
            else: break
        
    #plot only if you have a flag from user to plot the data
    #if plot_Bool == True: plot(X,Y,Z)
    find_Path()

def find_Path():
    gmaps = GoogleMaps()

    home = raw_input("Enter your starting address: ")
    end =  raw_input("Enter your end address: ")
    results = Geocoder.geocode(home)
    results2 = Geocoder.geocode(end)

    dirs  = gmaps.directions(results, results2)

    time  = dirs['Directions']['Duration']['seconds']
    dist  = dirs['Directions']['Distance']['meters']
    route = dirs['Directions']['Routes'][0]
    for step in route['Steps']:
        print step['Point']['coordinates'][1], step['Point']['coordinates'][0]
        print step['descriptionHtml']


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
            #plot only if you have a flag from user to plot the data
            if len(argv) == 4:
                if argv[3] == '-plot':
                    plot_Flag = True
                else:
                    print '#####ERROR: Flag Option Does not exist. To Plot, run: python path.py -train NUM_TRAIN -plot'
                    plot_Flag = False
                    sys.exit()

            if len(argv) == 3 and argv[1] == '-train' and argv[2] != '':
                print '...reading ', argv[2], ' training examples'
                NUM = argv[2]
                readData(NUM, plot_Flag)
            else:
                print '...enter the number of train examples you desire to use e.g: python path.py -train 500'
                print '...DEFAULT VALUE: 100 training examples'
                NUM = 100
                readData(NUM, plot_Flag)
            #raise Usage(msg)
    # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

