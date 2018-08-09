import csv
import re

def processFile (inputCSV, outputCSV):
    
    with open(inputCSV,'r') as csvinput:
        with open(outputCSV, 'w', newline = '\n' ) as csvoutput:
            writer = csv.DictWriter(csvoutput, fieldnames = ["ID","Brand","Product name","Pack size","Amount", "Unit"])
            reader = csv.DictReader(csvinput)

            writer.writeheader()

            for row in reader:
                psize = row["Pack size"]
                mStrResult = re.match(r'\d*\.?\d+',psize)
                
                if (mStrResult):
                    amount = re.findall(r'\d*\.?\d+',psize)
                else:
                    amount = [""];

                unit = psize.replace(amount[0],'')

                writer.writerow({'ID': row['ID'], 'Brand': row['Brand'], 'Product name': row['Product name'], 'Pack size' : row ['Pack size'], 'Amount' : amount[0], 'Unit' : unit})
                        
        csvoutput.close()

