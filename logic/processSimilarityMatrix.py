import time
import csv
from tqdm import tqdm
import numpy as np
import bottleneck as bn


def findSimilarItems(inputCSV1, inputCSV2, weights, simPath):

    print(" --- Processing similarity matrices at " + simPath + " ---")

    first = []
    with open(inputCSV1,'r') as csvinput1:
        reader1 = csv.DictReader(csvinput1, delimiter=',', quotechar='|') 
        for row in reader1: # each row is a list
            first.append(row)
    
    second = []
    with open(inputCSV2,'r') as csvinput2:
        reader2 = csv.DictReader(csvinput2, delimiter=',', quotechar='|') 
        for row in reader2: # each row is a list
            second.append(row)
    
    wLev = 0.0
    wName = 0.0
    wHam = 0.0
    wJWink = 0.0

    with open(weights,'r') as wCSV:
        reader3 = csv.reader(wCSV, delimiter=',') 
        next(reader3)
        ws = next(reader3)
        wLev = float(ws[0])
        wName = float(ws[1])
        wJWink = float(ws[2])
        wHam = float(ws[3])
    
    levSim = np.genfromtxt(simPath + 'LEVn.csv', delimiter=',')
    levSim = np.multiply(levSim, wLev)
    nameSim = np.genfromtxt(simPath + 'NAMEn.csv', delimiter=',')
    nameSim = np.multiply(nameSim, wName)
    hamSim = np.genfromtxt(simPath + 'HAMn.csv', delimiter=',')
    hamSim = np.multiply(hamSim, wHam)
    jwinkSim = np.genfromtxt(simPath + 'JWINKn.csv', delimiter=',')
    jwinkSim = np.multiply(jwinkSim, wJWink)
    
    simMatrix = np.zeros(shape=(len(first), len(second)), dtype=float)
    simMatrix = levSim + nameSim + hamSim + jwinkSim
    print(simMatrix.shape)
    np.savetxt(simPath+'simMat.csv', simMatrix, delimiter=",")
    
    print(" --- Similarity matrix created ---")
    
    print(" --- Generating recommendations ---")
    
    swMat = np.copy(simMatrix)

    


    indices =  np.argpartition(swMat.flatten(), -10)[-10:]
    indices = np.vstack(np.unravel_index(indices, swMat.shape)).T
    
    for i in range(0,len(indices)):
        print(indices[i])
        print(swMat[indices[i][0]][indices[i][1]])
        print(first[indices[i][0]]['Brand'] + " - " +  first[indices[i][0]]['Product name'] + " - " + first[indices[i][0]]['Pack size'] +
                " <-> " + 
                second[indices[i][1]]['Brand'] + " - " +  second[indices[i][1]]['Product name'] + " - " + second[indices[i][1]]['Pack size'])
    
    #### this was for top three items per row 
    #top3 = np.zeros(shape=(len(first),3), dtype=int)
    #for i in tqdm(range(0,len(first))):
    #    top3[i] = np.argsort(simMatrix[i,:])[-3:][::-1]
    #np.savetxt(simPath+'top3.csv', top3, delimiter=",")

    print(" --- Recommendations complete ---")


