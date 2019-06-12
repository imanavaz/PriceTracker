from PyQt5 import QtGui,QtCore
import pyqtgraph as pg
import psycopg2
import sys
from connx import *
import numpy as np
from pg_time_axis import *
from datetime import datetime 


# Form implementation generated from reading ui file 'PriceTracker.ui'
#
# Created by: PyQt5 UI code generator 5.11.3

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    conn = None 
    results = [] 

    #def __init__(self, parent=None):
    #    pyqtgraph.setConfigOption('background', 'w') #before loading widget
    #    super(ExampleApp, self).__init__(parent)
        

    def setupUi(self, MainWindow):
        # My Added code - setting the theme for vis element
        # ================
        #pg.setConfigOption('background', 'w')
        #pg.setConfigOption('background', 'k')
        #=================

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1281, 681))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget.setObjectName("widget")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 140, 1270, 541))
        self.tabWidget.setObjectName("tabWidget")
        self.graphTab = QtWidgets.QWidget()
        self.graphTab.setObjectName("graphTab")
        self.exportImageBtn = QtWidgets.QPushButton(self.graphTab)
        self.exportImageBtn.setGeometry(QtCore.QRect(1228, 0, 36, 35))
        self.exportImageBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/export-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportImageBtn.setIcon(icon)
        self.exportImageBtn.setObjectName("exportImageBtn")
        self.visBox = QtGui.QWidget(self.graphTab)
        self.visBox.setGeometry(QtCore.QRect(0, 0, 1228, 515))
        self.visBox.setObjectName("visBox")
        self.tabWidget.addTab(self.graphTab, "")
        self.dataTab = QtWidgets.QWidget()
        self.dataTab.setObjectName("dataTab")
        self.dataTable = QtWidgets.QTableWidget(self.dataTab)
        self.dataTable.setGeometry(QtCore.QRect(0, 0, 1228, 515))
        self.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dataTable.setAlternatingRowColors(True)
        self.dataTable.setObjectName("dataTable")
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.dataTable.horizontalHeader().setCascadingSectionResizes(False)
        self.dataTable.horizontalHeader().setSortIndicatorShown(False)
        self.exportDataBtn = QtWidgets.QPushButton(self.dataTab)
        self.exportDataBtn.setGeometry(QtCore.QRect(1228, 0, 36, 35))
        self.exportDataBtn.setText("")
        self.exportDataBtn.setIcon(icon)
        self.exportDataBtn.setObjectName("exportDataBtn")
        self.tabWidget.addTab(self.dataTab, "")
        self.nutritionTab = QtWidgets.QWidget()
        self.nutritionTab.setObjectName("nutritionTab")
        self.nutritionTable = QtWidgets.QTableWidget(self.nutritionTab)
        self.nutritionTable.setGeometry(QtCore.QRect(0, 0, 1228, 515))
        self.nutritionTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.nutritionTable.setAlternatingRowColors(True)
        self.nutritionTable.setObjectName("nutritionTable")
        self.nutritionTable.setColumnCount(0)
        self.nutritionTable.setRowCount(0)
        self.nutritionTable.horizontalHeader().setCascadingSectionResizes(False)
        self.nutritionTable.horizontalHeader().setSortIndicatorShown(False)
        self.exportNutDataBtn = QtWidgets.QPushButton(self.nutritionTab)
        self.exportNutDataBtn.setGeometry(QtCore.QRect(1228, 0, 36, 35))
        self.exportNutDataBtn.setText("")
        self.exportNutDataBtn.setIcon(icon)
        self.exportNutDataBtn.setObjectName("exportNutDataBtn")
        self.tabWidget.addTab(self.nutritionTab, "")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(740, 10, 531, 131))
        self.groupBox.setObjectName("groupBox")
        self.itemList = QtWidgets.QListWidget(self.groupBox)
        self.itemList.setGeometry(QtCore.QRect(0, 20, 531, 110))
        self.itemList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.itemList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.itemList.setObjectName("itemList")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(6, 10, 691, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.fromDateEdit = QtWidgets.QDateEdit(self.groupBox_2)
        self.fromDateEdit.setGeometry(QtCore.QRect(120, 80, 130, 30))
        self.fromDateEdit.setCalendarPopup(True)
        self.fromDateEdit.setDate(QtCore.QDate(2018, 1, 1))
        self.fromDateEdit.setObjectName("fromDateEdit")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 30, 47, 30))
        self.label.setObjectName("label")
        self.brandLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.brandLineEdit.setGeometry(QtCore.QRect(60, 30, 150, 30))
        self.brandLineEdit.setClearButtonEnabled(True)
        self.brandLineEdit.setObjectName("brandLineEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(220, 30, 47, 30))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(270, 80, 51, 30))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(420, 30, 47, 30))
        self.label_5.setObjectName("label_5")
        self.toDateEdit = QtWidgets.QDateEdit(self.groupBox_2)
        self.toDateEdit.setGeometry(QtCore.QRect(325, 80, 130, 30))
        self.toDateEdit.setCalendarPopup(True)
        self.toDateEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.toDateEdit.setObjectName("toDateEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 101, 30))
        self.label_2.setObjectName("label_2")
        self.nameLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.nameLineEdit.setGeometry(QtCore.QRect(260, 30, 150, 30))
        self.nameLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.searchProductButton = QtWidgets.QPushButton(self.groupBox_2)
        self.searchProductButton.setGeometry(QtCore.QRect(580, 30, 100, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../img/search-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchProductButton.setIcon(icon1)
        self.searchProductButton.setCheckable(False)
        self.searchProductButton.setObjectName("searchProductButton")
        self.packSizeLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.packSizeLineEdit.setGeometry(QtCore.QRect(480, 30, 81, 30))
        self.packSizeLineEdit.setClearButtonEnabled(True)
        self.packSizeLineEdit.setObjectName("packSizeLineEdit")
        self.reportButton = QtWidgets.QPushButton(self.groupBox_2)
        self.reportButton.setGeometry(QtCore.QRect(580, 80, 100, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../img/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reportButton.setIcon(icon2)
        self.reportButton.setObjectName("reportButton")
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.brandLineEdit, self.nameLineEdit)
        MainWindow.setTabOrder(self.nameLineEdit, self.packSizeLineEdit)
        MainWindow.setTabOrder(self.packSizeLineEdit, self.searchProductButton)
        MainWindow.setTabOrder(self.searchProductButton, self.itemList)
        MainWindow.setTabOrder(self.itemList, self.fromDateEdit)
        MainWindow.setTabOrder(self.fromDateEdit, self.toDateEdit)
        MainWindow.setTabOrder(self.toDateEdit, self.reportButton)
        MainWindow.setTabOrder(self.reportButton, self.tabWidget)

        # My Added code
        # ================
        self.searchProductButton.clicked.connect(self.seachForProduct)
        self.reportButton.clicked.connect(self.generateReport)

        self.visBox.setLayout(QtGui.QVBoxLayout())
        self.canvas = pg.GraphicsLayoutWidget() # create GrpahicsLayoutWidget obejct  
        

        # icon locations "../img/search-icon.png"
        # ================

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Price Tracker"))
        self.exportImageBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export Image</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graphTab), _translate("MainWindow", "Graph"))
        self.dataTable.setSortingEnabled(False)
        self.exportDataBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export Data</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataTab), _translate("MainWindow", "Data"))
        self.nutritionTable.setSortingEnabled(False)
        self.exportNutDataBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export Data</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.nutritionTab), _translate("MainWindow", "Nutrition Info"))
        self.groupBox.setTitle(_translate("MainWindow", "Search Results: "))
        self.groupBox_2.setTitle(_translate("MainWindow", "Search for products:"))
        self.fromDateEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy"))
        self.label.setText(_translate("MainWindow", "Brand :"))
        self.brandLineEdit.setPlaceholderText(_translate("MainWindow", " Product Brand"))
        self.label_4.setText(_translate("MainWindow", "Name :"))
        self.label_3.setText(_translate("MainWindow", "To date : "))
        self.label_5.setText(_translate("MainWindow", "Pack Size: "))
        self.toDateEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy"))
        self.label_2.setText(_translate("MainWindow", "Report from date : "))
        self.nameLineEdit.setPlaceholderText(_translate("MainWindow", " Product Name"))
        self.searchProductButton.setText(_translate("MainWindow", "Search"))
        self.searchProductButton.setShortcut(_translate("MainWindow", "Alt+S"))
        self.packSizeLineEdit.setPlaceholderText(_translate("MainWindow", " Pack Size"))
        self.reportButton.setText(_translate("MainWindow", "Report"))
        self.reportButton.setShortcut(_translate("MainWindow", "Alt+R"))


        #++++++ My Code ++++++++
        self.dataTable.setColumnCount(8)     #Set 8 columns
        self.dataTable.setHorizontalHeaderLabels(['Brand', 'Name', 'Pack size', 'Product Code', 'Date', 'Original Price', 'Promoted price', 'Multi Buy Special Price'])
        self.dataTable.resizeColumnsToContents()

        self.nutritionTable.setColumnCount(6)     #Set 5 columns
        self.nutritionTable.setHorizontalHeaderLabels(['  ', 'From Coles', 'Qty per 100 gr/ml','   ','From Woolworth', 'Qty per 100 gr/ml'])
        self.nutritionTable.resizeColumnsToContents()
        
        #self.nutritionTable.setRowCount(10)
        #self.nutritionTable.setVerticalHeaderLabels(['Brand', 'Name', 'Pack size', 'Energy', 'Protein', 'Total fat', 'Saturated fat', 'Carbohydrate', 'Sugars', 'Sodium'])
        
        #+++++++++++++++++++++++

    
    # My Added code
    # ================
    
    def seachForProduct(self):
        print('== Searching for product')
        try:
            self.conn = connectDB()
            
            if self.conn is None:
                print('Failed to connect to DB in Ui_ProceTracker.searchForProduct(..)...!')
                raise Exception('Failed to connect')

            # create a cursor
            cur = self.conn.cursor()
            
            #check if data is available in database 
            sql = None
            sql = 'SELECT * FROM product as product'
            sql += ' WHERE LOWER(Brand) LIKE LOWER(\'%' + self.brandLineEdit.text() +'%\')' 
            sql += ' AND LOWER(Product_name) LIKE LOWER(\'%' + self.nameLineEdit.text() + '%\')' 
            sql += ' AND LOWER(Pack_size) LIKE LOWER(' +'\'%' + self.packSizeLineEdit.text() + '%\');'

            #print('====== Product retrieval SQL ======')
            #print(sql)
            
            cur.execute(sql)
            #res=None
            #res = cur.fetchall() 
            self.results = []
            for row in cur:
                self.results.append([row[0],row[1],row[4],row[5],row[7]])

            self.itemList.clear()
            
            for i in range(len(self.results)):
                self.itemList.addItem(self.results[i][1]+" - " + self.results[i][2]+" - " + self.results[i][3]+" - "+self.results[i][4])   

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            disconnectDB(self.conn)

   
             
    def generateReport(self):
        self.nutritionTable.setRowCount(0) 
        #get selected items    
        selectedProducts = self.itemList.selectedItems()
        
        
        if len(selectedProducts) < 1 :
            print("Generate Report - No item has been selected")
        else:
            dataResults = []
            dataForVis = []

            for product in selectedProducts:
                #itemIndexes.append(self.itemList.row(product))
                print("Selected item's UID :" + self.results[self.itemList.row(product)][0])
                print("item list row:", self.results[self.itemList.row(product)])

                try:
                    self.conn = connectDB()
            
                    if self.conn is None:
                        print('Failed to connect to DB in Ui_ProceTracker.generateReport(..)...!')
                        raise Exception('Failed to connect')

                    # create a cursor
                    cur = self.conn.cursor()
                    
                    #Get price data from database 
                    sql = None
                    sql = 'Select product.Brand, product.Product_name, product.Pack_size, product.Product_code, DATE_FORMAT(price.Price_Date, \'%d/%m/%Y\') as Date, price.Original_Price, price.Price_Promoted_Price, price.Multi_Buy_Special_Price'
                    sql += ' from product'
                    sql += ' LEFT JOIN price'
                    sql += ' ON product.UID=price.UID'
                    sql += ' where product.UID=\'' + self.results[self.itemList.row(product)][0] +'\'' 
                    sql += ' AND price.Price_Date BETWEEN STR_TO_DATE(\'' + self.fromDateEdit.text() + '\', \'%d/%m/%Y\') AND STR_TO_DATE(\'' + self.toDateEdit.text() + '\', \'%d/%m/%Y\');'
                            
                    cur.execute(sql)
                    priceDateData = []
                                        
                    for row in cur:
                        #prepare data table data
                        dataResults.append([row[0], row[1], row[2], row[3], row[4], row[5], row[7]])
                        priceDateData.append([row[4],row[5]])


                    #prepare data for vis
                    dataForVis.append([self.results[self.itemList.row(product)][1]+'-'+self.results[self.itemList.row(product)][2]+'-'+self.results[self.itemList.row(product)][3] , priceDateData])

                    

                    #get matches and nutrition data
                    uid = self.results[self.itemList.row(product)][0]
                    
                    matchSQL = 'SELECT * FROM matches WHERE '
                    if "-C-" in uid:
                        matchSQL += 'UID1=\'' + uid + '\'' #Coles is UID1
                    elif "-W-" in uid:
                        matchSQL += 'UID2=\'' + uid + '\'' #Woolworth is UID2  
                    
                    cur2 = self.conn.cursor()
                    cur2.execute(matchSQL)
                    foundMatches = []#[uid] #put the selected item in this as well to uniform the table generation
                    for r in cur2:
                        foundMatches.append(r)
                    
                    if len(foundMatches) < 1:#no matches found
                        foundMatches = [[uid]]

                    #print("Matches found are:")
                    #print(foundMatches)
                    
                    fetchSQL=''
                    colesCount = 0
                    woolworthCount = 0
                    
                    for fm in foundMatches:
                        rowNo = self.nutritionTable.rowCount()
                        self.nutritionTable.insertRow(rowNo)
                        self.nutritionTable.setItem(rowNo, 0, QtGui.QTableWidgetItem("Brand"))
                        self.nutritionTable.insertRow(rowNo + 1)
                        self.nutritionTable.setItem(rowNo + 1, 0, QtGui.QTableWidgetItem("Name"))
                        self.nutritionTable.insertRow(rowNo + 2)
                        self.nutritionTable.setItem(rowNo + 2, 0, QtGui.QTableWidgetItem("Pack size"))
                        self.nutritionTable.insertRow(rowNo + 3)
                        self.nutritionTable.setItem(rowNo + 3, 0, QtGui.QTableWidgetItem("Energy"))
                        self.nutritionTable.insertRow(rowNo + 4)
                        self.nutritionTable.setItem(rowNo + 4, 0, QtGui.QTableWidgetItem("Protein"))
                        self.nutritionTable.insertRow(rowNo + 5)
                        self.nutritionTable.setItem(rowNo + 5, 0, QtGui.QTableWidgetItem("Total fat"))
                        self.nutritionTable.insertRow(rowNo + 6)
                        self.nutritionTable.setItem(rowNo + 6, 0, QtGui.QTableWidgetItem("Saturated fat"))
                        self.nutritionTable.insertRow(rowNo + 7)
                        self.nutritionTable.setItem(rowNo + 7, 0, QtGui.QTableWidgetItem("Carbohydrate"))
                        self.nutritionTable.insertRow(rowNo + 8)
                        self.nutritionTable.setItem(rowNo + 8, 0, QtGui.QTableWidgetItem("Sugar"))
                        self.nutritionTable.insertRow(rowNo + 9)
                        self.nutritionTable.setItem(rowNo + 9, 0, QtGui.QTableWidgetItem("Sodium"))
                        
                        fetchSQL = 'SELECT UID as Uid, Source as ItemSource, Brand as Brand, Product_name as ProductName,'
                        fetchSQL += 'Pack_size as PackSize, Energy_per_100g_or_100ml as Energy, Protein_per_100g_or_100ml as Protein,'
                        fetchSQL += 'Total_fat_per_100g_or_100ml as TotalFat, Saturated_fat_per_100g_or_100ml as  SaturatedFat, '
                        fetchSQL += 'Carbohydrate_per_100g_or_100ml as Carbohydrate, Sugars_per_100g_or_100ml as Sugar, '
                        fetchSQL += 'Sodium_per_100g_or_100ml as Sodium FROM product WHERE UID=\''+fm[0]+'\''
                        cur2.execute(fetchSQL)
                        #print("Fetch SQL :" + fetchSQL)

                        fresult = cur2.fetchone()
                        #print(fresult)
                        sIndex = 0 #index to fill the table
                        
                        if fresult is not None:
                            if fresult[1] == 'Coles':
                                sIndex = 1
                            else:
                                sIndex = 4
                                    
                            self.nutritionTable.setItem(rowNo , sIndex, QtGui.QTableWidgetItem(fresult[2]))
                            self.nutritionTable.setItem(rowNo + 1, sIndex, QtGui.QTableWidgetItem(fresult[3]))
                            self.nutritionTable.setItem(rowNo + 2, sIndex, QtGui.QTableWidgetItem(fresult[4]))
                            self.nutritionTable.setItem(rowNo + 3, sIndex + 1, QtGui.QTableWidgetItem(fresult[5]))
                            self.nutritionTable.setItem(rowNo + 4, sIndex + 1, QtGui.QTableWidgetItem(fresult[6]))
                            self.nutritionTable.setItem(rowNo + 5, sIndex + 1, QtGui.QTableWidgetItem(fresult[7]))
                            self.nutritionTable.setItem(rowNo + 6, sIndex + 1, QtGui.QTableWidgetItem(fresult[8]))
                            self.nutritionTable.setItem(rowNo + 7, sIndex + 1, QtGui.QTableWidgetItem(fresult[9]))
                            self.nutritionTable.setItem(rowNo + 8, sIndex + 1, QtGui.QTableWidgetItem(fresult[10]))
                            self.nutritionTable.setItem(rowNo + 9, sIndex + 1, QtGui.QTableWidgetItem(fresult[11]))
                        
                        if (len(fm) > 1): #there is an actual match found match
                            fetchSQL = 'SELECT UID as Uid, Source as ItemSource, Brand as Brand, Product_name as ProductName,'
                            fetchSQL += 'Pack_size as PackSize, Energy_per_100g_or_100ml as Energy, Protein_per_100g_or_100ml as Protein,'
                            fetchSQL += 'Total_fat_per_100g_or_100ml as TotalFat, Saturated_fat_per_100g_or_100ml as  SaturatedFat, '
                            fetchSQL += 'Carbohydrate_per_100g_or_100ml as Carbohydrate, Sugars_per_100g_or_100ml as Sugar, '
                            fetchSQL += 'Sodium_per_100g_or_100ml as Sodium FROM product WHERE UID=\''+fm[1]+'\''
                            cur2.execute(fetchSQL)
                            #print("Fetch SQL 2:" + fetchSQL)

                            fresult = cur2.fetchone()
                            #print(fresult)
                            
                            if fresult is not None:
                                sIndex = 0 #index to fill the table
                                if fresult[1] == 'Coles':#probably not anymore 
                                    sIndex = 1
                                else:
                                    sIndex = 4
                                    
                                self.nutritionTable.setItem(rowNo , sIndex, QtGui.QTableWidgetItem(fresult[2]))
                                self.nutritionTable.setItem(rowNo + 1, sIndex, QtGui.QTableWidgetItem(fresult[3]))
                                self.nutritionTable.setItem(rowNo + 2, sIndex, QtGui.QTableWidgetItem(fresult[4]))
                                self.nutritionTable.setItem(rowNo + 3, sIndex + 1, QtGui.QTableWidgetItem(fresult[5]))
                                self.nutritionTable.setItem(rowNo + 4, sIndex + 1, QtGui.QTableWidgetItem(fresult[6]))
                                self.nutritionTable.setItem(rowNo + 5, sIndex + 1, QtGui.QTableWidgetItem(fresult[7]))
                                self.nutritionTable.setItem(rowNo + 6, sIndex + 1, QtGui.QTableWidgetItem(fresult[8]))
                                self.nutritionTable.setItem(rowNo + 7, sIndex + 1, QtGui.QTableWidgetItem(fresult[9]))
                                self.nutritionTable.setItem(rowNo + 8, sIndex + 1, QtGui.QTableWidgetItem(fresult[10]))
                                self.nutritionTable.setItem(rowNo + 9, sIndex + 1, QtGui.QTableWidgetItem(fresult[11]))
                                
                    
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    disconnectDB(self.conn)

                
            
            #process dataResults into dataTable 
            self.dataTable.setRowCount(0) 

            for row_number, row_data in enumerate(dataResults):
                self.dataTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.dataTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))


            
            self.drawVis(dataForVis)

            self.dataTable.resizeColumnsToContents()
            self.nutritionTable.resizeColumnsToContents()         


    #$ pip install pyqtgraph​
    def drawVis(self, data):
        
        print(data)
        
        self.canvas.clear()
        self.visBox.layout().addWidget(self.canvas)
        self.myPlot = self.canvas.addPlot(title='Price over time')  
        #self.myPlot.clear()

        
        #x_axis = self.myPlot.getAxis('bottom')
        y_axis = self.myPlot.getAxis('left')
        #x_axis.setLabel(text='Price date') # set axis labels
        y_axis.setLabel(text='Price')
        self.myPlot.addLegend() # create a legend   

        for i in range(len(data)):
            xData = []#[1, 2, 3 , 4]
            yData = []#[10, 20, 10, 30]
            for d in data[i][1]:
                xData.append((datetime.strptime(d[0], '%d/%m/%Y')).timestamp())
                yData.append(d[1])
            
            #xdict = dict(enumerate(x)) #x-axis is date
            #stringaxis = pg.AxisItem(orientation='bottom') 
            #stringaxis.setTicks([xdict.items()]) 
            
            # Add the Date-time axis
            x_axis = DateAxisItem(orientation='bottom')
            x_axis.attachToPlotItem(self.myPlot)
            

            #x_axis.axisItems={'bottom': stringaxis}
            pl = self.myPlot.plot(x=xData,y=yData, pen=(i,len(data)), symbol='o', symbolPen=(i,len(data)), symbolBrush=0.5, name=data[i][0])
            #pl = self.myPlot.plot(x,y, pen=(i,len(data)))
            
            #if legend is to be put in specific coordinate
            #l = pg.LegendItem((100,30), offset=(950,(i+1)*30))  # args are (size, offset)
            #l.setParentItem(self.myPlot.graphicsItem())   # Note we do NOT call plt.addItem in this case
            #l.addItem(pl, data[i][0])

  
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# ================