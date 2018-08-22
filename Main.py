
import csv
#from logic.levenshtein import iterative_levenshtein
#from logic.appendID import appendIDtoRow
#from logic.preparations import processFile
from logic.scrapedDataChecker import extractSimilarData
from tkinter import *


##------------------------------##
# --------- (-: UI :-) --------- #
##------------------------------##


class AppGUI(Frame):
    
    def __init__(self, recList, master): 
        Frame.__init__(self, master)
        self.grid()
        self.master.rowconfigure(len(recList), weight=1)   
        self.master.columnconfigure(3, weight=1)

        for i in range(0, len(recList)):
            Button(master, text="Yes",
                command=lambda: 
                    print('accepted')).grid(row=i, column=0)
                    #aB.acceptButton.config(state="disabled")
                    #aB.rejectButton.config(state="disabled"))
            #newButtonA.append(newButtonA)

            Button(master, text="No", 
                command=lambda: 
                    print('rejected')).grid(row=i, column=1)
                    #self.acceptButton.config(state="disabled")
                    #self.rejectButton.config(state="disabled"))
            #newButtonR.append(newButtonR)
            Label(master, text=recList[i]).grid(row=i, column=2)
    #def setRecommendationText(rectext):
    #   self.recText.config(text='change the value')

root = Tk()

recl = ['test 1', 'test 2', 'test 3']

gui = AppGUI(recl, root)

#rec3.setRecommendationText("rec 3 hurray")

root.mainloop()


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



