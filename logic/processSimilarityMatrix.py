import time
import csv
import readchar as rc
from tqdm import tqdm
import numpy as np
#from scrapedDataChecker import *



def processSimilarItemsNoTraining(inputFirst, inputSecond, simPath, funfacts, funfactIndex):#this does not process/consider the feedback 

    print(" --- Processing similarity matrix at " + simPath + " ---")
    print(" This will take some time, please be patient...")

    first = []
    with open(inputFirst,'r') as csvinput1:
        reader1 = csv.DictReader(csvinput1, delimiter=',') 
        for row in reader1: # each row is a list
            first.append(row)

    second = []
    with open(inputSecond,'r') as csvinput2:
        reader2 = csv.DictReader(csvinput2, delimiter=',') 
        for row in reader2: # each row is a list
            second.append(row)
   
    # clear the previous matches
    with open(simPath + 'Matches.csv', 'w+', newline='') as cM:
        fM = ['Date of data Extraction 1', 'Brand 1', 'Product name 1', 'Category 1', 'Pack size 1', 'Serving size 1', 'Servings per pack 1', 'Product code 1', 'Energy per 100g (or 100ml) 1', 'Protein per 100g (or 100ml) 1', 'Total fat per 100g (or 100ml) 1', 'Saturated fat per 100g (or 100ml) 1', 'Carbohydrate per 100g (or 100ml) 1', 'Sugars per 100g (or 100ml) 1', 'Sodium per 100g (or 100ml) 1', 'Original Price 1', 'Price Promoted 1', 'Price Promoted Price 1', 'Multi Buy Special 1', 'Multi Buy Special Details 1', 'Multi Buy Price 1', 'UID 1',
                            'Date of data Extraction 2', 'Brand 2', 'Product name 2', 'Category 2', 'Pack size 2', 'Serving size 2', 'Servings per pack 2', 'Product code 2', 'Energy per 100g (or 100ml) 2', 'Protein per 100g (or 100ml) 2', 'Total fat per 100g (or 100ml) 2', 'Saturated fat per 100g (or 100ml) 2', 'Carbohydrate per 100g (or 100ml) 2', 'Sugars per 100g (or 100ml) 2', 'Sodium per 100g (or 100ml) 2', 'Original Price 2', 'Price Promoted 2', 'Price Promoted Price 2', 'Multi Buy Special 2', 'Multi Buy Special Details 2', 'Multi Buy Price 2', 'UID 2' ]
        mW = csv.DictWriter(cM, fieldnames=fM)
        mW.writeheader()

    # clear the previous un-matched items
    with open(simPath + 'unmatchedItems.csv', 'w+', newline='') as cUM:
        fUM = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
        umW = csv.DictWriter(cUM, fieldnames=fUM)
        umW.writeheader()   

    swMat = np.genfromtxt(simPath + 'simMat.csv', delimiter=',')

    print(" --- Generating recommendations ---")
    
    matches = [] #arraye to keep all the similar pairs as tuples of [(first, second)...]
    getch = ''

    #read first batch of indices 
    indices =  np.argpartition(swMat.flatten(), -100)[-100]
    indices = np.vstack(np.unravel_index(indices, swMat.shape)).T
    
    while (swMat[indices[0][0]][indices[0][1]] >= 2):
        
        for i in range(0,len(indices)):
            print(" ")
            if (swMat[indices[i][0]][indices[i][1]] > 0): #if the item is not already matched in current batch
                print(first[indices[i][0]]['Brand'] + " - " +  first[indices[i][0]]['Product name'] + " - " + first[indices[i][0]]['Pack size'] +
                        " <===> " + 
                        second[indices[i][1]]['Brand'] + " - " +  second[indices[i][1]]['Product name'] + " - " + second[indices[i][1]]['Pack size'])# + " -- similarity is %s :" % swMat[indices[i][0]][indices[i][1]])
                
                print ('Is this recommendation true (y|n)?')
                getch = rc.readchar()

                while not (getch == b'y' or getch == b'Y' or getch == b'n' or getch == b'N' or getch == b'q' or getch == b'Q'):
                    print('Invalid input, sorry! - please answer by n or y')
                    getch = rc.readchar()
                
                if (getch == b'y' or getch == b'Y'):
                    #remove the items from simMatrix
                    swMat[indices[i][0], :] = -1.0   
                    swMat[:, indices[i][1]] = -1.0
                    #save the match
                    matches.append((first[indices[i][0]], second[indices[i][1]]))                    
                    
                    """#penalise/promote the recommenders
                    #haming's avg = 0.58 and median = 0.6
                    if (hamS[indices[i][0]][indices[i][1]] >= 0.6):#correctly recommended (use original similarity matrix before applying weights)
                        wHam += 0.0001 #promote
                    else:
                        wHam -= 0.0001 #penalise
                    
                    #jwink avg = 0.0143 median = 0.0137
                    if (jwinkS[indices[i][0]][indices[i][1]] >= 0.0137):#correctly recommended 
                        wJWink += 0.0001 #promote
                    else:
                        wJWink -= 0.0001 #penalise

                    #lve avg = 0.560 median = 0.582
                    if (levS[indices[i][0]][indices[i][1]] >= 0.582):#correctly recommended 
                        wLev += 0.0001 #promote
                    else:
                        wLev -= 0.0001 #penalise
                    
                    #name avg = 0.017 median = 0
                    if (nameS[indices[i][0]][indices[i][1]] > 0):#correctly recommended 
                        wName += 0.0001 #promote
                    else:
                        wName -= 0.0001 #penalise"""
                
                elif (getch == b'n' or getch == b'N'):
                    #void that similarity calculation
                    swMat[indices[i][0], indices[i][1]] = -1.0  
                    
                    """#penalise/promote the recommenders
                    #haming's avg = 0.58 and median = 0.6
                    if (hamS[indices[i][0]][indices[i][1]] < 0.6):#correctly not recommended (use original similarity matrix before applying weights)
                        wHam += 0.0001 #promote
                    else:
                        wHam -= 0.0001 #penalise
                    
                    #jwink avg = 0.0143 median = 0.0137
                    if (jwinkS[indices[i][0]][indices[i][1]] < 0.0137):#correctly not recommended 
                        wJWink += 0.0001 #promote
                    else:
                        wJWink -= 0.0001 #penalise

                    #lve avg = 0.560 median = 0.582
                    if (levS[indices[i][0]][indices[i][1]] < 0.582):#correctly not recommended 
                        wLev += 0.0001 #promote
                    else:
                        wLev -= 0.0001 #penalise
                    
                    #name avg = 0.017 median = 0
                    if (nameS[indices[i][0]][indices[i][1]] == 0):#correctly not recommended 
                        wName += 0.0001 #promote
                    else:
                        wName -= 0.0001 #penalise"""

                elif (getch == b'q' or getch == b'Q'):
                    break

        print(" --- Saving results... ---\n")
        print(" * While I am saving the results so far...")
        print(" * Did you know ...")
        print(" * "+getFunFact(funfactIndex, funfacts))
        funfactIndex += 1
        if funfactIndex >= len(funfacts):
            funfactIndex = 0
        print()
        #time.sleep(3)

        #I should probably avoid saving this multiple times too! Given each file is 3GB
        #np.savetxt('res/swMat.csv', swMat, delimiter=",")
       
        #save new weights
        """with open(weights, 'w', newline='') as csvfile:
            fieldnames = ['levenshtein', 'name', 'jwink', 'hamming']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'levenshtein': wLev, 'name': wName, 'jwink': wJWink, 'hamming': wHam})
        """
        
        #save matches
        with open(simPath + 'Matches.csv', 'a', newline='') as csvMatches:
            fieldnamesMatch = ['Date of data Extraction 1', 'Brand 1', 'Product name 1', 'Category 1', 'Pack size 1', 'Serving size 1', 'Servings per pack 1', 'Product code 1', 'Energy per 100g (or 100ml) 1', 'Protein per 100g (or 100ml) 1', 'Total fat per 100g (or 100ml) 1', 'Saturated fat per 100g (or 100ml) 1', 'Carbohydrate per 100g (or 100ml) 1', 'Sugars per 100g (or 100ml) 1', 'Sodium per 100g (or 100ml) 1', 'Original Price 1', 'Price Promoted 1', 'Price Promoted Price 1', 'Multi Buy Special 1', 'Multi Buy Special Details 1', 'Multi Buy Price 1', 'UID 1',
                               'Date of data Extraction 2', 'Brand 2', 'Product name 2', 'Category 2', 'Pack size 2', 'Serving size 2', 'Servings per pack 2', 'Product code 2', 'Energy per 100g (or 100ml) 2', 'Protein per 100g (or 100ml) 2', 'Total fat per 100g (or 100ml) 2', 'Saturated fat per 100g (or 100ml) 2', 'Carbohydrate per 100g (or 100ml) 2', 'Sugars per 100g (or 100ml) 2', 'Sodium per 100g (or 100ml) 2', 'Original Price 2', 'Price Promoted 2', 'Price Promoted Price 2', 'Multi Buy Special 2', 'Multi Buy Special Details 2', 'Multi Buy Price 2', 'UID 2' ]
            matchWriter = csv.DictWriter(csvMatches, fieldnames=fieldnamesMatch)

            for m in matches:
                matchWriter.writerow({'Date of data Extraction 1': m[0]['Date of data Extraction'],
                                    'Brand 1': m[0]['Brand'], 
                                    'Product name 1': m[0]['Product name'], 
                                    'Category 1': m[0]['Category'], 
                                    'Pack size 1': m[0]['Pack size'], 
                                    'Serving size 1': m[0]['Serving size'], 
                                    'Servings per pack 1': m[0][ 'Servings per pack'], 
                                    'Product code 1': m[0]['Product code'], 
                                    'Energy per 100g (or 100ml) 1': m[0]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml) 1': m[0]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml) 1': m[0]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml) 1': m[0][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml) 1': m[0]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml) 1': m[0]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml) 1': m[0][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price 1': m[0]['Original Price'], 
                                    'Price Promoted 1': m[0]['Price Promoted'], 
                                    'Price Promoted Price 1': m[0]['Price Promoted Price'], 
                                    'Multi Buy Special 1': m[0]['Multi Buy Special'], 
                                    'Multi Buy Special Details 1': m[0][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price 1': m[0]['Multi Buy Price'], 
                                    'UID 1': m[0]['UID'],
                                    'Date of data Extraction 2': m[1]['Date of data Extraction'],
                                    'Brand 2': m[1]['Brand'], 
                                    'Product name 2': m[1]['Product name'], 
                                    'Category 2': m[1]['Category'], 
                                    'Pack size 2': m[1]['Pack size'], 
                                    'Serving size 2': m[1]['Serving size'], 
                                    'Servings per pack 2': m[1][ 'Servings per pack'], 
                                    'Product code 2': m[1]['Product code'], 
                                    'Energy per 100g (or 100ml) 2': m[1]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml) 2': m[1]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml) 2': m[1]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml) 2': m[1][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml) 2': m[1]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml) 2': m[1]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml) 2': m[1][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price 2': m[1]['Original Price'], 
                                    'Price Promoted 2': m[1]['Price Promoted'], 
                                    'Price Promoted Price 2': m[1]['Price Promoted Price'], 
                                    'Multi Buy Special 2': m[1]['Multi Buy Special'], 
                                    'Multi Buy Special Details 2': m[1][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price 2': m[1]['Multi Buy Price'], 
                                    'UID 2': m[1]['UID']})


        if (getch == b'q' or getch == b'Q'):
            break

        #read new set of indexes
        indices = np.argpartition(swMat.flatten(), -100)[-100:]
        indices = np.vstack(np.unravel_index(indices, swMat.shape)).T
    #end of recommendation process

    #process remaining unmatched items
    if (getch == b'q' or getch == b'Q'):
        print(" --- Process interrupted ---")
    else:
        print(" --- No more similar items with similarity more than 1.5 found ---")
        print(" --- Processing remainig none-similar items ---")
        #list all unmatched items
        with open(simPath + 'unmatchedItems.csv', 'a', newline='') as csvUMatches:
            fieldnamesUMatch = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
            unmatchWriter = csv.DictWriter(csvUMatches, fieldnames=fieldnamesUMatch)

            for i in tqdm(range(0,np.size(swMat,0))): #process rows -> first[]
                if (np.argmax(swMat[i,:]) > 0): #row has not been assigned
                    #print(first[i])
                    unmatchWriter.writerow({'Date of data Extraction': first[i]['Date of data Extraction'],
                                    'Brand': first[i]['Brand'], 
                                    'Product name': first[i]['Product name'], 
                                    'Category': first[i]['Category'], 
                                    'Pack size': first[i]['Pack size'], 
                                    'Serving size': first[i]['Serving size'], 
                                    'Servings per pack': first[i][ 'Servings per pack'], 
                                    'Product code': first[i]['Product code'], 
                                    'Energy per 100g (or 100ml)': first[i]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml)': first[i]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml)': first[i]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml)': first[i][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml)': first[i]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml)': first[i]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml)': first[i][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price': first[i]['Original Price'], 
                                    'Price Promoted': first[i]['Price Promoted'], 
                                    'Price Promoted Price': first[i]['Price Promoted Price'], 
                                    'Multi Buy Special': first[i]['Multi Buy Special'], 
                                    'Multi Buy Special Details': first[i][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price': first[i]['Multi Buy Price'], 
                                    'UID': first[i]['UID']})

            for j in tqdm(range(0,np.size(swMat,1))): #process columns -> second[]
                if (np.argmax(swMat[:,j]) > 0): #column has not been assigned
                    #print(second[j])
                    unmatchWriter.writerow({'Date of data Extraction': second[j]['Date of data Extraction'],
                                    'Brand': second[j]['Brand'], 
                                    'Product name': second[j]['Product name'], 
                                    'Category': second[j]['Category'], 
                                    'Pack size': second[j]['Pack size'], 
                                    'Serving size': second[j]['Serving size'], 
                                    'Servings per pack': second[j][ 'Servings per pack'], 
                                    'Product code': second[j]['Product code'], 
                                    'Energy per 100g (or 100ml)': second[j]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml)': second[j]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml)': second[j]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml)': second[j][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml)': second[j]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml)': second[j]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml)': second[j][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price': second[j]['Original Price'], 
                                    'Price Promoted': second[j]['Price Promoted'], 
                                    'Price Promoted Price': second[j]['Price Promoted Price'], 
                                    'Multi Buy Special': second[j]['Multi Buy Special'], 
                                    'Multi Buy Special Details': second[j][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price': second[j]['Multi Buy Price'], 
                                    'UID': second[j]['UID']})

    print(" --- Process complete ---")
