import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import math

x = []
y = []

x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

a1 = 'pdfFuel.json'
a2 = 'pdfFuelFuzzy.json'
a3 = 'pdfSpeed.json'
a4 = 'pdfSpeedFuzzy.json'

rotas = ['rotas1', 'rotas2', 'rotas3', 'rotas4', 'rotas5']
a = ['fuel1F','fuel2F','fuel3F','fuelGAF']
b = ['fuel1S','fuel2S','fuel3S','fuelGA']
c = ['CO2BFS','CO2DFS','CO2Astar','CO2AG']
d = ['speed1F','speed2F','speed3F','speed1S','speed2S','speed3S']
#arquivo = 'Empirical_Probability_Density'

""" Fuel """
x = []
y = []
total = []
time = []

for j in b:
    lista = []
    tempo = []
    for i in rotas:
        #print("entrou aqui")
        with open(i +'/'+ j+'.json', 'r', encoding='utf8') as f:
                data = json.load(f)
        x.append(np.array(list(map(int,data.keys()))))
        y.append(np.array(list(data.values())))
        listX = list(map(int,data.keys()))
        
        valores = list(data.values())
        cumulative = 0
        time2 = 0

        for h in range(len(valores)):
            cumulative += valores[h]
        lista.append(cumulative)    

        for o in range(len(listX)):            
            time2 += 1#int(listX[o])            
        tempo.append(time2)
    time.append(tempo)
    total.append(lista)

x1 = []
y1 = []
total1 = []
time1 = []

for j in a:
    lista = []
    tempo = []
    for i in rotas:
        
        with open(i +'/'+ j+'.json', 'r', encoding='utf8') as f:
                data = json.load(f)
        x1.append(np.array(list(map(int,data.keys()))))
        y1.append(np.array(list(data.values())))
        listX1 = list(map(int,data.keys()))
        
        valores = list(data.values())
        cumulative = 0 
        time2 = 0

        for h in range(len(valores)):
            cumulative += valores[h]        
        lista.append(cumulative)    

        for o in range(len(listX1)):
            time2 += 1 #listX1[o]        
        tempo.append(time2)

    time1.append(tempo)
    total1.append(lista)

x2 = []
y2 = []
total2 = []

for j in c:
    lista = []
    cont = 1
    for i in rotas:
        
        with open(i +'/'+ j + str(cont) +'F.json', 'r', encoding='utf8') as f:
                data = json.load(f)
        x2.append(np.array(list(map(int,data.keys()))))
        y2.append(np.array(list(data.values())))
        
        valores = list(data.values())
        cumulative = 0 
        time2 = 0

        for h in range(len(valores)):
            cumulative += (valores[h] / 1000)
        lista.append(cumulative)
        cont += 1    

    total2.append(lista)
print("Fuzzy CO2",total2)

x3 = []
y3 = []
total3 = []

for j in c:
    lista = []    
    cont = 1
    for i in rotas:
        
        with open(i +'/'+ j+ str(cont)+'S.json', 'r', encoding='utf8') as f:
                data = json.load(f)
        x3.append(np.array(list(map(int,data.keys()))))
        y3.append(np.array(list(data.values())))
        
        valores = list(data.values())
        cumulative = 0 
        time2 = 0

        for h in range(len(valores)):
            cumulative += (valores[h] / 1000)
        lista.append(cumulative)    
        cont += 1

    total3.append(lista)
print("SUMO CO2",total3)

