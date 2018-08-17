import time
import csv
from logic.levenshtein import iterative_levenshtein
from tqdm import tqdm

def checkTheSame (row1, row2):
    if ((row1['Brand'].strip().lower() == row2['Brand'].strip().lower()) and 
        (row1['Product name'].strip().lower() == row2['Product name'].strip().lower()) and
        (row1['Pack size'].strip().lower() == row2['Pack size'].strip().lower())):
        return True
   
    return False


def checkSimilarLev(row1, row2):
    if (iterative_levenshtein(row1['Brand'].strip().lower(), row2['Brand'].strip().lower(), costs=(1, 1, 1)) < 2 and
        iterative_levenshtein(row1['Product name'].strip().lower(), row2['Product name'].strip().lower(), costs=(1, 1, 1)) < 2 and
        iterative_levenshtein(row1['Pack size'].strip().lower(), row2['Pack size'].strip().lower(), costs=(1, 1, 1)) < 2):
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
            if (checkTheSame(a,b)):
                print('-- Found Same Item: {0} , {1} , {2} <---> {3} , {4} , {5}\n'.format(a['Brand'], a['Product name'], a['Pack size'], b['Brand'], b['Product name'], b['Pack size']))
                simcounter = simcounter + 1
            elif(checkSimilarLev(a,b)):
                print('-- Found LV Similar Item: {0} , {1} , {2} <---> {3} , {4} , {5}\n'.format(a['Brand'], a['Product name'], a['Pack size'], b['Brand'], b['Product name'], b['Pack size']))
                simcounter = simcounter + 1    
    
    print('--- process finished in {0} seconds and found {1} similar rows ---'.format((time.time() - start_time), simcounter))

