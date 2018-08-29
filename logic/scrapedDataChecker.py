import time
import csv
#from logic.levenshtein import iterative_levenshtein
from tqdm import tqdm
from jellyfish import *
from numpy import genfromtxt



def checkTheSame (row1, row2):#higher is better
    simScore = 0
    if (row1['Brand'].strip().lower() == row2['Brand'].strip().lower()):
        simScore = simScore + 1

    if (row1['Product name'].strip().lower() == row2['Product name'].strip().lower()):
        simScore = simScore + 1

    if (row1['Pack size'].strip().lower() == row2['Pack size'].strip().lower()):
        simScore = simScore + 1
    
    return simScore


def checkSimilarJWink(row1, row2):#lower is better  
    simScore2 = (jaro_winkler(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) + 
                jaro_winkler(row1['Product name'].strip().lower(), row2['Product name'].strip().lower()) + 
                jaro_winkler(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower()))# / 3
    
    return simScore2
   

#lower is better
def checkSimilarLev(row1, row2):
    simScore3 = levenshtein_distance(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) + 
               levenshtein_distance(row1['Product name'].strip().lower(), row2['Product name'].strip().lower()) + 
               levenshtein_distance(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower())
    #if (iterative_levenshtein(row1['Brand'].strip().lower(), row2['Brand'].strip().lower(), costs=(1, 1, 1)) <= 3 and
    #    iterative_levenshtein(row1['Product name'].strip().lower(), row2['Product name'].strip().lower(), costs=(1, 1, 1)) <= 3):
        #iterative_levenshtein(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower(), costs=(1, 1, 1)) <= 3):
    
    return simScore3


def checkSimilarHamming(row1, row2): #lower is better
    simScore4 = hamming_distance(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) +
               hamming_distance(row1['Product name'].strip().lower(), row2['Product name'].strip().lower())+
               hamming_distance(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower())

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
    
    print("--- Reading the files complete ---")
    
    start_time = time.time()
    
    simcounter = 0

    simMatrixLev = np.zeros([len(first), len(second), dtype=float])
    simMatrixNameSim = np.zeros([len(first), len(second), dtype=float])
    simMatrixJWink = np.zeros([len(first), len(second), dtype=float])
    simMatrixHamming = np.zeros([len(first), len(second), dtype=float])

    #calculate similarities
    for i in tqdm(range(len(first))):
        for j in range(len(second):
            simMatrixnameSim[i,j] = checkTheSame(first[i],second[j])
            simMatrixLev[i,j] = checkSimilarLev(first[i],second[j])
            simMatrixJWink[i,j] = checkSimilarJWink(first[i],second[j])
            simMatrixHamming[i,j] = checkSimilarHamming(first[i],second[j])