#end of processSimilarItems


#separate function just to create similarity matrix from recommendations and not to do processing 
def createSimMatrix (weights, simPath):

    print(" --- Processing similarity matrices at " + simPath + " to create simMatrix ---")

    wLev = 0.0
    wName = 0.0
    wHam = 0.0
    wJWink = 0.0

    with open(weights,'r') as wCSV:
        reader = csv.reader(wCSV, delimiter=',') 
        next(reader)
        ws = next(reader)
        wLev = float(ws[0])
        wName = float(ws[1])
        wJWink = float(ws[2])
        wHam = float(ws[3])

    print(" ***  Reading LevSim ***")
    levSim = np.genfromtxt(simPath + 'LEVn.csv', delimiter=',')
    levSim = np.multiply(levSim, wLev)
    simMatrix = np.zeros_like(levSim) #initiate simMatrix to be similar size as levSim
    simMatrix += levSim
    levSim = None #release memory 

    print(" ***  Reading NameSim ***")
    nameSim = np.genfromtxt(simPath + 'NAMEn.csv', delimiter=',')
    nameSim = np.multiply(nameSim, wName)
    simMatrix += nameSim
    nameSim = None

    print(" ***  Reading HamSim ***")
    hamSim = np.genfromtxt(simPath + 'HAMn.csv', delimiter=',')
    hamSim = np.multiply(hamSim, wHam)
    simMatrix += hamSim
    hamSim = None
    
    print(" ***  Reading JWinkSim ***")
    jwinkSim = np.genfromtxt(simPath + 'JWINKn.csv', delimiter=',')
    jwinkSim = np.multiply(jwinkSim, wJWink)
    simMatrix += jwinkSim
    jwinkSim = None
    
    np.savetxt(simPath+'simMat.csv', simMatrix, delimiter=",")
    
    print(" *** Similarity matrix created ***")