def plotTotal(total,nameFile):    

    limInf = 0
    limSup = len(total) + 2
    
    space = 0.6

    new = []
    x1 = []
    for i in range(1,len(total)+3):
        if i >= limInf and i <= limSup:
            new.append(int(i))  

    for i in range(1,len(total[0])+1):
        x1.append(int(i))

    x = np.array(x1)
    y = total[0]
    y1 = total[1]
    y2 = total[2]
    y3 = total[3]        
    
    #maximo = max(max(y1),max(y),max(y2),max(y3))
    fig = plt.figure(figsize=(15,5))
    #plt.ylim(0, maximo+4) 
    plt.xlim(limInf, limSup)      
        
    plt.bar(x - 0.47*space, y, label='BFS', color='tab:blue', width=0.2)
    plt.bar(x - 0.16*space, y1, label='DFS', color='tab:orange', width=0.2)        
    plt.bar(x + 0.17*space, y2, label='A-star', color='tab:green', width=0.2)
    plt.bar(x + 0.5*space, y3, label='AG', color='tab:red', width=0.2)      
    #plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")

    if nameFile == 'timeSumo' or nameFile == 'timeFuzzy':        
        plt.ylabel('Tempo (s)', fontweight="bold")
    elif nameFile == 'fuelSumo' or nameFile == 'fuelFuzzy':
        plt.ylabel('Consumo Total de Combustível (ml)', fontweight="bold")
    else:
        plt.ylabel('Emissão de CO2 (mg)', fontweight="bold")
        # https://sumo.dlr.de/docs/Simulation/Output/EmissionOutput.html
    plt.xlabel('Simulação', fontweight="bold")    

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper right", ncol=4)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    
    fig.savefig(nameFile+'Routes.png', bbox_inches='tight')
    plt.show()
    plt.close(fig)

def plotTotal1(total, total2, nameFile):    

    limInf = 0
    limSup = len(total) + 2
    
    space = 0.6

    new = []
    x1 = []
    for i in range(1,len(total)+3):
        if i >= limInf and i <= limSup:
            new.append(int(i))  

    for i in range(1,len(total[0])+1):
        x1.append(int(i))

    x = np.array(x1)
    y = total[0]
    y1 = total[1]
    y2 = total[2]
    y3 = total[3] 

    z = total2[0]
    z1 = total2[1]
    z2 = total2[2]
    z3 = total2[3]        
    
    #maximo = max(max(y1),max(y),max(y2),max(y3))
    fig = plt.figure(figsize=(15,5))
    #plt.ylim(0, maximo+4) 
    plt.xlim(limInf, limSup)
    #plt.yscale('log', nonposy='clip')      
        
    plt.bar(x - 0.59*space, y, label='BFS Fuzzy', color='tab:blue', width=0.1)
    plt.bar(x - 0.427*space, z, label='BFS SUMO', color='darkblue', width=0.1)
    plt.bar(x - 0.26*space, y1, label='DFS Fuzzy', color='tab:orange', width=0.1)
    plt.bar(x - 0.1*space, z1, label='DFS SUMO', color='lightsalmon', width=0.1)        
    plt.bar(x + 0.072*space, y2, label='A-star Fuzzy', color='tab:green', width=0.1)
    plt.bar(x + 0.24*space, z2, label='A-star SUMO', color='darkgreen', width=0.1)
    plt.bar(x + 0.39*space, y3, label='AG Fuzzy', color='tab:red', width=0.1)      
    plt.bar(x + 0.54*space, z3, label='AG SUMO', color='darkred', width=0.1)      
    #plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")

    if nameFile == 'timeSumo' or nameFile == 'timeFuzzy':        
        plt.ylabel('Tempo (s)', fontweight="bold")
    elif nameFile == 'fuelSumo' or nameFile == 'fuelFuzzy':
        plt.ylabel('Consumo Total de Combustível (ml)', fontweight="bold")
    else:
        plt.ylabel('Emissão de CO2 (\u03BCg)', fontweight="bold")
        # https://sumo.dlr.de/docs/Simulation/Output/EmissionOutput.html
    plt.xlabel('Simulação', fontweight="bold")    

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper right", ncol=2)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    
    fig.savefig(nameFile+'FuzzyRoutes.png', bbox_inches='tight')
    plt.close(fig)

#plotTotal(total,'fuelSumo')
#plotTotal(total1,'fuelFuzzy')
#plotTotal(time,'timeSumo')
#plotTotal(time1,'timeFuzzy')
#plotTotal1(total2,total3,'CO2')
plotTotal1(total1,total,'fuelSumo')
