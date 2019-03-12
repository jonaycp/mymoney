import pandas as pd 

data = pd.read_csv(
    './data/data20190310.csv', 
    sep=';', 
    dayfirst=1, 
    header=0,
    parse_dates=['Date'],  #muy importante, de otra manera lo pilla mal.
    dtype={"Volume":float},
    usecols=['Date','Volume', 'Note', 'Type']
    )

print(data.shape) #Imprime las dimensiones del dataset
print(data.count) #Imprime las dimensiones del dataset
col_names= data.columns.tolist() #Guardamos en una lista los nombres de las columnas
print(col_names)

#print(data[data.Date > '01/31/2019']) #Imprime con filtro de fechas

###OJO porque las fechas estan como MM/DD/YYYY

#print(data.describe()) #da cierta informacion de los valores numericos
