import csv
import time
import datetime

#this function will append a uniques ID to each row, reading the timestamp of each row, and adding a number to it.
#This si how it is used: append ID to coles
#appendIDtoRow('coles.csv', 'coles2.csv','C') #these would be the files with unique IDs

def appendIDtoRow (inputCSV, outputCSV, seperator):
    with open(inputCSV,'r') as csvinput:
        with open(outputCSV, 'w') as csvoutput:
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
                    rdate = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S %Z")
                    unixtime = time.mktime(rdate.timetuple())
                    newid = str(unixtime)+"-"+seperator+"-"+str(count)
                    count = count + 1
                    row.append(newid)
                    all.append(row)

            writer.writerows(all)

        csvoutput.close()

