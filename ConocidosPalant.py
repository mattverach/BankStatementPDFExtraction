import re

import requests
import pdfplumber
import pandas as pd
from collections import namedtuple

text=''

with pdfplumber.open('Dic2020.pdf') as pdf:
    for page in pdf.pages:
        text += page.extract_text()
        

registro = re.compile(r'(ð )?(ñ )?\d{2}[-].*')

data = {
            "Debito": [],
            "Credito": [],
            "Total": []
        }
df = pd.DataFrame(data)


total_actual = 0
debito = []
credito = []
for line in text.split('\n'):
    if registro.match(line):
        registro_fecha, *registro_desc = line.split()
        registro_importe = registro_desc[len(registro_desc)-2]
        registro_total = registro_desc[len(registro_desc)-1]
        
        #Eliminamos los puntos
        registro_total = registro_total.replace('.','')
        print(registro_total)
        #Cambiamos coma decimal por punto decimal y parse float
        registro_total = float(registro_total.replace(',','.'))
        
          
        if registro_total < total_actual:
            debito.append(registro_importe)
            nuevo_registro = {'Debito':registro_importe, 'Credito':'', "Total":registro_total}
            df = df.append(nuevo_registro, ignore_index = True)
            #print('Débito: ' + registro_importe)
        else:
            credito.append(registro_importe)
            nuevo_registro = {'Debito':'', 'Credito':registro_importe , "Total":registro_total}
            df = df.append(nuevo_registro, ignore_index = True)
            #print('Crédito: ' + registro_importe)
            
        total_actual = registro_total
        


#print(debito, credito)
print(df)
df.to_csv('Final.csv')