#end of createSimMatrix


def loadFunFacts(funf):
    #fun facts to improve user experience 
    with open('res/funfacts.csv','r') as funfactsCSV:
        readerf = csv.DictReader(funfactsCSV, delimiter=',') 
        for ffact in readerf: # each row is a list
            funf.append(ffact)
#end of loadFunFacts


def getFunFact(idx, funf):
    if (idx >= len(funf)):
        idx = 0
    
    ff = funf[idx]['fact']
    idx += 1
    return ff
#end of getFunFact


#============================== the previous function which does not work with large files well     
def processSimilarItemsWithTraining(inputFirst, inputSecond, weights, simPath, funfacts, funfactIndex):

    print(" --- Processing similarity matrix at " + simPath + " ---")
    print(" This will take some time, please be patient...")

    #read scrapped data 
    first = []
    with open(inputFirst,'r') as csvinput1:
        reader1 = csv.DictReader(csvinput1, delimiter=',') 
        for row in reader1: # each row is a list
            first.append(row)

    second = []
    with open(inputSecond,'r') as csvinput2:
        reader2 = csv.DictReader(csvinput2, delimiter=',') 
        for row in reader2: # each row is a list
            second.append(row)    

    #read weights 
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
    
    # clear the previous matches
    with open(simPath + 'Matches.csv', 'w+', newline='') as cM:
        fM = ['Date of data Extraction 1', 'Brand 1', 'Product name 1', 'Category 1', 'Pack size 1', 'Serving size 1', 'Servings per pack 1', 'Product code 1', 'Energy per 100g (or 100ml) 1', 'Protein per 100g (or 100ml) 1', 'Total fat per 100g (or 100ml) 1', 'Saturated fat per 100g (or 100ml) 1', 'Carbohydrate per 100g (or 100ml) 1', 'Sugars per 100g (or 100ml) 1', 'Sodium per 100g (or 100ml) 1', 'Original Price 1', 'Price Promoted 1', 'Price Promoted Price 1', 'Multi Buy Special 1', 'Multi Buy Special Details 1', 'Multi Buy Price 1', 'UID 1',
                            'Date of data Extraction 2', 'Brand 2', 'Product name 2', 'Category 2', 'Pack size 2', 'Serving size 2', 'Servings per pack 2', 'Product code 2', 'Energy per 100g (or 100ml) 2', 'Protein per 100g (or 100ml) 2', 'Total fat per 100g (or 100ml) 2', 'Saturated fat per 100g (or 100ml) 2', 'Carbohydrate per 100g (or 100ml) 2', 'Sugars per 100g (or 100ml) 2', 'Sodium per 100g (or 100ml) 2', 'Original Price 2', 'Price Promoted 2', 'Price Promoted Price 2', 'Multi Buy Special 2', 'Multi Buy Special Details 2', 'Multi Buy Price 2', 'UID 2' ]
        mW = csv.DictWriter(cM, fieldnames=fM)
        mW.writeheader()

    #clear previous unmatched items
    with open(simPath + 'unmatchedItems.csv', 'w+', newline='') as cUM:
        fUM = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
        umW = csv.DictWriter(cUM, fieldnames=fUM)
        umW.writeheader()    

    simMatrix = np.zeros(shape=(len(first), len(second)), dtype=float)
    
    levS = np.genfromtxt(simPath + 'LEVn.csv', delimiter=',')
    levSim = np.multiply(levS, wLev)
    simMatrix += levSim
    levSim = None #release memory 

    nameS = np.genfromtxt(simPath + 'NAMEn.csv', delimiter=',')
    nameSim = np.multiply(nameS, wName)
    simMatrix += nameSim
    nameSim = None

    hamS = np.genfromtxt(simPath + 'HAMn.csv', delimiter=',')
    hamSim = np.multiply(hamS, wHam)
    simMatrix += hamSim
    hamSim = None
    
    jwinkS = np.genfromtxt(simPath + 'JWINKn.csv', delimiter=',')
    jwinkSim = np.multiply(jwinkS, wJWink)
    simMatrix += jwinkSim
    jwinkSim = None
    
    np.savetxt(simPath+'simMat.csv', simMatrix, delimiter=",")
    
    print(" --- Similarity matrix created ---")
    
    print(" --- Generating recommendations ---")
    
    swMat = np.copy(simMatrix)

    matches = [] #arraye to keep all the similar pairs as tuples of [(first, second)...]
    getch = ''

    #read first batch of indices 
    indices =  np.argpartition(swMat.flatten(), -50)[-50:]
    indices = np.vstack(np.unravel_index(indices, swMat.shape)).T
    
    while (swMat[indices[0][0]][indices[0][1]] >= 2):
        #print(swMat[indices[0][0]][indices[0][1]])
        for i in range(0,len(indices)):
            print(" ")
            if (swMat[indices[i][0]][indices[i][1]] > 0): #if the item is not already matched in current batch
                print(first[indices[i][0]]['Brand'] + " - " +  first[indices[i][0]]['Product name'] + " - " + first[indices[i][0]]['Pack size'] +
                        " <===> " + 
                        second[indices[i][1]]['Brand'] + " - " +  second[indices[i][1]]['Product name'] + " - " + second[indices[i][1]]['Pack size'])# + " -- similarity is %s :" % swMat[indices[i][0]][indices[i][1]])
                
                print ('Is this recommendation true (y|n)?')
                getch = rc.readchar()

                while not (getch == b'y' or getch == b'Y' or getch == b'n' or getch == b'N' or getch == b'q' or getch == b'Q'):
                    print('Invalid input, sorry! - please answer by n or y')
                    getch = rc.readchar()
                
                if (getch == b'y' or getch == b'Y'):
                    #remove the items from simMatrix
                    swMat[indices[i][0], :] = -1.0   
                    swMat[:, indices[i][1]] = -1.0
                    #save the match
                    matches.append((first[indices[i][0]], second[indices[i][1]]))                    
                    #penalise/promote the recommenders
                    #haming's avg = 0.58 and median = 0.6
                    if (hamS[indices[i][0]][indices[i][1]] >= 0.6):#correctly recommended (use original similarity matrix before applying weights)
                        wHam += 0.0001 #promote
                    else:
                        wHam -= 0.0001 #penalise
                    
                    #jwink avg = 0.0143 median = 0.0137
                    if (jwinkS[indices[i][0]][indices[i][1]] >= 0.0137):#correctly recommended 
                        wJWink += 0.0001 #promote
                    else:
                        wJWink -= 0.0001 #penalise

                    #lve avg = 0.560 median = 0.582
                    if (levS[indices[i][0]][indices[i][1]] >= 0.582):#correctly recommended 
                        wLev += 0.0001 #promote
                    else:
                        wLev -= 0.0001 #penalise
                    
                    #name avg = 0.017 median = 0
                    if (nameS[indices[i][0]][indices[i][1]] > 0):#correctly recommended 
                        wName += 0.0001 #promote
                    else:
                        wName -= 0.0001 #penalise
                
                elif (getch == b'n' or getch == b'N'):
                    #void that similarity calculation
                    swMat[indices[i][0], indices[i][1]] = -1  
                    #penalise/promote the recommenders
                    #haming's avg = 0.58 and median = 0.6
                    if (hamS[indices[i][0]][indices[i][1]] < 0.6):#correctly not recommended (use original similarity matrix before applying weights)
                        wHam += 0.0001 #promote
                    else:
                        wHam -= 0.0001 #penalise
                    
                    #jwink avg = 0.0143 median = 0.0137
                    if (jwinkS[indices[i][0]][indices[i][1]] < 0.0137):#correctly not recommended 
                        wJWink += 0.0001 #promote
                    else:
                        wJWink -= 0.0001 #penalise

                    #lve avg = 0.560 median = 0.582
                    if (levS[indices[i][0]][indices[i][1]] < 0.582):#correctly not recommended 
                        wLev += 0.0001 #promote
                    else:
                        wLev -= 0.0001 #penalise
                    
                    #name avg = 0.017 median = 0
                    if (nameS[indices[i][0]][indices[i][1]] == 0):#correctly not recommended 
                        wName += 0.0001 #promote
                    else:
                        wName -= 0.0001 #penalise

                elif (getch == b'q' or getch == b'Q'):
                    break

        print(" --- Saving results... ---\n")
        print(" * While I am saving the results so far...")
        print(" * Did you know ...")
        print(" * "+getFunFact(funfactIndex, funfacts))
        funfactIndex += 1
        if funfactIndex >= len(funfacts):
            funfactIndex = 0
        print()
        time.sleep(3)

        np.savetxt(simPath + 'swMatTest.csv', swMat, delimiter=",")
       
        #save new weights
        with open(weights, 'w', newline='') as csvfile:
            fieldnames = ['levenshtein', 'name', 'jwink', 'hamming']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'levenshtein': wLev, 'name': wName, 'jwink': wJWink, 'hamming': wHam})
        
        #save matches
        with open(simPath + 'Matches.csv', 'a', newline='') as csvMatches:
            fieldnamesMatch = ['Date of data Extraction 1', 'Brand 1', 'Product name 1', 'Category 1', 'Pack size 1', 'Serving size 1', 'Servings per pack 1', 'Product code 1', 'Energy per 100g (or 100ml) 1', 'Protein per 100g (or 100ml) 1', 'Total fat per 100g (or 100ml) 1', 'Saturated fat per 100g (or 100ml) 1', 'Carbohydrate per 100g (or 100ml) 1', 'Sugars per 100g (or 100ml) 1', 'Sodium per 100g (or 100ml) 1', 'Original Price 1', 'Price Promoted 1', 'Price Promoted Price 1', 'Multi Buy Special 1', 'Multi Buy Special Details 1', 'Multi Buy Price 1', 'UID 1',
                               'Date of data Extraction 2', 'Brand 2', 'Product name 2', 'Category 2', 'Pack size 2', 'Serving size 2', 'Servings per pack 2', 'Product code 2', 'Energy per 100g (or 100ml) 2', 'Protein per 100g (or 100ml) 2', 'Total fat per 100g (or 100ml) 2', 'Saturated fat per 100g (or 100ml) 2', 'Carbohydrate per 100g (or 100ml) 2', 'Sugars per 100g (or 100ml) 2', 'Sodium per 100g (or 100ml) 2', 'Original Price 2', 'Price Promoted 2', 'Price Promoted Price 2', 'Multi Buy Special 2', 'Multi Buy Special Details 2', 'Multi Buy Price 2', 'UID 2' ]
            matchWriter = csv.DictWriter(csvMatches, fieldnames=fieldnamesMatch)

            for m in matches:
                matchWriter.writerow({'Date of data Extraction 1': m[0]['Date of data Extraction'],
                                    'Brand 1': m[0]['Brand'], 
                                    'Product name 1': m[0]['Product name'], 
                                    'Category 1': m[0]['Category'], 
                                    'Pack size 1': m[0]['Pack size'], 
                                    'Serving size 1': m[0]['Serving size'], 
                                    'Servings per pack 1': m[0][ 'Servings per pack'], 
                                    'Product code 1': m[0]['Product code'], 
                                    'Energy per 100g (or 100ml) 1': m[0]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml) 1': m[0]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml) 1': m[0]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml) 1': m[0][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml) 1': m[0]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml) 1': m[0]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml) 1': m[0][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price 1': m[0]['Original Price'], 
                                    'Price Promoted 1': m[0]['Price Promoted'], 
                                    'Price Promoted Price 1': m[0]['Price Promoted Price'], 
                                    'Multi Buy Special 1': m[0]['Multi Buy Special'], 
                                    'Multi Buy Special Details 1': m[0][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price 1': m[0]['Multi Buy Price'], 
                                    'UID 1': m[0]['UID'],
                                    'Date of data Extraction 2': m[1]['Date of data Extraction'],
                                    'Brand 2': m[1]['Brand'], 
                                    'Product name 2': m[1]['Product name'], 
                                    'Category 2': m[1]['Category'], 
                                    'Pack size 2': m[1]['Pack size'], 
                                    'Serving size 2': m[1]['Serving size'], 
                                    'Servings per pack 2': m[1][ 'Servings per pack'], 
                                    'Product code 2': m[1]['Product code'], 
                                    'Energy per 100g (or 100ml) 2': m[1]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml) 2': m[1]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml) 2': m[1]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml) 2': m[1][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml) 2': m[1]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml) 2': m[1]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml) 2': m[1][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price 2': m[1]['Original Price'], 
                                    'Price Promoted 2': m[1]['Price Promoted'], 
                                    'Price Promoted Price 2': m[1]['Price Promoted Price'], 
                                    'Multi Buy Special 2': m[1]['Multi Buy Special'], 
                                    'Multi Buy Special Details 2': m[1][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price 2': m[1]['Multi Buy Price'], 
                                    'UID 2': m[1]['UID']})


        if (getch == b'q' or getch == b'Q'):
            break

        #read new set of indexes
        indices =  np.argpartition(swMat.flatten(), -50)[-50:]
        indices = np.vstack(np.unravel_index(indices, swMat.shape)).T
    #end of recommendation process

    #process remaining unmatched items
    if (getch == b'q' or getch == b'Q'):
        print(" --- Process interrupted ---")
    else:
        print(" --- No more similar items with similarity more than 1.5 found ---")
        print(" --- Processing remainig items ---")
        #list all unmatched items
        with open(simPath + 'unmatchedItems.csv', 'a', newline='') as csvUMatches:
            fieldnamesUMatch = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
            unmatchWriter = csv.DictWriter(csvUMatches, fieldnames=fieldnamesUMatch)

            for i in tqdm(range(0,np.size(swMat,0))): #process rows -> first[]
                if (np.argmax(swMat[i,:]) > 0): #row has not been assigned
                    #print(first[i])
                    unmatchWriter.writerow({'Date of data Extraction': first[i]['Date of data Extraction'],
                                    'Brand': first[i]['Brand'], 
                                    'Product name': first[i]['Product name'], 
                                    'Category': first[i]['Category'], 
                                    'Pack size': first[i]['Pack size'], 
                                    'Serving size': first[i]['Serving size'], 
                                    'Servings per pack': first[i][ 'Servings per pack'], 
                                    'Product code': first[i]['Product code'], 
                                    'Energy per 100g (or 100ml)': first[i]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml)': first[i]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml)': first[i]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml)': first[i][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml)': first[i]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml)': first[i]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml)': first[i][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price': first[i]['Original Price'], 
                                    'Price Promoted': first[i]['Price Promoted'], 
                                    'Price Promoted Price': first[i]['Price Promoted Price'], 
                                    'Multi Buy Special': first[i]['Multi Buy Special'], 
                                    'Multi Buy Special Details': first[i][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price': first[i]['Multi Buy Price'], 
                                    'UID': first[i]['UID']})

            for j in tqdm(range(0,np.size(swMat,1))): #process columns -> second[]
                if (np.argmax(swMat[:,j]) > 0): #column has not been assigned
                    #print(second[j])
                    unmatchWriter.writerow({'Date of data Extraction': second[j]['Date of data Extraction'],
                                    'Brand': second[j]['Brand'], 
                                    'Product name': second[j]['Product name'], 
                                    'Category': second[j]['Category'], 
                                    'Pack size': second[j]['Pack size'], 
                                    'Serving size': second[j]['Serving size'], 
                                    'Servings per pack': second[j][ 'Servings per pack'], 
                                    'Product code': second[j]['Product code'], 
                                    'Energy per 100g (or 100ml)': second[j]['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml)': second[j]['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml)': second[j]['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml)': second[j][ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml)': second[j]['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml)': second[j]['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml)': second[j][ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price': second[j]['Original Price'], 
                                    'Price Promoted': second[j]['Price Promoted'], 
                                    'Price Promoted Price': second[j]['Price Promoted Price'], 
                                    'Multi Buy Special': second[j]['Multi Buy Special'], 
                                    'Multi Buy Special Details': second[j][ 'Multi Buy Special Details'], 
                                    'Multi Buy Price': second[j]['Multi Buy Price'], 
                                    'UID': second[j]['UID']})

    print(" --- Process complete ---")

    #### this was for top three items per row 
    #top3 = np.zeros(shape=(len(first),3), dtype=int)
    #for i in tqdm(range(0,len(first))):
    #    top3[i] = np.argsort(simMatrix[i,:])[-3:][::-1]
    #np.savetxt(simPath+'top3.csv', top3, delimiter=",")

#end of findSimilarItems


