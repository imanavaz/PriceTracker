
import csv
#from logic.levenshtein import iterative_levenshtein
from logic.dataPreparation import *
#from logic.preparations import processFile
from logic.generateSimilarities import *
from logic.processSimilarityMatrix import *
import os
#from tkinter import *


#clear terminal 
os.system('cls' if os.name == 'nt' else 'clear')

#generateSimialrityMatrices('data/c-i-Meat-Seafood-A-Deli.csv', 'data/w-i-Meat-Seafood-A-Deli.csv', 'res/Meat-Seafood-A-Deli/')
#generateSimialrityMatrices('data/c-i-Pantry.csv', 'data/w-i-Pantry.csv', 'res/Pantry/')
#generateSimialrityMatrices('data/c-i.csv', 'data/w-i-Lunch-Box.csv', 'res/Lunch-Box/')

#for user experience 
funfactidx = 0
funfacts = []
loadFunFacts(funfacts)

##needed only once
#appendIDtoRow ('data/c.csv', 'data/c-i.csv', 'C')
#appendIDtoRow ('data/w.csv', 'data/w-i.csv', 'W')

#read scrapped data 
first = []
with open('data/c-i.csv','r') as csvinput1:
    reader1 = csv.DictReader(csvinput1, delimiter=',') 
    for row in reader1: # each row is a list
        first.append(row)

second = []
with open('data/w-i.csv','r') as csvinput2:
    reader2 = csv.DictReader(csvinput2, delimiter=',') 
    for row in reader2: # each row is a list
        second.append(row)


#WITH TRAINING SECTION
#createSimMatrix ('weights.csv', 'res/Baby/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Baby/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Bread-A-Bakery/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Bread-A-Bakery/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Dairy-Eggs-A-Meals/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Dairy-Eggs-A-Meals/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Drinks/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Drinks/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Frozen/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Frozen/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Fruit-A-Vegetables/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Fruit-A-Vegetables/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Meat-Seafood-A-Deli/')
#processSimilarItemsWithTraining(first, second, 'weights.csv', 'res/Meat-Seafood-A-Deli', funfacts, funfactidx)




#NO TRAINING SECTION 
#createSimMatrix ('weights.csv', 'res/Liquor/')
#processSimilarItemsNoTraining(first, second, 'res/Liquor/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Pantry/')
#processSimilarItemsNoTraining(first, second, 'res/Pantry/', funfacts, funfactidx)

#createSimMatrix ('weights.csv', 'res/Lunch-Box/')
#processSimilarItemsNoTraining(first, second, 'res/Lunch-Box/', funfacts, funfactidx)



## for the TKinker 
#root = Tk()
#recl = ['test 1', 'test 2', 'test 3']
#gui = AppGUI(recl, root)
##rec3.setRecommendationText("rec 3 hurray")
#root.mainloop()


#def test(option):
#    print option
#for indx, option in enumerate(things):
#    cmd = lambda opt=option: test(opt)
#    btn = Tkinter.Button(text=option, command=cmd)
#    btn.pack(side='left')

#frame = Frame(root, width=600, height=550)
#frame.bind("<Button-1>",leftClick)
#frame.bind("<Button-3>",rightClick) #
#frame.pack()





##---------------------------------------##
# --------- (-:, CSV Process :-) --------- #
##---------------------------------------##

#data partitioning by categories
"""partitionData('data/c-i.csv', 'data/c-i-Pantry.csv', 'Pantry')
partitionData('data/c-i.csv', 'data/c-i-Baby.csv', 'Baby')
partitionData('data/c-i.csv', 'data/c-i-Bread-A-Bakery.csv', 'Bread & Bakery')
partitionData('data/c-i.csv', 'data/c-i-Dairy-Eggs-A-Meals.csv', 'Dairy, Eggs & Meals')
partitionData('data/c-i.csv', 'data/c-i-Drinks.csv', 'Drinks')
partitionData('data/c-i.csv', 'data/c-i-Frozen.csv', 'Frozen')
partitionData('data/c-i.csv', 'data/c-i-Fruit-A-Vegetables.csv', 'Fruit & Vegetables')
partitionData('data/c-i.csv', 'data/c-i-Liquor.csv', 'Liquor')
partitionData('data/c-i.csv', 'data/c-i-Meat-Seafood-A-Deli.csv', 'Meat, Seafood & Deli')"""

"""partitionData('data/w-i.csv', 'data/w-i-Baby.csv', 'Baby')
partitionData('data/w-i.csv', 'data/w-i-Bakery.csv', 'Bakery')
partitionData('data/w-i.csv', 'data/w-i-Dairy-Eggs-A-Fridge.csv', 'Dairy, Eggs & Fridge')
partitionData('data/w-i.csv', 'data/w-i-Drinks.csv', 'Drinks')
partitionData('data/w-i.csv', 'data/w-i-Freezer.csv', 'Freezer')
partitionData('data/w-i.csv', 'data/w-i-Fruit-A-Veg.csv', 'Fruit & Veg')
partitionData('data/w-i.csv', 'data/w-i-Liquor.csv', 'Liquor')
partitionData('data/w-i.csv', 'data/w-i-Lunch-Box.csv', 'Lunch Box')
partitionData('data/w-i.csv', 'data/w-i-Meat-Seafood-A-Deli.csv', 'Meat, Seafood & Deli')
partitionData('data/w-i.csv', 'data/w-i-Pantry.csv', 'Pantry')"""




#######extractSimilarData('data\c.csv', 'data\w.csv')

#processFile('coles2.csv','colesInfo2.csv')

###-----Woolies-----###
#countW = 0
#wooliesfile = open("woolworth2.csv", "r")#data\woolworth.csv') 
#wooliesDataReader = csv.DictReader(wooliesfile)
#wooliesDataReader = csv.reader(wooliesfile, delimiter=',', quotechar='|')

###-----Coles-----###
#countC = 0
#colesfile = open("coles2.csv", "r")#data\coles.csv')
#colesDataReader = csv.DictReader(colesfile)



###----Comparison----###
#for rowC in colesDataReader:
#    for rowW in wooliesDataReader:
#        #print(rowC['Brand'] + " vs. " + rowW['Brand'])
#        if (iterative_levenshtein(str.lower(str.lstrip(rowC['Brand'])), str.lower(str.lstrip(rowW['Brand'])), costs=(1, 1, 1)) == 0):
#            print('LD for '+rowW['Brand']+' and '+rowC['Brand']+" is Zero!")
#    wooliesfile.seek(0)

#wooliesfile.close()
#colesfile.close()

#print('total number of records in Woolies :',countW)
#print('total number of records in Coles :',countC )



