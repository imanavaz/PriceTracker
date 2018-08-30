import time
import csv
from tqdm import tqdm
from jellyfish import *
import numpy as np


def checkTheSame (row1, row2):#higher is better
    simScore = 0
    if (row1['Brand'].strip().lower() == row2['Brand'].strip().lower()):
        simScore = simScore + 1
    if (row1['Product name'].strip().lower() == row2['Product name'].strip().lower()):
        simScore = simScore + 1
    if (row1['Pack size'].strip().lower() == row2['Pack size'].strip().lower()):
        simScore = simScore + 1
    return simScore


def checkSimilarJWink(row1, row2): #lower is better  
    simScore2 = (jaro_winkler(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) + jaro_winkler(row1['Product name'].strip().lower(), row2['Product name'].strip().lower()) + jaro_winkler(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower()))
    return simScore2


def checkSimilarLev(row1, row2): #lower is better
    simScore3 = (levenshtein_distance(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) + levenshtein_distance(row1['Product name'].strip().lower(), row2['Product name'].strip().lower()) + levenshtein_distance(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower()))
    return simScore3


def checkSimilarHamming(row1, row2): #lower is better
    simScore4 = hamming_distance(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) + hamming_distance(row1['Product name'].strip().lower(), row2['Product name'].strip().lower()) + hamming_distance(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower())
    return simScore4


def extractSimilarData (inputCSV1, inputCSV2):

    print("--- Process started ---")
    
    #first = genfromtxt('data\Woolies.csv', delimiter=',', skip_header=1, usecols=np.arange(0,22))

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
    
    print("--- Reading the files complete ---\n")
    start_time = time.time()
    simMatrixLev = np.zeros(shape=(len(first), len(second)), dtype=float)
    simMatrixNameSim = np.zeros(shape=(len(first), len(second)), dtype=float)
    simMatrixJWink = np.zeros(shape=(len(first), len(second)), dtype=float)
    simMatrixHamming = np.zeros(shape=(len(first), len(second)), dtype=float)
    selectionMatrix = np.zeros(shape=(len(first), len(second)), dtype=float)

    #calculate similarities
    for i in tqdm(range(0,len(first))):
        for j in range(0,len(second)):
            simMatrixNameSim[i,j] = checkTheSame(first[i],second[j])
            simMatrixLev[i,j] = checkSimilarLev(first[i],second[j])
            simMatrixJWink[i,j] = checkSimilarJWink(first[i],second[j])
            simMatrixHamming[i,j] = checkSimilarHamming(first[i],second[j])

    np.savetxt("LEV.csv", simMatrixLev, delimiter=",")
    np.savetxt("NAME.csv", simMatrixNameSim, delimiter=",")
    np.savetxt("JWINK.csv",  simMatrixJWink, delimiter=",")
    np.savetxt("HAM.csv", simMatrixHamming, delimiter=",")

    end_time = time.time()
    print(" --- The process took "+end_time - start_time+" ---")
