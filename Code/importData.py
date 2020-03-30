from tqdm import tqdm
import datetime
import csv
from connx import *
 
def importNewProductData(inputFile, testRun=True):
    
    #read scrapped data 
    products = []
    with open(inputFile,'r') as csvInput:
        reader = csv.DictReader(csvInput, delimiter=',') 
        for row in reader: # each row is a list
            products.append(row)


        conn = None

        try:

            conn = connectDB()
            
            if conn == None:
                print('Failed to connect to DB in importProductData(..)...!')
                raise Exception('Failed to connect')

            # create a cursor
            cur = conn.cursor(buffered=True)

            print("====== Processing New Product Import ======")

            for i in tqdm(range(0,len(products))): 
                #print(products[i])
                #preparesqp query
                sql = None
                sql = 'INSERT INTO product(UID, Source, Date_of_insertion, Date_of_data_extraction, Brand, Product_name, Category, Pack_size, Serving_size, Servings_per_Pack, Product_code, Energy_per_100g_or_100ml, Protein_per_100g_or_100ml, Total_fat_per_100g_or_100ml, Saturated_fat_per_100g_or_100ml, Carbohydrate_per_100g_or_100ml, Sugars_per_100g_or_100ml, Sodium_per_100g_or_100ml, Price_at_insertion) VALUES ('
                sql += '\'' + products[i]['UID'] + '\','
                
                #decide source
                source = ''
                if "-C-" in products[i]['UID']:
                    source = '\'Coles\''
                elif "-W-" in products[i]['UID']:
                    source = '\'Woolworth\''
                sql += source + ','
                
                t = datetime.datetime.now(datetime.timezone.utc)
                ts = t.strftime('%Y-%m-%d %H:%M:%S')
                sql += 'STR_TO_DATE(\'' + ts + '\', \'%Y-%m-%d %H:%i:%s\'),'
                dateOfEx = products[i]['Date of data Extraction']
                dateOfEx = dateOfEx.replace(' UTC', '')
                #print('in 2: ' + dateOfEx)
                sql += 'STR_TO_DATE(\'' +dateOfEx + '\', \'%Y-%m-%d %H:%i:%s\'),'
                sql += '\'' + (products[i]['Brand'].replace('\'', '\'\'') if '\'' in products[i]['Brand'] else products[i]['Brand']) + '\','
                sql += '\'' + (products[i]['Product name'].replace('\'', '\'\'') if '\'' in products[i]['Product name'] else products[i]['Product name']) + '\','
                sql += '\'' + products[i]['Category'] + '\','
                sql += '\'' + products[i]['Pack size'] + '\','
                sql += '\'' + products[i]['Serving size'] + '\','
                sql += '\'' + products[i]['Servings per pack'] + '\','
                sql += '\'' + products[i]['Product code'] + '\','
                sql += '\'' + products[i]['Energy per 100g (or 100ml)'] + '\','
                sql += '\'' + products[i]['Protein per 100g (or 100ml)'] + '\','
                sql += '\'' + products[i]['Total fat per 100g (or 100ml)'] + '\','
                sql += '\'' + products[i]['Saturated fat per 100g (or 100ml)'] + '\','
                sql += '\'' + products[i]['Carbohydrate per 100g (or 100ml)'] + '\','
                sql += '\'' + products[i]['Sugars per 100g (or 100ml)'] + '\','
                sql += '\'' + products[i]['Sodium per 100g (or 100ml)'] + '\','
                sql += products[i]['Original Price'] 
                sql += ');'
                #print('====== Product SQL ======')
                #print (sql)
                cur.execute(sql)

                sqlPrice = 'INSERT INTO price(UID, Price_Date, Original_Price, Price_Promoted, Price_Promoted_Price, Multi_Buy_Special, Multi_Buy_Special_Details, Multi_Buy_Special_Price) VALUES ('
                
                sqlPrice += '\'' + products[i]['UID'] + '\','
                dateOfEx = products[i]['Date of data Extraction']
                dateOfEx = dateOfEx.replace(' UTC', '')
                #print('in 3: ' + dateOfEx)
                sqlPrice += 'STR_TO_DATE(\'' +dateOfEx + '\',\'%Y-%m-%d %H:%i:%s\'),'
                sqlPrice += products[i]['Original Price'] + ',' 
                pp = '0'
                if products[i]['Price Promoted'] == 'TRUE':
                    pp = '1'
                sqlPrice += pp + ',' 
                ppPrice = '0'
                if (products[i]['Price Promoted Price'] is None or products[i]['Price Promoted Price']==' ' or products[i]['Price Promoted Price']==''):
                    ppPrice = '0.0'
                else:
                    ppPrice = products[i]['Price Promoted Price']
                sqlPrice += ppPrice + ',' 
                mbs = '0'
                if products[i]['Multi Buy Special'] == 'TRUE':
                    mbs = '1'
                sqlPrice += mbs + ',' 
                sqlPrice += '\'' + products[i]['Multi Buy Special Details'] + '\',' 
                
                if (products[i]['Multi Buy Price'] is None or products[i]['Multi Buy Price']==' ' or products[i]['Multi Buy Price']==''):
                    mbPrice = '0.0'
                else:
                    mbPrice = products[i]['Multi Buy Price']
                sqlPrice += mbPrice 
                sqlPrice += ');'
                #print('====== Price SQL ======')
                #print (sqlPrice)
                cur.execute(sqlPrice)

            if testRun != True:    
                conn.commit()
                
            # close the cursor 
            cur.close()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(conn)
        #finally:
        #    if conn is not None:
        #        disconnectDB(conn)
        #        print('Database connection closed.')
    return True
 

