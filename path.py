#for the Naive Bayes Classifier
from __future__ import division
import collections
import math
import json
from googlemaps import GoogleMaps
from pygeocoder import Geocoder
import csv
import sys, copy
import getopt
import numpy.random
import time
import subprocess #running perl on the fly
import os #file deletion, copying etc
import shutil

#Plotting and Math Libraries/Tools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.mlab import griddata


##########################
#Function delete(Name_of_File) : Deletes a file from the system
##########################
def delete(file):
    ## if file exists, delete it ##
    if os.path.isfile(file):
        os.remove(file)
    else:    ## Show an error ##
        print("Error: %s file not found" % file)

#Alternate plotting function: Still Under Testing
def plot2(DATA, MAP, CLUSTER):
    
    x = []
    y = []
    z = []
    
    for zip in CLUSTER:
        #Get x,y coordinates from MAP
        xy = MAP[zip]
        x.append(xy[0])
        y.append(xy[1])
        z.append(CLUSTER[zip])

    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')

    ax.scatter(x,y,z, c ='r', marker = 'o')

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    
    plt.show()

################################################
#FUNCTION: plot
        #:Plots the Crime Data on a meshgrid
################################################
def plot(DATA, MAP, CLUSTER):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    x = []
    y = []
    z = []
    
    for zip in CLUSTER:
        #Get x,y coordinates from MAP
        xy = MAP[zip]
        
        x.append(xy[0])
        y.append(xy[1])
        z.append(CLUSTER[zip])

    
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)

    surf = ax.plot_surface(X, Y, Z, rstride=3, cstride=3, cmap=cm.jet,linewidth=1,antialiased=True)
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
    
    #Automatically invoke the perl script to read in the data
    #param = 'world'
    #pipe = subprocess.Popen(["perl", "./cleanup.pl", param], stdout=subprocess.PIPE)
    #perl_result = pipe.stdout.read()

    #print perl_result
    
    PLACES = dict()
    CLUSTER = dict()
    MAP = dict()
    
    END = int(train) - 1
    k = 1
    with open('test.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        #Skips the column headers --eg. latitude, longitude, crime location etc
        reader.next()

        #The columns we want to include
        #included_cols = [0,1,5,6]
        included_cols = [7,8,9,10,11,12] #[0,1,2,3]
        #Read through all the entries and obtain the required training data

        X = []
        Y = []
        Z = []
        
        DATA = []
        
        for row in reader:
            if END >= 0:
                content = list(float(row[i]) for i in included_cols)
                content.append(row[1])
                content.append(row[13])
                #print content
                new_train = []
                
                #Unemployment Levels
                unemployment = content[2]
                if unemployment >= 2000: new_train.append('H')
                elif(unemployment > 1300 and unemployment < 2000 ): new_train.append('M')
                else: new_train.append('L')
                
                #Property Value
                pvalue = content[3]
                if pvalue >= 200000: new_train.append('H')
                elif pvalue < 200000 and pvalue > 120000: new_train.append('M')
                else: new_train.append('L')

                #Education Levels
                edu = content[4]
                if edu >= 88: new_train.append('H')
                elif edu < 88 and edu > 75 : new_train.append('M')
                else: new_train.append('L')
                
                #Street Crime Levels
                street = content[5]
                if street == 1 and content[6] == 'ASSAULT': new_train.append('H')
                elif street == 1 and content[6] != 'ASSAULT': new_train.append('M')
                else: new_train.append('L')

                #Append Label
                if float(content[7]) == 0 : new_train.append('yes')
                else: new_train.append('no')
                
                #Store the Data in a List of training examples, later to be added to a file
                DATA.append(new_train)
            
                #Obtain Latitude and Longitude
                lat = float(content[0])  #float(content[2])
                long = float(content[1]) #float(content[3])
                
                END = END - 1 ;
                k = k+1
                if(lat > 0 and lat < 180 and long > 0 and long < 180):
                    key = (lat, long)
                    if key in PLACES:
                        PLACES[key] += 1
                    else:
                        PLACES[key] = 1
        
                    if content[2] in CLUSTER: #for ZIP code --adding points to that Zip Code
                        CLUSTER[content[2]] += 1;
                        #Set point as average of points assigned to it only for purposes of plotting
                        newpt = MAP[content[2]]
                        newx = (newpt[0] + lat)/2
                        newy = (newpt[1] + long)/2
                        MAP[content[2]] = [newx,newy]
                    else:
                        CLUSTER[content[2]] = 1
                        MAP[content[2]] = [lat,long]
                        #time.sleep(.2) #so I don't get a timeout when I send too many requests to Google per second
            else: break

    #Returns Houses and their Average Price, By ZIP CODE, which is a feature for Naive Bayes classifier later on
    HOUSES = read_Estate()
    #print HOUSES
    #plot only if you have a flag from user to plot the data
    #if plot_Bool == True: plot2(PLACES, MAP, CLUSTER)
    predict(PLACES)
    #find_Path()


##########################
#Function: read_Estate(): Reads in the Real Estate Prices for various Zip Codes, Helps us to make good prediction when it comes to safety
##########################
def read_Estate():
    HOUSES = dict()
    with open('houses.csv','rU') as f:
        next(f) # skip headings
        reader=csv.reader(f)
        reader.next()
        for row in reader:
            HOUSES[row[0]] = float(row[2])
    return HOUSES

def find_Path(MAP, model):
    gmaps = GoogleMaps()
    
    home = raw_input("Enter your starting address: ")
    end =  raw_input("Enter your destination address: ")
    results = Geocoder.geocode(home)
    results2 = Geocoder.geocode(end)
    #results = Geocoder.reverse_geocode(41.96786329,-87.71349889)
    #results2 = Geocoder.reverse_geocode(41.763258, -87.61172601)

    print '---Finding Path from ', results, ' to ', results2

    dirs  = gmaps.directions(results, results2)

    time  = dirs['Directions']['Duration']['seconds']
    dist  = dirs['Directions']['Distance']['meters']
    route = dirs['Directions']['Routes'][0]
    
    PATH = []
    EVALUATION = []
    
    for step in route['Steps']:
        position = (step['Point']['coordinates'][1], step['Point']['coordinates'][0])
        if position in MAP:
            for i in range(4): PATH.append('H')
            PATH.append('no')
        else:
            for i in range(4):PATH.append('L')
            PATH.append('yes')
        
        #PREDICT FOR EACH CITY IN THE INTERMEDIATE STEPS
        with open("predict.arff", "a") as myfile:
            for elem in PATH:
                if elem == 'yes' or elem == 'no': myfile.write(elem)
                else: myfile.write(elem  + ',')
            myfile.write('\n')
        PATH = []

    EVALUATION = model.TestClassifier("predict.arff")
    #mark current place as SAFE since you're already at that location anyways
    EVALUATION[0] = 'yes'
    
    #Print Final Results At this Point
    k = 0
    for step in route['Steps']:
        position = (step['Point']['coordinates'][1], step['Point']['coordinates'][0])
        print step['Point']['coordinates'][1], step['Point']['coordinates'][0] ,  '===========================>SAFE? ', EVALUATION[k]
        print step['descriptionHtml']
        k +=1
    
    #UPDATE THE FILES
    delete("predict.arff")
    filename2 = "predict.arff"
    shutil.copy("predict_start.arff", filename2)
    if os.path.isfile (filename2): print "Have a Safe Journey"
    else: print "#####Problem Here: Error 99. Engineeer Will Fix the Bug ASAP"


#####################################################################################
                            #CLASS: NAIVE BAYES CLASSIFIER
#####################################################################################

#               Features:
#       ***********************
#Real Estate Value   :HIGH, LOW, MEDIUM
#Unemployment Level  :HIGH, LOW, MEDIUM
#Street Crime Level  :HIGH, LOW, MEDIUM
#Education Levels    :HIGH, LOW, MEDIUM

class Model:
    def __init__(self, arffFile):
        self.trainingFile = arffFile
        self.features = {}              #all feature names and their possible values (including the class label)
        self.featureNameList = []       #this is to maintain the order of features as in the arff
        self.featureCounts = collections.defaultdict(lambda: 1)#contains tuples of the form (label, feature_name, feature_value)
        self.featureVectors = []         #contains all the values and the label as the last entry
        self.labelCounts = collections.defaultdict(lambda: 0)   #these will be smoothed later
    
    ##########################
    #Train CLASSIFIER : Trains the classifier, given some features and labels
    ##########################
    def TrainClassifier(self):
        for fv in self.featureVectors:
            self.labelCounts[fv[len(fv)-1]] += 1    #udpate count of the label
            for counter in range(0, len(fv)-1):
                self.featureCounts[(fv[len(fv)-1], self.featureNameList[counter], fv[counter])] += 1
        
        for label in self.labelCounts:  #increase label counts (smoothing). remember that the last feature is actually the label
            for feature in self.featureNameList[:len(self.featureNameList)-1]:
                self.labelCounts[label] += len(self.features[feature])

    ##########################
    #NAIVE BAYES CLASSIFIER : classifies the data
    ##########################
    def Classify(self, featureVector):
        probabilityPerLabel = {}
        for label in self.labelCounts:
            logProb = 0
            for featureValue in featureVector:
                logProb += math.log(self.featureCounts[(label, self.featureNameList[featureVector.index(featureValue)], featureValue)]/self.labelCounts[label])
            probabilityPerLabel[label] = (self.labelCounts[label]/sum(self.labelCounts.values())) * math.exp(logProb)
        #print probabilityPerLabel
        return max(probabilityPerLabel, key = lambda classLabel: probabilityPerLabel[classLabel])
    
    ##########################
    #Function GetValues: Gets the features and values for training purposes
    ##########################
    def GetValues(self, DATA):
        with open(self.trainingFile, "a") as myfile:
            for example in DATA:
                for elem in example:
                    if elem == 'yes' or elem == 'no': myfile.write(elem)
                    else: myfile.write(elem  + ',')
                myfile.write('\n')
        
        file = open(self.trainingFile, 'r')
        for line in file:
            if line[0] != '@':  #start of actual data
                self.featureVectors.append(line.strip().lower().split(','))
            else:        #feature definitions
                if line.strip().lower().find('@data') == -1 and (not line.lower().startswith('@relation')):
                    self.featureNameList.append(line.strip().split()[1])
                    self.features[self.featureNameList[len(self.featureNameList) - 1]] = line[line.find('{')+1: line.find('}')].strip().split(',')
        file.close()
    
    ###########################
    #Function TestClassifier: Runs the classifier on the testfile to see the accuracy
    ###########################
    def TestClassifier(self, arffFile):
        PREDICTION  = []
        #Find Prediction Accuracy using these variables
        tot = 0
        correct = 0
    
        #Use the user input for prediction ie. these are the set of intermediate cities to destination
        file = open(arffFile, 'r')
        for line in file:
            if line[0] != '@':
                vector = line.strip().lower().split(',')
                print '************', vector
                prediction = self.Classify(vector)
                PREDICTION.append(prediction)
                expected = vector[len(vector) - 1]
                #print "classifier: " + prediction + " given " + expected
                if prediction == expected: correct += 1
                tot+=1
        print 'Percentage Confidence = ',(correct/tot) * 100, '%'
        return PREDICTION

###########################################
#Function: predict()
#Calls the Naive Bayes Classifier, Trains and Predicts Safety of Path Given  User Query
###########################################
#This file updates the files: Deletes the training data file and creates a fresh copy with the attributes
def predict(DATA):
    model = Model("trainingFile.arff")
    #print DATA
    model.GetValues(DATA) #this will be appended to output and then used for training (test.csv)
    model.TrainClassifier()
    find_Path(DATA, model)
    #EVALUATION = model.TestClassifier("predict.arff") #("features.arff")
    updateFiles(model)


###########################################
#updateFiles
###########################################
#This file updates the files: Deletes the training data file and creates a fresh copy with the attributes
def updateFiles(model):
    #create a new file for next run--delete the file with appended data, i.e. create fresh copy of training data-to be appended upon run
    delete(model.trainingFile)
    filename2 = model.trainingFile
    shutil.copy("train_start.arff", filename2)
    if os.path.isfile (filename2): print "Successfully created a new file!! *****"

#####################################################################################
                            # MAIN AND EXCEPTION HANDLERS
#####################################################################################

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
            elif len(argv) == 2:
                print '...enter the number of train examples you desire to use e.g: python path.py -train 500'
                print '...DEFAULT VALUE: 100 training examples'
                NUM = 100
                readData(NUM, plot_Flag)
            else:
                readData(argv[2], plot_Flag)
            #raise Usage(msg)
    # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

