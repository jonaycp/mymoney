#ibrerias para el trato de datos
import pandas as pd 
import numpy as np
import re

#Representacion de gr'aficas
import seaborn as sns
import matplotlib.pyplot as plt

#Utilidades del sistema, como para comprobar si un archivo existe
import os

#Printing with colors
from termcolor import colored

#Add algoriths for calculate how similar or different are 2 strings
import textdistance as td


class mymoney:
    #creator function
    #Parameters:
    #   filepath = the path of the csv file, by default data/Transactions.csv"
    #   initial = if we have only transaction but not the total, 
    #   with initial we can calculate the total after each transaction
    def __init__(self,myfilepath="data/Transactions.csv",initial=0):
        
        #loading the file
        self.filepath=myfilepath
        self.data=self.loadcsv()
        #setting the initial amount
        self.initial_total=initial
        
        #Changing data types
        self.data["Date"]=pd.to_datetime(self.data["Date"])
        
        #creating new columns
        self.create_cols()
        
        
        

    def loadcsv(self):
        exists = os.path.isfile(self.filepath)
        if exists:
            # Store configuration file values
            mydata = pd.read_csv(\
                           self.filepath,\
                           sep=';',\
                           dayfirst=1,\
                           header=0,\
                           #parse_dates=['Date'],  #muy importante, de otra manera lo pilla mal.
                           dtype={"Volume":float})
                          # usecols=['Date','Volume'] ) #, 'Note', 'Type'
            return mydata
        else:
            print("The file doesn't exist")
            return False

        
        
        

    def create_coltotal(self):
            saldo=self.initial_total
            self.data["Total"]=0.
            self.data["Total"][0]=saldo
            for i in range(len(self.data["Volume"])):
                if i == 0: self.data["Total"][i]=saldo+self.data["Volume"][0]
                else: self.data["Total"][i] = self.data["Total"][i-1] + self.data["Volume"][i]

    def create_datacols(self):
        self.data['Week']=self.data['Date'].dt.week
        self.data['Month']=self.data['Date'].dt.month
        self.data['Year']=self.data['Date'].dt.year
        self.data['Day']=self.data['Date'].dt.day
        
    #This column will have True if the row is an expense, and False if is not (Salary entry, utilities, etc)

        
    
    
    def create_cols(self):
        #Creating new columns
        self.create_coltotal()
        self.create_datacols()
        self.data['Category1']=0
        self.data['Category2']=0
        #This column will have True if the row is an expense, 
        #and False if is not (Salary entry, utilities, etc)
        self.data['periodic']=False        
        #String field where it will be possible to add a better description for the expense
        self.data['Description']=""
        
#functions which returns a dataframe with 
#selected data according the time

    def selday(self,d,m):
        return self.data[ (self.data['Day']==d) & (self.data['Month']==m) ]
    
    def selweek(self,w,y=2019):
        return self.data[ (self.data['Week']==w) & (self.data['Year']==y) ]
    
    def selmonth(self,m,y=2019):
        return self.data[ (self.data['Month']==m) & (self.data['Year']==y) ]
    
    def selyear(self,y=2019):
        return self.data[ self.data['Year']==y ]
    
    def selexpen(self,expenseId):
        return self.data.iloc[expenseId]

        
#functions for print information charts

    def print_week(self,w,y=2019):
        myweek=pd.DataFrame(list(self.selweek(w)['Volume'])\
                            ,index=self.selweek(w)['Date']\
                            ,columns=['Volume'])
        
        print(myweek['Volume'].plot(kind='bar'))
        
    def print_year(self,y=2019):
        myyear=pd.DataFrame(list(self.selyear(y)['Volume'])\
                            ,index=self.selyear(y)['Date']\
                            ,columns=['Volume'])
        print(myyear['Volume'].plot())

        
    def print_month(self,m,y=2019):
        mymonth=pd.DataFrame(list(self.selmonth(m)['Volume'])\
                            ,index=self.selmonth(m)['Date']\
                            ,columns=['Volume'])
        
        print(mymonth['Volume'].plot())     

    def print_monthbyweeks(self,m,y=2019):
        mymonth=pd.DataFrame(list(self.selmonth(m)['Volume'])\
                            ,index=self.selmonth(m)['Week']\
                            ,columns=['Volume'])
        mymonth=mymonth.groupby(by='Week').sum()
        print(mymonth['Volume'].plot(kind="bar"))
        
    
    def print_expen(self,expenid):
        print(self.selexpen(expenid))
        
        
#Selecting similar expenses to apply changes
#elem = index of element to compare
#field = Name of the column to match
#porcent, is a string metric for measuring the difference between two sequences. 
    def findsimilar(self,elem,field,porcent=100):
        if 0 < porcent <= 100 : porcent=porcent/100.
        myresult=[]
        myelem=m.data.iloc[elem][field]
        for ind,it in enumerate(m.data[field]):
            if td.jaro(str(myelem),str(it)) >= porcent :
                myresult.append(ind)
        myresult.remove(elem)
        return myresult

#Print results from findsimilar
    def printsimilar(self,elem,field,porcent=100):
        listresult = self.findsimilar(elem,field,porcent)
        return self.data.iloc[listresult]

#Given a list of index, the category and level or category, it uodates the information.
    def setcategory(self,elemlist,cat,level=1):
        if (level == 1): self.data['Category1'][elemlist]=cat
        else: self.data['Category2'][elemlist]=cat
        return self.data