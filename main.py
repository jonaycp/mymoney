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
        
    
    
    
    def create_cols(self):
        #Creating new columns
        self.create_coltotal()
        self.create_datacols()
        self.data['Category1']=""
        self.data['Category2']=""
        
        
#functions which returns a dataframe with 
#selected data according the time

    def selday(self,d,m):
        return self.data[ (self.data['Day']==d) & (self.data['Month']==m) ]
    
    def selweek(self,w,y=2019):
        return self.data[ (self.data['Week']==w) & (self.data['Year']==y) ]
    
    def selmonth(self,m,y=2019):
        return self.data[ (self.data['Month']==m) & (self.data['Year']==y) ]
    
    def selyear(self,y):
        return self.data[self.data['Year']==y]

        
#functions for print information charts

    def print_week(self,w,y=2019):
        myweek=pd.DataFrame(list(self.selweek(w)['Volume'])\
                            ,index=self.selweek(w)['Date']\
                            ,columns=['Volume'])
        
        print(myweek['Volume'].plot(kind='bar'))
        
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




