import csv
from tqdm import tqdm


def cleanWolies (inputDirtyFile, outputCleanFile):
    print(" --- Clean Woolies files, removing brands from product name ---")

    rows = []
    with open(inputDirtyFile,'r') as csvinput1:
        reader1 = csv.DictReader(csvinput1, delimiter=',') 
        for row in reader1: # each row is a list
            rows.append(row)

    # new updated data
    with open(outputCleanFile, 'w+', newline='') as cUM:
        fUM = ['Date of data Extraction', 'Brand', 'Product name', 'Category', 'Pack size', 'Serving size', 'Servings per pack', 'Product code', 'Ingredients', 'Energy per 100g (or 100ml)', 'Protein per 100g (or 100ml)', 'Total fat per 100g (or 100ml)', 'Saturated fat per 100g (or 100ml)', 'Carbohydrate per 100g (or 100ml)', 'Sugars per 100g (or 100ml)', 'Sodium per 100g (or 100ml)', 'Original Price', 'Price Promoted', 'Price Promoted Price', 'Multi Buy Special', 'Multi Buy Special Details', 'Multi Buy Price', 'UID']
        umW = csv.DictWriter(cUM, fieldnames=fUM)
        umW.writeheader()   

        newRows = []

        for i in tqdm(range(0,len(rows))):
            #check if bran is being repeated in the product name
            brand = rows[i]['Brand'].strip().lower()
            productName = rows[i]['Product name'].strip().lower()
            newPName = productName

            if (productName.startswith(brand) and len(brand)>0): ###### ADDED len(brand)
                newPName = productName[len(brand)+1:].strip()
                if (len(newPName) > 0):
                    if (newPName[0] == '-'):
                        newPName = newPName[1:].strip()

            umW.writerow({'Date of data Extraction': rows[i]['Date of data Extraction'],
                                            'Brand': rows[i]['Brand'], 
                                            'Product name': newPName, 
                                            'Category': rows[i]['Category'], 
                                            'Pack size': rows[i]['Pack size'], 
                                            'Serving size': rows[i]['Serving size'], 
                                            'Servings per pack': rows[i][ 'Servings per pack'], 
                                            'Product code': rows[i]['Product code'], #for woolworth IDs m['ProductID'] in the past / for cloes m['Product code']
                                            'Ingredients': rows[i]['Ingredients'],
                                            'Energy per 100g (or 100ml)': rows[i]['Energy per 100g (or 100ml)'], 
                                            'Protein per 100g (or 100ml)': rows[i]['Protein per 100g (or 100ml)'], 
                                            'Total fat per 100g (or 100ml)': rows[i]['Total fat per 100g (or 100ml)'], 
                                            'Saturated fat per 100g (or 100ml)': rows[i][ 'Saturated fat per 100g (or 100ml)'], 
                                            'Carbohydrate per 100g (or 100ml)': rows[i]['Carbohydrate per 100g (or 100ml)'], 
                                            'Sugars per 100g (or 100ml)': rows[i]['Sugars per 100g (or 100ml)'], 
                                            'Sodium per 100g (or 100ml)': rows[i][ 'Sodium per 100g (or 100ml)'], 
                                            'Original Price': rows[i]['Original Price'], 
                                            'Price Promoted': rows[i]['Price Promoted'], 
                                            'Price Promoted Price': rows[i]['Price Promoted Price'], 
                                            'Multi Buy Special': rows[i]['Multi Buy Special'], 
                                            'Multi Buy Special Details': rows[i][ 'Multi Buy Special Details'], 
                                            'Multi Buy Price': rows[i]['Multi Buy Price'], 
                                            'UID': rows[i]['UID']})
            #print (brand + ' -- ' + newPName)
    return True


if __name__ == "__main__":
   pass
   #cleanWolies('C:/Users/avaz/OneDrive - Deakin University/Projects/Price Tracker/Data/RData/20200302-woolworths-export/20200302-woolworths-export-i.csv', 'C:/Users/avaz/OneDrive - Deakin University/Projects/Price Tracker/Data/RData/test.csv')
   #cleanWolies('w-3-i-Bakery-Not clean.csv', 'w-3-i-cc-Bakery.csv')
   #cleanWolies('w-3-i-Drinks-Not clean.csv', 'w-3-i-cc-Drinks.csv')
   