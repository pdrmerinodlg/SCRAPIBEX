''' CODE CRAWLER IBEX
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>> Scrap the bank PROGRAM >>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

types
   registro Empresa
      nombre : str
      ultimo : str
      dif : str
      color : str
      fondo : bool
    fin_registros

variables
   f : file
   fuente, fecha : str
   ibex35[35], info[35], aleatorios[10] : str
   posiciones[35], finposi[35], fin_primeracol[35], ini_segundacol[35], fin_segundacol[35], ini_terceracol[35], fin_tercerracol[35] : int
   empresasIBEX[35] : Empresa
'''
from bs4 import BeautifulSoup
import requests
import random
import time
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import datetime


class Empresa:
    def __init__(self):
        self.nombre = ''
        self.ultimo = ''
        self.dif = ''
        self.color = ''
        self.fondo = False


empresasIBEX = [ Empresa() for _ in range(35) ]


#connection to database

maquina_remota = MongoClient("mongodb://pete:p3dr0@localhost:27017")

baseddatos = maquina_remota.crawler

# -----------------------------------------------------------------------------------------------------------------
# ----We start by taking data from the website. First, we will generate a text file with the web's HTML------------
# -----------------------------------------------------------------------------------------------------------------


URL = "http://www.bolsamadrid.es/esp/aspx/Portada/Portada.aspx"

req = requests.get(URL)

htmlText = req.text

with open('log1.txt', 'w') as fichero:
        for linea in htmlText:
                fichero.write(linea)

fichero.close()

# Now we open in lecture mode and we start the pursuit.

f = open('log1.txt','tr')

fuente = f.read()

# At this point, we've got the HTML code in a variable. Now we create an array which contains the names of the companies we want to monitorize.

ibex35 = ['ACCIONA','ACERINOX','ACS','AENA','AMADEUS','ARCELORMIT.','BA.SABADELL','B.SANTANDER','BANKIA','BANKINTER','BBVA','CAIXABANK','CELLNEX','CIE AUTOMOT.','ENAGAS','ENCE','ENDESA','FERROVIAL','GRIFOLS CL.A','IAG','IBERDROLA','INDITEX','INDRA A','INM.COLONIAL','MAPFRE','MASMOVIL','MEDIASET','MELIA HOTELS','MERLIN','NATURGY','R.E.C.','REPSOL','SIEMENS GAME','TELEFONICA','VISCOFAN']

posiciones = [0]*35

finposi = [0]*35

# We are going to look for the first appearance of the companies' names in the code, and the position we need to cut.

for i in range(35):
    
    posiciones[i] = int(fuente.find(ibex35[i]))
    
    finposi[i] = int(fuente.find('</tr>',posiciones[i]))

# Now we cut (for the first time) the text and save the info in an array.

info = ['']*35

for i in range(35):
    
    info[i]=fuente[posiciones[i]:finposi[i]]
 
# At last, but not least, we are going to 'chop' each position of the array (which contains the info of a single company) to save it 
# properly in a register (empresasIBEX) to make as accesible as possible, because we want to graphically visualize the data.    

fin_primeracol = [0]*35

ini_segundacol = [0]*35

fin_segundacol = [0]*35

ini_terceracol = [0]*35

fin_terceracol = [0]*35

ini_color = [0]*35

fin_color = [0]*35

for i in range(35):
    
    fin_primeracol[i] = int(info[i].find('</A>'))
    
    ini_segundacol[i] = int(info[i].find('<td>',fin_primeracol[i]))
    
    fin_segundacol[i] = int(info[i].find('</td>',ini_segundacol[i]))
    
    ini_terceracol[i] = int(info[i].find('<td ',fin_segundacol[i]))
    
    fin_terceracol[i] = int(info[i].find('</td>',ini_terceracol[i])) 

    ini_color[i] = int(info[i].find('="',ini_terceracol[i]))
    
    fin_color[i] = int(info[i].find('">',ini_color[i]))

for i in range(35):
    
    empresasIBEX[i].nombre = info[i][0:fin_primeracol[i]]
    
    empresasIBEX[i].ultimo = info[i][ini_segundacol[i]+4:fin_segundacol[i]]
    
    empresasIBEX[i].dif = info[i][ini_terceracol[i]+20:fin_terceracol[i]]
    
    empresasIBEX[i].color = info[i][ini_color[i]+2:fin_color[i]]
    
    if (info[i][ini_color[i]+2:fin_color[i]] == 'DifClSb'):
        empresasIBEX[i].color = 'V'
    else:
        empresasIBEX[i].color = 'R'
   

aleatorios = ['']*10

for i in range(10):
    aleatorios[i] = empresasIBEX[random.randint(0,34)].nombre

for i in range(35):
    for j in range(10):
        if (empresasIBEX[i].nombre == aleatorios[j]):
            empresasIBEX[i].fondo = True


# To conclude, we are going to associate a date to each execution of the script and we output the data in json structure to the database. We 
# print the result, for good luck ;)

result = []

for i in range(35):
    print(f'Nombre: {empresasIBEX[i].nombre} ---- Último: {empresasIBEX[i].ultimo} ---- %dif: {empresasIBEX[i].dif} ---- 
        color: empresasIBEX[i].color} ---- fondo: {empresasIBEX[i].fondo}')
    
    float(empresasIBEX[i].dif.replace(',','.')),'color' : empresasIBEX[i].color, 'fondo' : empresasIBEX[i].fondo })
    
    result.append({'nombre' : empresasIBEX[i].nombre,'ultimo' : str(empresasIBEX[i].ultimo.replace(',','.')), 
        '%_dif' : str(empresasIBEX[i].dif.replace(',','.')),'color' : empresasIBEX[i].color, 'fondo' : empresasIBEX[i].fondo })

baseddatos.ibex35.insert({'fecha':datetime.datetime.utcnow(),'empresasIBEX':result})

print(result)

f.close()
