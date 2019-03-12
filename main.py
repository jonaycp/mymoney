import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv(
    './data/data20190310.csv', 
    sep=';', 
    dayfirst=1, 
    header=0,
    #parse_dates=['Date'],  #muy importante, de otra manera lo pilla mal.
    dtype={"Volume":float}, #parseamos la cantidad a un float
    usecols=['Date','Volume'] #, 'Note', 'Type']
    )

print("Data dimensions: ",data.shape) #Imprime las dimensiones del dataset
#print(data.count) #Imprime las dimensiones del dataset
col_names= data.columns.tolist() #Guardamos en una lista los nombres de las columnas
print(col_names)

#print(data[data.Date > '01/31/2019']) #Imprime con filtro de fechas

###OJO porque las fechas estan como MM/DD/YYYY

#print(data.describe()) #da cierta informacion de los valores numericos

#HACEMOS UN LISTADO SOLO CON LOS GASTOS Y OTRO CON LOS INGRESOS
gastos=data.loc[data['Volume'] < 0]
ingresos=data.loc[data['Volume'] > 0]




###SHOW THE PLOT
x=gastos['Date']
y=gastos['Volume']

#First paint try
fig = plt.figure()
axes = fig.add_axes([0.1,0.1,0.8,0.8])
axes.plot(x,y)

print("Mean of average: ", np.average(y))
print("Expense Min: ", np.amin(y))
print("Expense Max: ", np.amax(y))
print("Total Sum: ", np.sum(y))

plt.show()


