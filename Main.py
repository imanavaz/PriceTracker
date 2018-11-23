
import csv
#from logic.levenshtein import iterative_levenshtein
from logic.dataPreparation import *
#from logic.preparations import processFile
from logic.generateSimilarities import *
from logic.processSimilarityMatrix import *
import os



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
#appendIDtoRow ('data/c-2.csv', 'data/c-2-i.csv', 'C')
#appendIDtoRow ('data/w-2.csv', 'data/w-2-i.csv', 'W')


#WITH TRAINING SECTION
#generateSimialrityMatrices('data/c-i-Bread-A-Bakery.csv', 'data/w-i-Bakery-cc.csv', 'res/Bread-A-Bakery/')
#print("\n\n --- Starting process for %s ---" % "Bread & Bakery")
#createSimMatrix ('weights.csv', 'res/Bread-A-Bakery/')
#processSimilarItemsWithTraining('data/c-i-Bread-A-Bakery.csv', 'data/w-i-Bakery-cc.csv', 'weights.csv', 'res/Bread-A-Bakery/', funfacts, 55)

#print("\n\n --- Starting process for %s ---" % "Dairy, Eggs & Meals")
#createSimMatrix ('weights.csv', 'res/Dairy-Eggs-A-Meals/')
#processSimilarItemsWithTraining('data/c-i-Dairy-Eggs-A-Meals.csv', 'data/w-i-Dairy-Eggs-A-Fridge.csv', 'weights.csv', 'res/Dairy-Eggs-A-Meals/', funfacts, 1)

#print("\n\n --- Starting process for %s ---" % "Drinks")
#createSimMatrix ('weights.csv', 'res/Drinks/')
#processSimilarItemsWithTraining('data/c-i-Drinks.csv', 'data/w-i-Drinks.csv', 'weights.csv', 'res/Drinks/', funfacts, 45)

#print("\n\n --- Starting process for %s ---" % "Frozen")
#createSimMatrix ('weights.csv', 'res/Frozen/')
#processSimilarItemsWithTraining('data/c-i-Frozen.csv', 'data/w-i-Freezer.csv', 'weights.csv', 'res/Frozen/', funfacts, 15)

#print("\n\n --- Starting process for %s ---" % "Fruit & Vegetables")
#createSimMatrix ('weights.csv', 'res/Fruit-A-Vegetables/')
#processSimilarItemsWithTraining('data/c-i-Fruit-A-Vegetables.csv', 'data/w-i-Fruit-A-Veg.csv', 'weights.csv', 'res/Fruit-A-Vegetables/', funfacts, 20)

#print("\n\n --- Starting process for %s ---" % "Meat, Seafood & Deli")
#createSimMatrix ('weights.csv', 'res/Meat-Seafood-A-Deli/')
#processSimilarItemsWithTraining('data/c-i-Meat-Seafood-A-Deli.csv', 'data/w-i-Meat-Seafood-A-Deli.csv', 'weights.csv', 'res/Meat-Seafood-A-Deli/', funfacts, 8)

#print("\n\n --- Starting process for %s ---" % "Baby")
#createSimMatrix ('weights.csv', 'res/Baby/')
#processSimilarItemsWithTraining('data/c-i-Baby.csv', 'data/w-i-Baby.csv', 'weights.csv', 'res/Baby/', funfacts, 30)


#NO TRAINING SECTION 
#print("\n\n *** Processing the following three categories will take some time ***")
#print(" *** Please be patient ****")
#print("\n\n --- Starting process for %s ---" % "Liquor")
#createSimMatrix ('weights.csv', 'res/Liquor/')
#processSimilarItemsNoTraining('data/c-i-Liquor.csv', 'data/w-i-Liquor.csv', 'res/Liquor/', funfacts, 12)

#print("\n\n --- Starting process for %s ---" % "Pantry")
#createSimMatrix ('weights.csv', 'res/Pantry/')
#processSimilarItemsNoTraining('data/c-i-Pantry.csv', 'data/w-i-Pantry.csv', 'res/Pantry/', funfacts, 20)

#print("\n\n --- Starting process for %s ---" % "Lunch Box")
#createSimMatrix ('weights.csv', 'res/Lunch-Box/')
#processSimilarItemsNoTraining('data/c-i.csv', 'data/w-i-Lunch-Box.csv', 'res/Lunch-Box/', funfacts, 60)




##---------------------------------------##
# -------- (-:, CSV Process :-) --------- #
##---------------------------------------##

#data partitioning by categories
partitionData('data/c-2-i.csv', 'data/c-2-i-Pantry.csv', 'Pantry')
partitionData('data/c-2-i.csv', 'data/c-2-i-Baby.csv', 'Baby')
partitionData('data/c-2-i.csv', 'data/c-2-i-Bread-A-Bakery.csv', 'Bread & Bakery')
partitionData('data/c-2-i.csv', 'data/c-2-i-Dairy-Eggs-A-Meals.csv', 'Dairy, Eggs & Meals')
partitionData('data/c-2-i.csv', 'data/c-2-i-Drinks.csv', 'Drinks')
partitionData('data/c-2-i.csv', 'data/c-2-i-Frozen.csv', 'Frozen')
partitionData('data/c-2-i.csv', 'data/c-2-i-Fruit-A-Vegetables.csv', 'Fruit & Vegetables')
partitionData('data/c-2-i.csv', 'data/c-2-i-Liquor.csv', 'Liquor')
partitionData('data/c-2-i.csv', 'data/c-2-i-Meat-Seafood-A-Deli.csv', 'Meat, Seafood & Deli')

partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Baby.csv', 'Baby')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Bakery.csv', 'Bakery')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Dairy-Eggs-A-Fridge.csv', 'Dairy, Eggs & Fridge')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Drinks.csv', 'Drinks')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Freezer.csv', 'Freezer')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Fruit-A-Veg.csv', 'Fruit & Veg')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Liquor.csv', 'Liquor')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Lunch-Box.csv', 'Lunch Box')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Meat-Seafood-A-Deli.csv', 'Meat, Seafood & Deli')
partitionData('data/w-2-i-cc.csv', 'data/w-2-i-Pantry.csv', 'Pantry')