def importMatches(matchesFile, testRun=True):
    
    #read matches data
    matches = []
    with open(matchesFile,'r') as csvMatches:
        mreader = csv.DictReader(csvMatches, delimiter=',') 
        for row in mreader: # each row is a list
            matches.append(row)

        conn = None

        try:

            conn = connectDB()
            
            if conn == None:
                print('Failed to connect to DB in importMatches(..)...!')
                raise Exception('Failed to connect')

            # create a cursor
            cur = conn.cursor()

            print('====== Processing Matched Items ======')
            #put new items in a separate files to be inserted 
            pTime = datetime.datetime.now(datetime.timezone.utc)
            pTimeStr = pTime.strftime('%Y-%m-%d-%H-%M-%S')
            pItemsFileName = 'newMatches-' + pTimeStr + '.csv'

            with open(pItemsFileName, 'w+', newline='') as mcsvfile:
                fUM = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
                mFile = csv.DictWriter(mcsvfile, fieldnames=fUM)
                mFile.writeheader()   


                for i in tqdm(range(0,len(matches))): 
                    #print(matches[i])
                    #preparesqp query
                    sql = None
                    sql = 'INSERT INTO matches(UID1, UID2) VALUES (\'' + matches[i]['UID 1'] + '\', \'' + matches[i]['UID 2'] + '\');'
                    #print('====== Match SQL ======')
                    #print (sql)
                    
                    #insert match into db 
                    cur.execute(sql)

                    #Add matches data to file to be inserted in db
                    #needs to separate the rows 
                    mFile.writerow({'Date of data Extraction': matches[i]['Date of data Extraction 1'],
                        'Brand': matches[i]['Brand 1'], 
                        'Product name': matches[i]['Product name 1'], 
                        'Category': matches[i]['Category 1'], 
                        'Pack size': matches[i]['Pack size 1'], 
                        'Serving size': matches[i]['Serving size 1'], 
                        'Servings per pack': matches[i][ 'Servings per pack 1'], 
                        'Product code': matches[i]['Product code 1'], 
                        'Energy per 100g (or 100ml)': matches[i]['Energy per 100g (or 100ml) 1'], 
                        'Protein per 100g (or 100ml)': matches[i]['Protein per 100g (or 100ml) 1'], 
                        'Total fat per 100g (or 100ml)': matches[i]['Total fat per 100g (or 100ml) 1'], 
                        'Saturated fat per 100g (or 100ml)': matches[i][ 'Saturated fat per 100g (or 100ml) 1'], 
                        'Carbohydrate per 100g (or 100ml)': matches[i]['Carbohydrate per 100g (or 100ml) 1'], 
                        'Sugars per 100g (or 100ml)': matches[i]['Sugars per 100g (or 100ml) 1'], 
                        'Sodium per 100g (or 100ml)': matches[i][ 'Sodium per 100g (or 100ml) 1'], 
                        'Original Price': matches[i]['Original Price 1'], 
                        'Price Promoted': matches[i]['Price Promoted 1'], 
                        'Price Promoted Price': matches[i]['Price Promoted Price 1'], 
                        'Multi Buy Special': matches[i]['Multi Buy Special 1'], 
                        'Multi Buy Special Details': matches[i][ 'Multi Buy Special Details 1'], 
                        'Multi Buy Price': matches[i]['Multi Buy Price 1'], 
                        'UID': matches[i]['UID 1']})

                    mFile.writerow({'Date of data Extraction': matches[i]['Date of data Extraction 2'],
                        'Brand': matches[i]['Brand 2'], 
                        'Product name': matches[i]['Product name 2'], 
                        'Category': matches[i]['Category 2'], 
                        'Pack size': matches[i]['Pack size 2'], 
                        'Serving size': matches[i]['Serving size 2'], 
                        'Servings per pack': matches[i][ 'Servings per pack 2'], 
                        'Product code': matches[i]['Product code 2'], 
                        'Energy per 100g (or 100ml)': matches[i]['Energy per 100g (or 100ml) 2'], 
                        'Protein per 100g (or 100ml)': matches[i]['Protein per 100g (or 100ml) 2'], 
                        'Total fat per 100g (or 100ml)': matches[i]['Total fat per 100g (or 100ml) 2'], 
                        'Saturated fat per 100g (or 100ml)': matches[i][ 'Saturated fat per 100g (or 100ml) 2'], 
                        'Carbohydrate per 100g (or 100ml)': matches[i]['Carbohydrate per 100g (or 100ml) 2'], 
                        'Sugars per 100g (or 100ml)': matches[i]['Sugars per 100g (or 100ml) 2'], 
                        'Sodium per 100g (or 100ml)': matches[i][ 'Sodium per 100g (or 100ml) 2'], 
                        'Original Price': matches[i]['Original Price 2'], 
                        'Price Promoted': matches[i]['Price Promoted 2'], 
                        'Price Promoted Price': matches[i]['Price Promoted Price 2'], 
                        'Multi Buy Special': matches[i]['Multi Buy Special 2'], 
                        'Multi Buy Special Details': matches[i][ 'Multi Buy Special Details 2'], 
                        'Multi Buy Price': matches[i]['Multi Buy Price 2'], 
                        'UID': matches[i]['UID 2']})

            
            if testRun != True:    
                conn.commit()
            
            importRecentData(pItemsFileName, testRun)#import recent data from matches to the database 

                
            # close the cursor 
            cur.close()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(conn)
            print('Database connection closed.')
        finally:
            if conn != None:
                disconnectDB(conn)
                print('Database connection closed.')
    return True


