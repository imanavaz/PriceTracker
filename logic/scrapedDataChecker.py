import time
import csv
from logic.levenshtein import iterative_levenshtein
from tqdm import tqdm
from jellyfish import *


def checkTheSame (row1, row2):
    if ((row1['Brand'].strip().lower() == row2['Brand'].strip().lower()) and 
        (row1['Product name'].strip().lower() == row2['Product name'].strip().lower())): #and
        #(row1['Pack size'].strip().lower() == row2['Pack size'].strip().lower())):
        return True
   
    return False


def checkSimilarJWink(row1, row2):
    simScore = (jaro_winkler(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) + 
                jaro_winkler(row1['Product name'].strip().lower(), row2['Product name'].strip().lower())) / 2 #+ 
                #jaro_winkler(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower())) / 3
    if (simScore >= 60):
        return True
    
    return False
            

def checkSimilarLev(row1, row2):
    #if (iterative_levenshtein(row1['Brand'].strip().lower(), row2['Brand'].strip().lower(), costs=(1, 1, 1)) <= 3 and
    #    iterative_levenshtein(row1['Product name'].strip().lower(), row2['Product name'].strip().lower(), costs=(1, 1, 1)) <= 3):
        #iterative_levenshtein(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower(), costs=(1, 1, 1)) <= 3):
    if (levenshtein_distance(row1['Brand'].strip().lower(), row2['Brand'].strip().lower()) <= 3 and 
        levenshtein_distance(row1['Product name'].strip().lower(), row2['Product name'].strip().lower()) <= 4):
            return True
    return False


def extractSimilarData (inputCSV1, inputCSV2):

    print("--- Process started ---")
    
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
    for a in tqdm(first):
        for b in second:
            #simScore = 1/((levenshtein_distance(a['Brand'].strip().lower(), b['Brand'].strip().lower()) + 
            #    levenshtein_distance(a['Product name'].strip().lower(), b['Product name'].strip().lower()) + 
            #    levenshtein_distance(a['Pack size'].strip().lower(), b['Pack size'].strip().lower())) / 3)

            #print('-- JW Similarity for Items: {0} , {1} , {2} <---> {3} , {4} , {5}\n-- is {6}\n\n'.format(a['Brand'], a['Product name'], a['Pack size'], b['Brand'], b['Product name'], b['Pack size'], simScore))
            
            if (checkTheSame(a,b)):
                print('-- Found Same Item: {0} , {1} , {2} <---> {3} , {4} , {5}\n'.format(a['Brand'], a['Product name'], a['Pack size'], b['Brand'], b['Product name'], b['Pack size']))
                simcounter = simcounter + 1
            elif(checkSimilarLev(a,b)):
                print('-- Found LV Similar Item: {0} , {1} , {2} <---> {3} , {4} , {5}\n'.format(a['Brand'], a['Product name'], a['Pack size'], b['Brand'], b['Product name'], b['Pack size']))
                simcounter = simcounter + 1    
            elif (checkSimilarJWink(a,b)):
                print('-- Found JW Similar Item: {0} , {1} , {2} <---> {3} , {4} , {5}\n'.format(a['Brand'], a['Product name'], a['Pack size'], b['Brand'], b['Product name'], b['Pack size']))
                simcounter = simcounter + 1
            
    print('--- process finished in {0} seconds and found {1} similar rows ---'.format((time.time() - start_time), simcounter))

