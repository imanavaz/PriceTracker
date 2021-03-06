from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets  import QFileDialog
import pyqtgraph as pg
import psycopg2
import sys, os
import csv
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
        MainWindow.resize(1280, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1281, 711))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainTab = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.mainTab.setObjectName("mainTab")
        self.analysisTab = QtWidgets.QWidget()
        self.analysisTab.setObjectName("analysisTab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.analysisTab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(-1, -1, 1281, 701))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget.setObjectName("widget")
        self.nutritionTab = QtWidgets.QTabWidget(self.widget)
        self.nutritionTab.setGeometry(QtCore.QRect(0, 160, 1270, 521))
        self.nutritionTab.setObjectName("nutritionTab")
        self.graphTab = QtWidgets.QWidget()
        self.graphTab.setObjectName("graphTab")
        self.exportImageBtn = QtWidgets.QPushButton(self.graphTab)
        self.exportImageBtn.setGeometry(QtCore.QRect(1228, 0, 36, 35))
        self.exportImageBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/export-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportImageBtn.setIcon(icon)
        self.exportImageBtn.setObjectName("exportImageBtn")
        self.visBox = QtWidgets.QWidget(self.graphTab)
        self.visBox.setGeometry(QtCore.QRect(0, 4, 1228, 495))
        self.visBox.setObjectName("visBox")
        self.nutritionTab.addTab(self.graphTab, "")
        self.dataTab = QtWidgets.QWidget()
        self.dataTab.setObjectName("dataTab")
        self.dataTable = QtWidgets.QTableWidget(self.dataTab)
        self.dataTable.setGeometry(QtCore.QRect(0, 0, 1228, 495))
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
        self.nutritionTab.addTab(self.dataTab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.nutritionTable = QtWidgets.QTableWidget(self.tab)
        self.nutritionTable.setGeometry(QtCore.QRect(0, 0, 1228, 495))
        self.nutritionTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.nutritionTable.setAlternatingRowColors(True)
        self.nutritionTable.setObjectName("nutritionTable")
        self.nutritionTable.setColumnCount(0)
        self.nutritionTable.setRowCount(0)
        self.nutritionTable.horizontalHeader().setCascadingSectionResizes(False)
        self.nutritionTable.horizontalHeader().setSortIndicatorShown(False)
        self.exportNutDataBtn = QtWidgets.QPushButton(self.tab)
        self.exportNutDataBtn.setGeometry(QtCore.QRect(1228, 0, 36, 35))
        self.exportNutDataBtn.setText("")
        self.exportNutDataBtn.setIcon(icon)
        self.exportNutDataBtn.setObjectName("exportNutDataBtn")
        self.nutritionTab.addTab(self.tab, "")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(610, 10, 661, 151))
        self.groupBox.setObjectName("groupBox")
        self.itemList = QtWidgets.QListWidget(self.groupBox)
        self.itemList.setGeometry(QtCore.QRect(0, 20, 661, 131))
        self.itemList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.itemList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.itemList.setObjectName("itemList")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 10, 601, 151))
        self.groupBox_2.setObjectName("groupBox_2")
        self.fromDateEdit = QtWidgets.QDateEdit(self.groupBox_2)
        self.fromDateEdit.setGeometry(QtCore.QRect(80, 110, 141, 30))
        self.fromDateEdit.setCalendarPopup(True)
        self.fromDateEdit.setDate(QtCore.QDate(2018, 1, 1))
        self.fromDateEdit.setObjectName("fromDateEdit")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 30, 47, 30))
        self.label.setObjectName("label")
        self.brandLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.brandLineEdit.setGeometry(QtCore.QRect(80, 30, 181, 30))
        self.brandLineEdit.setClearButtonEnabled(True)
        self.brandLineEdit.setObjectName("brandLineEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(280, 30, 47, 30))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(270, 110, 51, 30))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 47, 30))
        self.label_5.setObjectName("label_5")
        self.toDateEdit = QtWidgets.QDateEdit(self.groupBox_2)
        self.toDateEdit.setGeometry(QtCore.QRect(320, 110, 121, 30))
        self.toDateEdit.setCalendarPopup(True)
        self.toDateEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.toDateEdit.setObjectName("toDateEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 101, 30))
        self.label_2.setObjectName("label_2")
        self.nameLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.nameLineEdit.setGeometry(QtCore.QRect(320, 30, 161, 30))
        self.nameLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.searchProductButton = QtWidgets.QPushButton(self.groupBox_2)
        self.searchProductButton.setGeometry(QtCore.QRect(511, 70, 81, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../img/search-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchProductButton.setIcon(icon1)
        self.searchProductButton.setCheckable(False)
        self.searchProductButton.setObjectName("searchProductButton")
        self.packSizeLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.packSizeLineEdit.setGeometry(QtCore.QRect(80, 70, 141, 30))
        self.packSizeLineEdit.setClearButtonEnabled(True)
        self.packSizeLineEdit.setObjectName("packSizeLineEdit")
        self.reportButton = QtWidgets.QPushButton(self.groupBox_2)
        self.reportButton.setGeometry(QtCore.QRect(510, 110, 81, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../img/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reportButton.setIcon(icon2)
        self.reportButton.setObjectName("reportButton")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(264, 70, 47, 30))
        self.label_8.setObjectName("label_8")
        self.categoryLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.categoryLineEdit.setGeometry(QtCore.QRect(320, 70, 121, 30))
        self.categoryLineEdit.setClearButtonEnabled(True)
        self.categoryLineEdit.setObjectName("categoryLineEdit")
        self.verticalLayout_2.addWidget(self.widget)
        self.mainTab.addTab(self.analysisTab, "")
        self.dataImportTab = QtWidgets.QWidget()
        self.dataImportTab.setObjectName("dataImportTab")
        self.dataImportGB = QtWidgets.QGroupBox(self.dataImportTab)
        self.dataImportGB.setGeometry(QtCore.QRect(10, 10, 601, 121))
        self.dataImportGB.setObjectName("dataImportGB")
        self.checkBox = QtWidgets.QCheckBox(self.dataImportGB)
        self.checkBox.setGeometry(QtCore.QRect(20, 75, 121, 25))
        self.checkBox.setObjectName("checkBox")
        self.newDataFileLe = QtWidgets.QLineEdit(self.dataImportGB)
        self.newDataFileLe.setGeometry(QtCore.QRect(70, 40, 441, 25))
        self.newDataFileLe.setObjectName("newDataFileLe")
        self.label_6 = QtWidgets.QLabel(self.dataImportGB)
        self.label_6.setGeometry(QtCore.QRect(20, 40, 111, 25))
        self.label_6.setObjectName("label_6")
        self.openDataFileBtn = QtWidgets.QPushButton(self.dataImportGB)
        self.openDataFileBtn.setGeometry(QtCore.QRect(520, 40, 75, 25))
        self.openDataFileBtn.setObjectName("openDataFileBtn")
        self.loadDataFileBtn = QtWidgets.QPushButton(self.dataImportGB)
        self.loadDataFileBtn.setGeometry(QtCore.QRect(520, 75, 75, 25))
        self.loadDataFileBtn.setObjectName("loadDataFileBtn")
        self.dataImportGB_2 = QtWidgets.QGroupBox(self.dataImportTab)
        self.dataImportGB_2.setGeometry(QtCore.QRect(10, 130, 601, 121))
        self.dataImportGB_2.setObjectName("dataImportGB_2")
        self.testRunAdditionCb = QtWidgets.QCheckBox(self.dataImportGB_2)
        self.testRunAdditionCb.setGeometry(QtCore.QRect(20, 75, 121, 25))
        self.testRunAdditionCb.setObjectName("testRunAdditionCb")
        self.additionalPriceDataFileLe = QtWidgets.QLineEdit(self.dataImportGB_2)
        self.additionalPriceDataFileLe.setGeometry(QtCore.QRect(70, 40, 441, 25))
        self.additionalPriceDataFileLe.setObjectName("additionalPriceDataFileLe")
        self.label_7 = QtWidgets.QLabel(self.dataImportGB_2)
        self.label_7.setGeometry(QtCore.QRect(20, 40, 111, 25))
        self.label_7.setObjectName("label_7")
        self.openAddedDataFileBtn = QtWidgets.QPushButton(self.dataImportGB_2)
        self.openAddedDataFileBtn.setGeometry(QtCore.QRect(520, 40, 75, 25))
        self.openAddedDataFileBtn.setObjectName("openAddedDataFileBtn")
        self.loadAddedDataFileBtn = QtWidgets.QPushButton(self.dataImportGB_2)
        self.loadAddedDataFileBtn.setGeometry(QtCore.QRect(520, 75, 75, 25))
        self.loadAddedDataFileBtn.setObjectName("loadAddedDataFileBtn")
        self.mainTab.addTab(self.dataImportTab, "")
        self.verticalLayout.addWidget(self.mainTab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.mainTab.setCurrentIndex(0)
        self.nutritionTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.mainTab, self.brandLineEdit)
        MainWindow.setTabOrder(self.brandLineEdit, self.nameLineEdit)
        MainWindow.setTabOrder(self.nameLineEdit, self.packSizeLineEdit)
        MainWindow.setTabOrder(self.packSizeLineEdit, self.categoryLineEdit)
        MainWindow.setTabOrder(self.categoryLineEdit, self.searchProductButton)
        MainWindow.setTabOrder(self.searchProductButton, self.fromDateEdit)
        MainWindow.setTabOrder(self.fromDateEdit, self.toDateEdit)
        MainWindow.setTabOrder(self.toDateEdit, self.reportButton)
        MainWindow.setTabOrder(self.reportButton, self.itemList)
        MainWindow.setTabOrder(self.itemList, self.nutritionTab)
        MainWindow.setTabOrder(self.nutritionTab, self.exportImageBtn)
        MainWindow.setTabOrder(self.exportImageBtn, self.exportDataBtn)
        MainWindow.setTabOrder(self.exportDataBtn, self.exportNutDataBtn)
        MainWindow.setTabOrder(self.exportNutDataBtn, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.newDataFileLe)
        MainWindow.setTabOrder(self.newDataFileLe, self.openDataFileBtn)
        MainWindow.setTabOrder(self.openDataFileBtn, self.loadDataFileBtn)
        MainWindow.setTabOrder(self.loadDataFileBtn, self.testRunAdditionCb)
        MainWindow.setTabOrder(self.testRunAdditionCb, self.additionalPriceDataFileLe)
        MainWindow.setTabOrder(self.additionalPriceDataFileLe, self.openAddedDataFileBtn)
        MainWindow.setTabOrder(self.openAddedDataFileBtn, self.loadAddedDataFileBtn)
        MainWindow.setTabOrder(self.loadAddedDataFileBtn, self.nutritionTable)
        MainWindow.setTabOrder(self.nutritionTable, self.dataTable)

        # My Added code
        # ================
        self.searchProductButton.clicked.connect(self.seachForProduct)
        self.reportButton.clicked.connect(self.generateReport)
        self.exportNutDataBtn.clicked.connect(self.saveNutritionReport)
        self.exportDataBtn.clicked.connect(self.savePriceReport)

        self.visBox.setLayout(QtGui.QVBoxLayout())
        self.canvas = pg.GraphicsLayoutWidget() # create GrpahicsLayoutWidget obejct  
        

        # icon locations "../img/search-icon.png"
        # ================

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Price Tracker"))
        self.exportImageBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export Image</p></body></html>"))
        self.nutritionTab.setTabText(self.nutritionTab.indexOf(self.graphTab), _translate("MainWindow", "Graph"))
        self.dataTable.setSortingEnabled(False)
        self.exportDataBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export Data</p></body></html>"))
        self.nutritionTab.setTabText(self.nutritionTab.indexOf(self.dataTab), _translate("MainWindow", "Data"))
        self.nutritionTable.setSortingEnabled(False)
        self.exportNutDataBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export Data</p></body></html>"))
        self.nutritionTab.setTabText(self.nutritionTab.indexOf(self.tab), _translate("MainWindow", "Nutrition Info"))
        self.groupBox.setTitle(_translate("MainWindow", "Search Results: "))
        self.groupBox_2.setTitle(_translate("MainWindow", "Search for products:"))
        self.fromDateEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy"))
        self.label.setText(_translate("MainWindow", "Brand :"))
        self.brandLineEdit.setPlaceholderText(_translate("MainWindow", " Product Brand"))
        self.label_4.setText(_translate("MainWindow", "Name :"))
        self.label_3.setText(_translate("MainWindow", "To date : "))
        self.label_5.setText(_translate("MainWindow", "Pack Size: "))
        self.toDateEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy"))
        self.label_2.setText(_translate("MainWindow", "From date : "))
        self.nameLineEdit.setPlaceholderText(_translate("MainWindow", " Product Name"))
        self.searchProductButton.setText(_translate("MainWindow", "Search"))
        self.searchProductButton.setShortcut(_translate("MainWindow", "Alt+S"))
        self.packSizeLineEdit.setPlaceholderText(_translate("MainWindow", " Pack Size"))
        self.reportButton.setText(_translate("MainWindow", "Report"))
        self.reportButton.setShortcut(_translate("MainWindow", "Alt+R"))
        self.label_8.setText(_translate("MainWindow", "Category:"))
        self.categoryLineEdit.setPlaceholderText(_translate("MainWindow", "Category"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.analysisTab), _translate("MainWindow", "Analysis"))
        self.dataImportGB.setTitle(_translate("MainWindow", "Import New Data"))
        self.checkBox.setText(_translate("MainWindow", "Run a test only "))
        self.label_6.setText(_translate("MainWindow", "Data file:"))
        self.openDataFileBtn.setText(_translate("MainWindow", "Open"))
        self.loadDataFileBtn.setText(_translate("MainWindow", "Load"))
        self.dataImportGB_2.setTitle(_translate("MainWindow", "Import Additional Price Data"))
        self.testRunAdditionCb.setText(_translate("MainWindow", "Run a test only "))
        self.label_7.setText(_translate("MainWindow", "Data file:"))
        self.openAddedDataFileBtn.setText(_translate("MainWindow", "Open"))
        self.loadAddedDataFileBtn.setText(_translate("MainWindow", "Load"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.dataImportTab), _translate("MainWindow", "Data Import"))


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
            sql += ' AND LOWER(Category) LIKE LOWER(\'%' + self.categoryLineEdit.text() + '%\')' #just changed LIKE to =     
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

            try:
                self.conn = connectDB()
        
                if self.conn is None:
                    print('Failed to connect to DB in Ui_ProceTracker.generateReport(..)...!')
                    raise Exception('Failed to connect')

                for product in selectedProducts:
                    #itemIndexes.append(self.itemList.row(product))
                    #print("Selected item's UID :" + self.results[self.itemList.row(product)][0])
                    #print("item list row:", self.results[self.itemList.row(product)])

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
                    itemstr = str(data)
                    if column_number > 4 and (itemstr == '0' or itemstr == '0.0'):
                        itemstr = ''
                    self.dataTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(itemstr))
                #print(row_data)    


            
            self.drawVis(dataForVis)

            self.dataTable.resizeColumnsToContents()
            self.nutritionTable.resizeColumnsToContents()         


    def saveNutritionReport(self):
        path = QFileDialog.getSaveFileName(self.nutritionTable, 'Export nutrition data to CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['  ', 'From Coles', 'Qty per 100 gr/ml','   ','From Woolworth', 'Qty per 100 gr/ml'])
                for row in range(self.nutritionTable.rowCount()):
                    row_data = []
                    for column in range(self.nutritionTable.columnCount()):
                        item = self.nutritionTable.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)


    def savePriceReport(self):                
        path = QFileDialog.getSaveFileName(self.nutritionTable, 'Export price data to CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            #from price data table 
            with open(path[0], 'w+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Brand', 'Name', 'Pack size', 'Product Code', 'Date', 'Original Price', 'Promoted price', 'Multi Buy Special Price'])
                for row in range(self.dataTable.rowCount()):
                    row_data = []
                    for column in range(self.dataTable.columnCount()):
                        item = self.dataTable.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)        
          


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