def importRecentData(ninputFile, testRun=True):
    
    #read scrapped data 
    products = []
    newProducts = []
    existingProducts = []

    with open(ninputFile,'r') as csvnInput:
        reader = csv.DictReader(csvnInput, delimiter=',') 
        for row in reader: # each row is a list
            products.append(row)

        conn = None

        try:

            conn = connectDB()
            
            if conn == None:
                print('Failed to connect to DB in importProductData(..)...!')
                raise Exception('Failed to connect')

            # create a cursor
            cur = conn.cursor(buffered=True)

            print("====== Processing new data, adding new price and newly introduced items ======")

            for i in tqdm(range(0,len(products))): 
                #print(products[i])
                
                #check if data is available in database 
                sql = None
                sql = 'SELECT UID FROM product WHERE'
                
                #decide source
                source = ''
                if "-C-" in products[i]['UID']:
                    source = '\'Coles\''
                elif "-W-" in products[i]['UID']:
                    source = '\'Woolworth\''
                
                if source == '': #this needs to flag the wrong source 
                    continue  

                sql += ' Source=' 
                sql += source
                
                #sql += ' AND Brand=' 
                #sql += '\'' + (products[i]['Brand'].replace('\'', '\'\'') if '\'' in products[i]['Brand'] else products[i]['Brand']) + '\''
                
                #sql += ' AND Product_name='
                #sql += '\'' + (products[i]['Product name'].replace('\'', '\'\'') if '\'' in products[i]['Product name'] else products[i]['Product name']) + '\''
                
                #sql += ' AND Pack_size='
                #sql += '\'' + products[i]['Pack size'] + '\''

                sql += ' AND Product_code='
                sql += '\'' + products[i]['Product code'] + '\';'
                
                #print('====== Product retrieval SQL ======')
                #print(sql)
                cur.execute(sql)
                res=None
                res = cur.fetchone() 
                

                if res == None: # We have new product
                    newProducts.append(products[i])
                else: #Record the price 
                    existingProducts.append(products[i])
                    #just check in case this is a repeated record
                    dateOfEx = products[i]['Date of data Extraction']
                    dateOfEx = dateOfEx.replace(' UTC', '')
                    #print(dateOfEx)
                    sqlCheckPriceExists = 'SELECT * FROM price WHERE UID=\''+ res[0] + '\' AND Price_Date=STR_TO_DATE(\'' +dateOfEx + '\', \'%Y-%m-%d %H:%i:%s\')'
                    cur.execute(sqlCheckPriceExists)
                    check1 = None
                    check1 = cur.fetchone() 

                    if check1 == None: #check is successful, add price/date tupple //else ignore
                        #prepare sql for new (price,date)            
                        sqlPrice = 'INSERT INTO price(UID, Price_Date, Original_Price, Price_Promoted, Price_Promoted_Price, Multi_Buy_Special, Multi_Buy_Special_Details, Multi_Buy_Special_Price) VALUES ('
                        
                        sqlPrice += '\'' + res[0] + '\','
                        sqlPrice += 'STR_TO_DATE(\'' +dateOfEx + '\', \'%Y-%m-%d %H:%i:%s\'),'
                        sqlPrice += products[i]['Original Price'] + ',' 
                        pp = '0'
                        if products[i]['Price Promoted'] == 'True':
                            pp = '1'
                        sqlPrice += pp + ',' 
                        ppPrice = '0'
                        if (products[i]['Price Promoted Price'] is None or products[i]['Price Promoted Price']==' ' or products[i]['Price Promoted Price']==''):
                            ppPrice = '0.0'
                        else:
                            ppPrice = products[i]['Price Promoted Price']
                        sqlPrice += ppPrice + ',' 
                        mbs = '0'
                        if products[i]['Multi Buy Special'] == 'TRUE':
                            mbs = '1'
                        sqlPrice += mbs + ',' 
                        sqlPrice += '\'' + products[i]['Multi Buy Special Details'] + '\',' 
                        
                        if (products[i]['Multi Buy Price'] is None or products[i]['Multi Buy Price']==' ' or products[i]['Multi Buy Price']==''):
                            mbPrice = '0.0'
                        else:
                            mbPrice = products[i]['Multi Buy Price']
                        sqlPrice += mbPrice 
                        sqlPrice += ');'

                        #print('====== Price SQL ======')
                        #print(sqlPrice)
                        
                        cur.execute(sqlPrice)
                    else:
                        pass #ignore insertion

            #save new products to newItems-date file and insert them to database
            if len(newProducts) > 0:
                print('====== Preparing New Products ======')
                #put new items in a separate files to be inserted 
                insertionTime = datetime.datetime.now(datetime.timezone.utc)
                insertionTimeStr = insertionTime.strftime('%Y-%m-%d-%H-%M-%S-%Z')
                newItemsFileName = 'newItems-' + insertionTimeStr + '.csv'
                with open(newItemsFileName, 'w+', newline='') as cUM:
                    fUM = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
                    umW = csv.DictWriter(cUM, fieldnames=fUM)
                    umW.writeheader()   

                    for i in tqdm(range(0,len(newProducts))):
                        #check if bran is being repeated in the product name
                        umW.writerow({'Date of data Extraction': newProducts[i]['Date of data Extraction'],
                                                'Brand': newProducts[i]['Brand'], 
                                                'Product name': newProducts[i]['Product name'], 
                                                'Category': newProducts[i]['Category'], 
                                                'Pack size': newProducts[i]['Pack size'], 
                                                'Serving size': newProducts[i]['Serving size'], 
                                                'Servings per pack': newProducts[i][ 'Servings per pack'], 
                                                'Product code': newProducts[i]['Product code'], 
                                                'Energy per 100g (or 100ml)': newProducts[i]['Energy per 100g (or 100ml)'], 
                                                'Protein per 100g (or 100ml)': newProducts[i]['Protein per 100g (or 100ml)'], 
                                                'Total fat per 100g (or 100ml)': newProducts[i]['Total fat per 100g (or 100ml)'], 
                                                'Saturated fat per 100g (or 100ml)': newProducts[i][ 'Saturated fat per 100g (or 100ml)'], 
                                                'Carbohydrate per 100g (or 100ml)': newProducts[i]['Carbohydrate per 100g (or 100ml)'], 
                                                'Sugars per 100g (or 100ml)': newProducts[i]['Sugars per 100g (or 100ml)'], 
                                                'Sodium per 100g (or 100ml)': newProducts[i][ 'Sodium per 100g (or 100ml)'], 
                                                'Original Price': newProducts[i]['Original Price'], 
                                                'Price Promoted': newProducts[i]['Price Promoted'], 
                                                'Price Promoted Price': newProducts[i]['Price Promoted Price'], 
                                                'Multi Buy Special': newProducts[i]['Multi Buy Special'], 
                                                'Multi Buy Special Details': newProducts[i][ 'Multi Buy Special Details'], 
                                                'Multi Buy Price': newProducts[i]['Multi Buy Price'], 
                                                'UID': newProducts[i]['UID']})

                importNewProductData(newItemsFileName, testRun) #also process and commit new items 


            #save products already exitisng in the database for potential information update 
            if len(existingProducts) > 0:
                print('====== Saving existing Products in file ======')
                #put old items in a separate files to be checked if needed 
                insertionTime = datetime.datetime.now(datetime.timezone.utc)
                insertionTimeStr = insertionTime.strftime('%Y-%m-%d-%H-%M-%S-%Z')
                existingItemsFileName = 'existingItems-' + insertionTimeStr + '.csv'
                with open(existingItemsFileName, 'w+', newline='') as existFN:
                    exFHeaderNames = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
                    exFPW = csv.DictWriter(existFN, fieldnames=exFHeaderNames)
                    exFPW.writeheader()   

                    for i in tqdm(range(0,len(existingProducts))):
                        #check if bran is being repeated in the product name
                        exFPW.writerow({'Date of data Extraction': existingProducts[i]['Date of data Extraction'],
                                                'Brand': existingProducts[i]['Brand'], 
                                                'Product name': existingProducts[i]['Product name'], 
                                                'Category': existingProducts[i]['Category'], 
                                                'Pack size': existingProducts[i]['Pack size'], 
                                                'Serving size': existingProducts[i]['Serving size'], 
                                                'Servings per pack': existingProducts[i][ 'Servings per pack'], 
                                                'Product code': existingProducts[i]['Product code'], 
                                                'Energy per 100g (or 100ml)': existingProducts[i]['Energy per 100g (or 100ml)'], 
                                                'Protein per 100g (or 100ml)': existingProducts[i]['Protein per 100g (or 100ml)'], 
                                                'Total fat per 100g (or 100ml)': existingProducts[i]['Total fat per 100g (or 100ml)'], 
                                                'Saturated fat per 100g (or 100ml)': existingProducts[i][ 'Saturated fat per 100g (or 100ml)'], 
                                                'Carbohydrate per 100g (or 100ml)': existingProducts[i]['Carbohydrate per 100g (or 100ml)'], 
                                                'Sugars per 100g (or 100ml)': existingProducts[i]['Sugars per 100g (or 100ml)'], 
                                                'Sodium per 100g (or 100ml)': existingProducts[i][ 'Sodium per 100g (or 100ml)'], 
                                                'Original Price': existingProducts[i]['Original Price'], 
                                                'Price Promoted': existingProducts[i]['Price Promoted'], 
                                                'Price Promoted Price': existingProducts[i]['Price Promoted Price'], 
                                                'Multi Buy Special': existingProducts[i]['Multi Buy Special'], 
                                                'Multi Buy Special Details': existingProducts[i][ 'Multi Buy Special Details'], 
                                                'Multi Buy Price': existingProducts[i]['Multi Buy Price'], 
                                                'UID': existingProducts[i]['UID']})


            #don't commit if it is a test run
            if testRun != True:    
                conn.commit() #commit new data added to database 
            
                            
            # close the cursor 
            cur.close()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(conn)
    return True


