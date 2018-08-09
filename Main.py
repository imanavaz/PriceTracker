
import csv
from logic.levenshtein import iterative_levenshtein
from logic.appendID import appendIDtoRow
from logic.preparations import processFile

##---------------------------------------##
# --------- (-: CSV Process :-) --------- #
##---------------------------------------##

#append ID to coles
#appendIDtoRow('coles.csv', 'coles2.csv','C') #these would be the files with unique IDs
#appendIDtoRow('data\woolworth.csv', 'woolworth2.csv','W')

processFile('coles2.csv','colesInfo2.csv')

###-----Woolies-----###
countW = 0
wooliesfile = open("woolworth2.csv", "r")#data\woolworth.csv') 
wooliesDataReader = csv.DictReader(wooliesfile)
#wooliesDataReader = csv.reader(wooliesfile, delimiter=',', quotechar='|')

###-----Coles-----###
countC = 0
#colesfile = open("coles2.csv", "r")#data\coles.csv')
#colesDataReader = csv.DictReader(colesfile)



###----Comparison----###
#for rowC in colesDataReader:
#    for rowW in wooliesDataReader:
#        #print(rowC['Brand'] + " vs. " + rowW['Brand'])
#        if (iterative_levenshtein(str.lower(str.lstrip(rowC['Brand'])), str.lower(str.lstrip(rowW['Brand'])), costs=(1, 1, 1)) == 0):
#            print('LD for '+rowW['Brand']+' and '+rowC['Brand']+" is Zero!")
#    wooliesfile.seek(0)

wooliesfile.close()
#colesfile.close()

#print('total number of records in Woolies :',countW)
#print('total number of records in Coles :',countC )



