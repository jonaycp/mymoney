import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_csv(
    './data/data20190310.csv', 
    sep=';', 
    dayfirst=1, 
    header=0,
    #parse_dates=['Date'],  #muy importante, de otra manera lo pilla mal.
    dtype={"Volume":float}, #parseamos la cantidad a un float
    usecols=['Date','Volume'] #, 'Note', 'Type']
    )

print(data.shape) #Imprime las dimensiones del dataset
print(data.count) #Imprime las dimensiones del dataset
col_names= data.columns.tolist() #Guardamos en una lista los nombres de las columnas
print(col_names)
x=data['Date']
y=data['Volume']
#print(data[data.Date > '01/31/2019']) #Imprime con filtro de fechas

###OJO porque las fechas estan como MM/DD/YYYY

#print(data.describe()) #da cierta informacion de los valores numericos



#First paint try
fig = plt.figure()
axes = fig.add_axes([0.1,0.1,0.8,0.8])
axes.plot(x,y)
plt.show()
