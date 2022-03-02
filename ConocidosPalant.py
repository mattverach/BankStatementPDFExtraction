import re

import requests
import pdfplumber
import pandas as pd
from collections import namedtuple

print(" _____                        _     _           ")
print("/  __ \                      (_)   | |          ")
print("| /  \/ ___  _ __   ___   ___ _  __| | ___  ___ ")
print("| |    / _ \| '_ \ / _ \ / __| |/ _` |/ _ \/ __|")
print("| \__/\ (_) | | | | (_) | (__| | (_| | (_) \__ \ ")
print(" \____/\___/|_| |_|\___/ \___|_|\__,_|\___/|___/")
print("")
print("Bank Statement Information Extraction Software by LkN & Devil")
print("")

text=''
print("1.Copie el archivo PDF a la carpeta del programa")
print("2.El programa generara un archivo 'Output.csv' (Importante: El nuevo archivo reemplazara uno generado anteriormente)")
valinput = input("3.Ingrese el nombre del archivo PDF: ")


#Devuelve una copia del String que recibe sin los substrings entre parentesis (Bug codigo de barra)
def remove_nested_parens(input_str):
    result = ''
    paren_level = 0
    for ch in input_str:
        if ch == '(':
            paren_level += 1
        elif (ch == ')') and paren_level:
            paren_level -= 1
        elif not paren_level:
            result += ch
    return result

with pdfplumber.open(valinput + '.pdf') as pdf:
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
        #Cambiamos coma decimal por punto decimal y parse float
        registro_total = registro_total.replace(',','.')
        
        
        

        registro_total = float(remove_nested_parens(registro_total))
        
        
        print(registro_total)
        
          
        if registro_total < total_actual:
            debito.append(registro_importe)
            nuevo_registro = {'Debito':registro_importe, 'Credito':'', "Total":registro_total}
            df = df.append(nuevo_registro, ignore_index = True)
            print('Débito: ' + registro_importe)
        else:
            credito.append(registro_importe)
            nuevo_registro = {'Debito':'', 'Credito':registro_importe , "Total":registro_total}
            df = df.append(nuevo_registro, ignore_index = True)
            print('Crédito: ' + registro_importe)
            
        total_actual = registro_total
        


#print(debito, credito)
print(df)
df.to_csv('Output.csv')