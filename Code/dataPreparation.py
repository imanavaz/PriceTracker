import csv
import time
import datetime


#partiotion large data items based on the given category (i.e. extract that category and save in new file)
#note that this one processes +0000 and UTC differently than append ID -> needs to be fixed. 
def partitionData(inputCSV, outputCSV, category):
    with open(inputCSV,'r') as csvinput:
        with open(outputCSV, 'w', newline='') as csvoutput:
            fUM = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Category2', 'Category3', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Ingredients', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
            writer = csv.DictWriter(csvoutput, fieldnames=fUM)
            writer.writeheader()   
            
            pData = []
            reader = csv.DictReader(csvinput, delimiter=',') 

            for row in reader: # each row is a list
                if (row['Category'] == category):
                    pData.append(row)

            for m in pData:       
                if "+0000" in m['Date of data Extraction']: #check and bring all back to UTC
                    m['Date of data Extraction'].replace("+0000", "UTC")

                writer.writerow({'Date of data Extraction': m['Date of data Extraction'],
                                    'Brand': m['Brand'], 
                                    'Product name': m['Product name'], 
                                    'Category': m['Category'], 
                                    'Category2': m['Category2'], 
                                    'Category3': m['Category3'], 
                                    'Pack size': m['Pack size'], 
                                    'Serving size': m['Serving size'], 
                                    'Servings per pack': m[ 'Servings per pack'], 
                                    'Product code': m['Product code'],
                                    'Ingredients': m['Ingredients'],
                                    'Energy per 100g (or 100ml)': m['Energy per 100g (or 100ml)'], 
                                    'Protein per 100g (or 100ml)': m['Protein per 100g (or 100ml)'], 
                                    'Total fat per 100g (or 100ml)': m['Total fat per 100g (or 100ml)'], 
                                    'Saturated fat per 100g (or 100ml)': m[ 'Saturated fat per 100g (or 100ml)'], 
                                    'Carbohydrate per 100g (or 100ml)': m['Carbohydrate per 100g (or 100ml)'], 
                                    'Sugars per 100g (or 100ml)': m['Sugars per 100g (or 100ml)'], 
                                    'Sodium per 100g (or 100ml)': m[ 'Sodium per 100g (or 100ml)'], 
                                    'Original Price': m['Original Price'], 
                                    'Price Promoted': m['Price Promoted'], 
                                    'Price Promoted Price': m['Price Promoted Price'], 
                                    'Multi Buy Special': m['Multi Buy Special'], 
                                    'Multi Buy Special Details': m[ 'Multi Buy Special Details'], 
                                    'Multi Buy Price': m['Multi Buy Price'], 
                                    'UID': m['UID']}) 

    print(" --- Data partitioning complete on %s ---" % outputCSV)
#end of partitionData


#this function will append a unique ID to each row, reading the timestamp of each row, and adding a number to it.
#This is how it is used: append ID to coles
#appendIDtoRow('coles.csv', 'coles2.csv','C') #these would be the files with unique IDs
def appendIDtoRow (inputCSV, outputCSV, supermarketIndicator):
    with open(inputCSV, 'r', encoding="utf-8") as csvinput:
        with open(outputCSV, 'w', encoding="utf-8") as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append('UID')
            all.append(row)

            count = 1

            for row in reader:
                #print(row[0])
                if row[0] != "":
                    rdate = ""
                    if ("UTC" in row[0]):
                        rdate = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S %Z")#"%Y-%m-%d %H:%M:%S %Z") #%z for +0000 %Z for UTC
                    elif ("+0" in row[0]):
                        rdate = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S %z")#"%Y-%m-%d %H:%M:%S %Z") #%z for +0000 %Z for UTC
                    unixtime = time.mktime(rdate.timetuple())
                    newid = str(unixtime)+"-"+ supermarketIndicator +"-"+str(count)
                    count = count + 1
                    row.append(newid)
                    all.append(row)

            writer.writerows(all)

        csvoutput.close()
    return True
#end of appendIDtoRow

if __name__ == '__main__':
    #appendIDtoRow('C:/Users/avaz/OneDrive - Deakin University/Projects/Price Tracker/Data/RData/20200302-coles-export-test.csv', 'C:/Users/avaz/OneDrive - Deakin University/Projects/Price Tracker/Data/RData/test.csv', 'W')
    pass
    