#use to update product information from new files. 
#NOTE: do not use none-string fields  
def updateProductInfoSpecificField(productFile, dBFieldToCheck, dataFieldToCheck, testRun=True):
    
    products = []#products that I want to check for update
    issues = [] #to keep products that have mismatch in what we have recorded in the database and what is being updated 

    with open(productFile,'r') as productInput:
        reader = csv.DictReader(productInput, delimiter=',') 
        for row in reader: # each row is a list
            products.append(row)

        conn = None

        try:

            conn = connectDB()
            
            if conn == None:
                print('Failed to connect to DB in importProductData(..)...!')
                raise Exception('Failed to connect')

            # create a cursor
            cur = conn.cursor(buffered=True)

            print("====== Processing information, adding new info to database ======")

            for i in tqdm(range(0,len(products))): 
                #print(products[i])
                
                #check if data is available in database 
                sql = None
                sql = 'SELECT UID, '+ dBFieldToCheck +' FROM product WHERE'
                
                #decide source
                source = ''
                if "-C-" in products[i]['UID']:
                    source = '\'Coles\''
                elif "-W-" in products[i]['UID']:
                    source = '\'Woolworth\''
                
                if source == '': #this needs to flag the wrong source 
                    continue  

                sql += ' Source=' 
                sql += source
                
                sql += ' AND Brand=' 
                sql += '\'' + (products[i]['Brand'].replace('\'', '\'\'') if '\'' in products[i]['Brand'] else products[i]['Brand']) + '\''
                
                sql += ' AND Product_name='
                sql += '\'' + (products[i]['Product name'].replace('\'', '\'\'') if '\'' in products[i]['Product name'] else products[i]['Product name']) + '\''
                
                sql += ' AND Pack_size='
                sql += '\'' + products[i]['Pack size'] + '\''

                #sql += ' AND Product_code='
                #sql += '\'' + products[i]['Product code'] + '\';'
                
                #print('====== Product retrieval SQL ======')
                #print(sql)
                cur.execute(sql)
                res=None
                res = cur.fetchone() 
                

                if res == None: # We have new product
                    print("*** A new product seems to have been inserted UID:"+res[0]+"!")
                    print("*** This should not have happend!")
                else: #check if data existed already for that field and is different 
                    if (res[1] == None) or (res[1] == '') or (res[1] == ' '): #information did not exist for dbField to check  
                        #run an update query 
                    
                        #check the data content to be inserted 
                        dataContentStr = products[i][dataFieldToCheck]
                        if (dataContentStr.find("\'") != -1):
                            dataContentStr = dataContentStr.replace("\'","\\'")


                        #prepare sql for updating the product item            
                        updateSql = "UPDATE product SET "+dBFieldToCheck+"=\'"+ dataContentStr+ "\' WHERE UID=\'" + res[0] + "\';"
                        
                        #print('====== Update SQL ======')
                        #print(updateSql)
                        
                        cur.execute(updateSql)

                    elif (res[1] != products[i][dataFieldToCheck]): #we have missmatched information between old and new 
                        issues.append([products[i], res[0], res[1]])
                    
                    else:#information and database record are the same
                        pass #ignore update

            #save issues to issues-date file to be checked which record is currect
            if len(issues) > 0:
                print('====== Saving products with issues to file ======')
                #put new items in a separate files to be inserted 
                insertionTime = datetime.datetime.now(datetime.timezone.utc)
                insertionTimeStr = insertionTime.strftime('%Y-%m-%d-%H-%M-%S-%Z')
                issuesFileName = 'issues-' + insertionTimeStr + '.csv'
                with open(issuesFileName, 'w+', newline='') as cUM:
                    fUM = ['Database UID','Existing Info','Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Ingredients', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
                    umW = csv.DictWriter(cUM, fieldnames=fUM)
                    umW.writeheader()   

                    for i in tqdm(range(0,len(issues))):
                        #check if bran is being repeated in the product name
                        umW.writerow({'Database UID': issues[i][1],
                                        'Existing Info': issues[i][2],
                                        'Date of data Extraction': issues[i][0]['Date of data Extraction'],
                                        'Brand': issues[i][0]['Brand'], 
                                        'Product name': issues[i][0]['Product name'], 
                                        'Category': issues[i][0]['Category'], 
                                        'Pack size': issues[i][0]['Pack size'], 
                                        'Serving size': issues[i][0]['Serving size'], 
                                        'Servings per pack': issues[i][0][ 'Servings per pack'], 
                                        'Product code': issues[i][0]['Product code'], 
                                        'Ingredients': issues[i][0]['Ingredients'],
                                        'Energy per 100g (or 100ml)': issues[i][0]['Energy per 100g (or 100ml)'], 
                                        'Protein per 100g (or 100ml)': issues[i][0]['Protein per 100g (or 100ml)'], 
                                        'Total fat per 100g (or 100ml)': issues[i][0]['Total fat per 100g (or 100ml)'], 
                                        'Saturated fat per 100g (or 100ml)': issues[i][0][ 'Saturated fat per 100g (or 100ml)'], 
                                        'Carbohydrate per 100g (or 100ml)': issues[i][0]['Carbohydrate per 100g (or 100ml)'], 
                                        'Sugars per 100g (or 100ml)': issues[i][0]['Sugars per 100g (or 100ml)'], 
                                        'Sodium per 100g (or 100ml)': issues[i][0][ 'Sodium per 100g (or 100ml)'], 
                                        'Original Price': issues[i][0]['Original Price'], 
                                        'Price Promoted': issues[i][0]['Price Promoted'], 
                                        'Price Promoted Price': issues[i][0]['Price Promoted Price'], 
                                        'Multi Buy Special': issues[i][0]['Multi Buy Special'], 
                                        'Multi Buy Special Details': issues[i][0][ 'Multi Buy Special Details'], 
                                        'Multi Buy Price': issues[i][0]['Multi Buy Price'], 
                                        'UID': issues[i][0]['UID']})

            #don't commit if it is a test run
            if testRun != True:    
                conn.commit() #commit new data added to database 
            
            # close the cursor 
            cur.close()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(conn)
    return True


#use to update nutrition info from new files
def updateProductNutirtionInfo (productFile, testRun=True):
    products = []#products that I want to check for update
    issues = [] #to keep products that have mismatch in what we have recorded in the database and what is being updated 

    with open(productFile,'r') as productInput:
        reader = csv.DictReader(productInput, delimiter=',') 
        for row in reader: # each row is a list
            products.append(row)

        conn = None

        try:

            conn = connectDB()
            
            if conn == None:
                print('Failed to connect to DB in importProductData(..)...!')
                raise Exception('Failed to connect')

            # create a cursor
            cur = conn.cursor(buffered=True)

            print("====== Processing information, adding new info to database ======")

            for i in tqdm(range(0,len(products))): 
                #print(products[i])
                
                #check if data is available in database 
                sql = None
                sql = 'SELECT UID, Energy_per_100g_or_100ml, Protein_per_100g_or_100ml, Total_fat_per_100g_or_100ml, Saturated_fat_per_100g_or_100ml, Carbohydrate_per_100g_or_100ml, Sugars_per_100g_or_100ml, Sodium_per_100g_or_100ml FROM product WHERE'
                
                #decide source
                source = ''
                if "-C-" in products[i]['UID']:
                    source = '\'Coles\''
                elif "-W-" in products[i]['UID']:
                    source = '\'Woolworth\''
                
                if source == '': #this needs to flag the wrong source 
                    continue  

                sql += ' Source=' 
                sql += source
                
                sql += ' AND Brand=' 
                sql += '\'' + (products[i]['Brand'].replace('\'', '\'\'') if '\'' in products[i]['Brand'] else products[i]['Brand']) + '\''
                
                sql += ' AND Product_name='
                sql += '\'' + (products[i]['Product name'].replace('\'', '\'\'') if '\'' in products[i]['Product name'] else products[i]['Product name']) + '\''
                
                sql += ' AND Pack_size='
                sql += '\'' + products[i]['Pack size'] + '\''

                #sql += ' AND Product_code='
                #sql += '\'' + products[i]['Product code'] + '\';'
                
                #print('====== Product retrieval SQL ======')
                #print(sql)
                cur.execute(sql)
                res=None
                res = cur.fetchone() 
                
                mismatchFlag = False #to check if data does not match the database 

                if res == None: # We have new product
                    print("*** A new product seems to have been inserted UID:"+res[0]+"!")
                    print("*** This should not have happend!")
                
                else: 
                    
                    if (res[1] == None) or (res[1] == '') or (res[1] == ' '): #information did not exist for dbField to check  
                        #check the value we are adding is not empty itself
                        #prepare sql for updating the product item            
                        updateSql = 'UPDATE product SET Energy_per_100g_or_100ml=\''+ products[i]['Energy per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        #print('====== Update SQL ======')
                        #print(updateSql)
                        cur.execute(updateSql)
                    elif (res[1] != products[i]['Energy per 100g (or 100ml)']) and (products[i]['Energy per 100g (or 100ml)'] != ''):#check if data existed already for that field and is different 
                        mismatchFlag = True

                    #repeat for all other nutrition fields 
                    if (res[2] == None) or (res[2] == '') or (res[2] == ' '): 
                        updateSql = 'UPDATE product SET Protein_per_100g_or_100ml=\''+ products[i]['Protein per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        cur.execute(updateSql)
                    elif (res[2] != products[i]['Protein per 100g (or 100ml)']) and (products[i]['Protein per 100g (or 100ml)'] != ''):
                        mismatchFlag = True

                    if (res[3] == None) or (res[3] == '') or (res[3] == ' '): 
                        updateSql = 'UPDATE product SET Total_fat_per_100g_or_100ml=\''+ products[i]['Total fat per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        cur.execute(updateSql)
                    elif (res[3] != products[i]['Total fat per 100g (or 100ml)']) and (products[i]['Total fat per 100g (or 100ml)'] != ''):
                        mismatchFlag = True

                    if (res[4] == None) or (res[4] == '') or (res[4] == ' '): 
                        updateSql = 'UPDATE product SET Saturated_fat_per_100g_or_100ml=\''+ products[i]['Saturated fat per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        cur.execute(updateSql)
                    elif (res[4] != products[i]['Saturated fat per 100g (or 100ml)']) and (products[i]['Saturated fat per 100g (or 100ml)'] != ''):
                        mismatchFlag = True
                    
                    if (res[5] == None) or (res[5] == '') or (res[5] == ' '): 
                        updateSql = 'UPDATE product SET Carbohydrate_per_100g_or_100ml=\''+ products[i]['Carbohydrate per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        cur.execute(updateSql)
                    elif (res[5] != products[i]['Carbohydrate per 100g (or 100ml)']) and (products[i]['Carbohydrate per 100g (or 100ml)'] != ''):
                        mismatchFlag = True
                    
                    if (res[6] == None) or (res[6] == '') or (res[6] == ' '): 
                        updateSql = 'UPDATE product SET Sugars_per_100g_or_100ml=\''+ products[i]['Sugars per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        cur.execute(updateSql)
                    elif (res[6] != products[i]['Sugars per 100g (or 100ml)']) and (products[i]['Sugars per 100g (or 100ml)'] != ''):
                        mismatchFlag = True
                    
                    if (res[7] == None) or (res[7] == '') or (res[7] == ' '): 
                        updateSql = 'UPDATE product SET Sodium_per_100g_or_100ml=\''+ products[i]['Sodium per 100g (or 100ml)']+ '\' WHERE UID=\'' + res[0] + '\';'
                        cur.execute(updateSql)
                    elif (res[7] != products[i]['Sodium per 100g (or 100ml)']) and (products[i]['Sodium per 100g (or 100ml)'] != ''):
                        mismatchFlag = True

                if (mismatchFlag == True): #we have missmatched information between old and new 
                    issues.append([products[i], res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]])
                
            #save issues to issues-date file to be checked which record is currect
            if len(issues) > 0:
                print('====== Saving products with missmatch issues to file ======')
                #put new items in a separate files to be inserted 
                insertionTime = datetime.datetime.now(datetime.timezone.utc)
                insertionTimeStr = insertionTime.strftime('%Y-%m-%d-%H-%M-%S-%Z')
                issuesFileName = 'issues-' + insertionTimeStr + '.csv'
                
                with open(issuesFileName, 'w+', newline='') as cUM:
                    fUM = ['Database UID','Energy_from_DB', 'Protein_from_DB', 'Total_fat_from_DB', 'Saturated_fat_from_DB', 'Carbohydrate_from_DB', 'Sugars_from_DB', 'Sodium_from_DB','Date of data Extraction', 'Brand', 'Product name', 'Ingredients', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
                    umW = csv.DictWriter(cUM, fieldnames=fUM)
                    umW.writeheader()   

                    for i in tqdm(range(0,len(issues))):
                        #check if bran is being repeated in the product name
                        umW.writerow({'Database UID': issues[i][1],
                                        'Energy_from_DB': issues[i][2],
                                        'Protein_from_DB': issues[i][3],
                                        'Total_fat_from_DB': issues[i][4],
                                        'Saturated_fat_from_DB': issues[i][5],
                                        'Carbohydrate_from_DB': issues[i][6],
                                        'Sugars_from_DB': issues[i][7],
                                        'Sodium_from_DB': issues[i][8],
                                        'Date of data Extraction': issues[i][0]['Date of data Extraction'],
                                        'Brand': issues[i][0]['Brand'], 
                                        'Product name': issues[i][0]['Product name'], 
                                        'Category': issues[i][0]['Category'], 
                                        'Pack size': issues[i][0]['Pack size'], 
                                        'Serving size': issues[i][0]['Serving size'], 
                                        'Servings per pack': issues[i][0][ 'Servings per pack'], 
                                        'Product code': issues[i][0]['Product code'], 
                                        'Ingredients': issues[i][0]['Ingredients'],
                                        'Energy per 100g (or 100ml)': issues[i][0]['Energy per 100g (or 100ml)'], 
                                        'Protein per 100g (or 100ml)': issues[i][0]['Protein per 100g (or 100ml)'], 
                                        'Total fat per 100g (or 100ml)': issues[i][0]['Total fat per 100g (or 100ml)'], 
                                        'Saturated fat per 100g (or 100ml)': issues[i][0][ 'Saturated fat per 100g (or 100ml)'], 
                                        'Carbohydrate per 100g (or 100ml)': issues[i][0]['Carbohydrate per 100g (or 100ml)'], 
                                        'Sugars per 100g (or 100ml)': issues[i][0]['Sugars per 100g (or 100ml)'], 
                                        'Sodium per 100g (or 100ml)': issues[i][0][ 'Sodium per 100g (or 100ml)'], 
                                        'Original Price': issues[i][0]['Original Price'], 
                                        'Price Promoted': issues[i][0]['Price Promoted'], 
                                        'Price Promoted Price': issues[i][0]['Price Promoted Price'], 
                                        'Multi Buy Special': issues[i][0]['Multi Buy Special'], 
                                        'Multi Buy Special Details': issues[i][0][ 'Multi Buy Special Details'], 
                                        'Multi Buy Price': issues[i][0]['Multi Buy Price'], 
                                        'UID': issues[i][0]['UID']})

            #don't commit if it is a test run
            if testRun != True:    
                conn.commit() #commit new data added to database 
            
            # close the cursor 
            cur.close()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(conn)
    return True
 


#if __name__ == '__main__':
    #importNewProductData('../res/Frozen/unmatchedItems_frozen.csv', True)
    #importRecentData('../data/w-new-cc.csv', True)
    #importMatches('../res/Frozen/Matches_Frozen.csv', True)
    #importNewProductData('newItems.csv', True)
    #updateProductInfoSpecificField('existingItems-2020-03-20-05-31-27-UTC.csv', 'Product_code', 'Product code', True)
    #updateProductNutirtionInfo('../data/new baby/Baby_w_21112019_cc.csv', True)
