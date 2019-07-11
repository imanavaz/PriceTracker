import psycopg2
from tqdm import tqdm
import csv
from connx import *


def generateNutritionReport():
    conn = None

    try:
        conn = connectDB()
        
        if conn is None:
            print('Failed to connect to DB in importProductData(..)...!')
            raise Exception('Failed to connect')

        # create a cursor
        cur = conn.cursor(buffered=True)

        
        #Get price data from database 
        sql = None
        sql = 'SELECT Source, Brand, Product_name, Category, Pack_size, Serving_size, Servings_per_Pack,  Energy_per_100g_or_100ml, Protein_per_100g_or_100ml, Total_fat_per_100g_or_100ml, Saturated_fat_per_100g_or_100ml, Carbohydrate_per_100g_or_100ml, Sugars_per_100g_or_100ml, Sodium_per_100g_or_100ml, UID, Product_code FROM product'
        
        cur.execute(sql)

        #insert in CSV file        
        with open('product_list.csv', 'w+', newline='') as cUM:
            fUM = ['Source', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'UID', 'Product code', 'Nutrition info from match', 'Match source', 'Match UID', 'Dietary code']
            umW = csv.DictWriter(cUM, fieldnames=fUM)
            umW.writeheader()   

            foundMatchItems = []
            
            
            for row in tqdm(cur):
                
                if (row[14] not in foundMatchItems):#if item is not in found matches, then process 
                    energy = row[7] 
                    protein = row[8] 
                    totalFat = row[9] 
                    saturatedFat = row[10] 
                    carbohydrate = row[11] 
                    sugars = row[12] 
                    sodium = row[13]
                    nutritionInfo = 'False'

                    cur2 = conn.cursor(buffered=True)
                    sql2 = 'SELECT UID1, UID2 FROM matches WHERE UID1=\''+row[14]+'\' OR UID2=\'' + row[14]+'\'' #check if there is a match
                    cur2.execute(sql2)
                    result = cur2.fetchone()
                    matchFound = ''
                    matchSource = ''

                    if result is not None:  
                        if result[0] == row[14]:
                            matchFound = result[1]
                        else:
                            matchFound = result[0]
                        foundMatchItems.append(matchFound)    
                        if "-C-" in matchFound:
                            matchSource = 'Coles'
                        elif "-W-" in matchFound:
                            matchSource = 'Woolworth'             
                    
                    #check if nutrition data exists for row, if not, get nutrition data from match
                    if (row[9]=='' or row[9]==' '):
                            #print('found a match for: '+row[14]+' in database pair: ['+result[0]+' , '+result[1]+']')
                            sql3 = 'SELECT Energy_per_100g_or_100ml, Protein_per_100g_or_100ml, Total_fat_per_100g_or_100ml, Saturated_fat_per_100g_or_100ml, Carbohydrate_per_100g_or_100ml, Sugars_per_100g_or_100ml, Sodium_per_100g_or_100ml FROM product'
                            sql3 += ' WHERE UID=\''+matchFound+'\''
                            cur2.execute(sql3)

                            nutri = cur2.fetchone()
                            if nutri is not None:
                                energy = nutri[0] 
                                protein = nutri[1]
                                totalFat = nutri[2]
                                saturatedFat = nutri[3]
                                carbohydrate = nutri[4]
                                sugars = nutri[5]
                                sodium = nutri[6]
                                nutritionInfo = 'True'

                    umW.writerow({'Source': row[0],
                                'Brand': row[1], 
                                'Product name': row[2], 
                                'Category': row[3], 
                                'Pack size': row[4], 
                                'Serving size': row[5], 
                                'Servings per pack': row[6], 
                                'Energy per 100g (or 100ml)': energy, 
                                'Protein per 100g (or 100ml)': protein, 
                                'Total fat per 100g (or 100ml)': totalFat, 
                                'Saturated fat per 100g (or 100ml)': saturatedFat, 
                                'Carbohydrate per 100g (or 100ml)': carbohydrate, 
                                'Sugars per 100g (or 100ml)': sugars, 
                                'Sodium per 100g (or 100ml)': sodium, 
                                'UID': row[14],
                                'Product code': row[15],
                                'Nutrition info from match': nutritionInfo,
                                'Match source': matchSource, 
                                'Match UID': matchFound,
                                'Dietary code': ''})
    
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(conn)


if __name__ == '__main__':
    generateNutritionReport()