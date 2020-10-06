import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import math

# Rota_01_187_DFS resultados
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

a = ['pdfFuel1F','pdfFuel2F','pdfFuel3F','pdfFuel1S','pdfFuel2S','pffFuel3S']
b = ['pdfSpeed1F','pdfSpeed2F','pdfSpeed3F','pdfSpeed1S','pdfSpeed2S','pffSpeed3S']
c = ['fuel1F','fuel2F','fuel3F','fuel1S','fuel2S','fuel3S']
d = ['speed1F','speed2F','speed3F','speed1S','speed2S','speed3S']
#arquivo = 'Empirical_Probability_Density'

""" Fuel """
with open('PDF/'+ a[4]+'.json', 'r', encoding='utf8') as f:
        data = json.load(f)
x = np.array(list(map(int,data.keys())))
y = np.array(list(data.values()))
print(y)
cdf1 = list(data.values())
cumulative = 0
for i in range(len(cdf1)):
    cumulative += cdf1[i]
    cdf1[i] = cumulative

with open('PDF/'+a[1]+'.json', 'r', encoding='utf8') as f:
        data = json.load(f)
x1 = np.array(list(map(int,data.keys())))
y1 = np.array(list(data.values()))
print(y1)
cdf2 = list(data.values())
cumulative = 0
for i in range(len(cdf2)):
    cumulative += cdf2[i]
    cdf2[i] = cumulative

""" Speed """
with open('PDF/'+b[4]+'.json', 'r', encoding='utf8') as f:
        data = json.load(f)
x2 = np.array(list(map(int,data.keys())))
y2 = np.array(list(data.values()))

cdf3 = list(data.values())
cumulative = 0
for i in range(len(cdf3)):
    cumulative += cdf3[i]
    cdf3[i] = cumulative

with open('PDF/'+b[1]+'.json', 'r', encoding='utf8') as f:
        data = json.load(f)
x3 = np.array(list(map(int,data.keys())))
y3 = np.array(list(data.values()))

cdf4 = list(data.values())
cumulative = 0
for i in range(len(cdf4)):
    cumulative += cdf4[i]
    cdf4[i] = cumulative

def plotPDF(x,x1,y,y1,nameFile):    

    if nameFile == 'speed':
        limInf = 14
        limSup = 56
    else:
        limInf = -1
        limSup = max(x)+1
    
    space = 0.4

    new = []
    for i in range(len(x)):
        if i >= limInf and i <= limSup:
            new.append(int(x[i]))    

    maximo = max(max(y),max(y1))
    fig = plt.figure(figsize=(15,5))
    plt.ylim(0, maximo+4) 
    plt.xlim(limInf, limSup)      
        
    #plt.bar(x - 0.43*space, y2, label='Neural Network', color='tab:blue', width=0.2)
    plt.bar(x - 0.37*space, y, label='SUMO', color='tab:orange', width=0.3)        
    plt.bar(x + 0.37*space, y1, label='Fuzzy', color='tab:green', width=0.3)
    #plt.bar(x + 0.5*space, y3, label='SUMO', color='tab:red', width=0.2)  
    #plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.ylabel('Função Densidade de Probabilidade Empírica (%)', fontweight="bold")
    #plt.xlabel('Fuel Consumption (ml/s)', fontweight="bold")
    if nameFile == 'fuel':
        plt.xlabel('Consumo de Combustível (ml/s)', fontweight="bold")
    else:
        plt.xlabel('Velocidade (km/h)', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper right", ncol=2)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    
    fig.savefig(nameFile+'PDF.png', bbox_inches='tight')
    plt.close(fig)

def plotCDF(x,cdf1,cdf2,nameFile):    

    np.array(cdf1)
    np.array(cdf2)

    limInf = 0
    limSup = max(x)-2
    space = 0.6

    new = []
    for i in range(len(x)):
        if i >= limInf and i <= limSup:
            new.append(int(x[i]))

    fig = plt.figure(figsize=(15,5))
    plt.ylim(0, max(cdf1)+5 or max(cdf2)+5) 
    plt.xlim(limInf, limSup)    
    
    print(len(x))
    print(x)
    print(cdf1)
    #plt.bar(x - 0.43*space, y2, label='Neural Network', color='tab:blue', width=0.2)
    plt.bar(x - 0.1*space, cdf1, label='SUMO', color='tab:orange', width=0.2)        
    plt.bar(x + 0.2*space, cdf2, label='Fuzzy', color='tab:green', width=0.2)
    #plt.bar(x + 0.5*space, y3, label='SUMO', color='tab:red', width=0.2)  
    #plt.ylabel('Cumulative Distribution Function (%)', fontweight="bold")
    plt.ylabel('Função Distribuição Acumulada (%)', fontweight="bold")
    # plt.xlabel('Fuel Consumption (ml/s)', fontweight="bold")    
    if nameFile == 'fuel':
        plt.xlabel('Consumo de Combustível (ml/s)', fontweight="bold")
    else:
        plt.xlabel('Velocidade (km/h)', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper left", ncol=2)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    name = 'CDF'
    fig.savefig(name+'.png', bbox_inches='tight')
    plt.close(fig)

def plotCDF1(x,cdf1,cdf2,nameFile):
    fig = plt.figure(1)
    
    yMax = max(cdf1) or max(cdf2)
    yMim =  min(cdf1) and min(cdf2)

    xMax = max(x) + 2
    xMim =  min(x) - 1
    
    plt.xlim(xMim, xMax)

    plt.xticks(rotation = "horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)                                                 
            
    plt.errorbar(x,cdf1, ls='-', label='SUMO',color='tab:orange', zorder=3)
    plt.errorbar(x,cdf2, ls='-', label='Fuzzy',color='tab:green', zorder=3)
            
    #ylabel = 'Cumulative Distribution Function (%)'
    ylabel = 'Função Distribuição Acumulada (%)'
    #xlabel = 'Fuel Consumption (ml/s)'
    if nameFile == 'fuel':
        xlabel = 'Consumo de Combustível (ml/s)'
    else:
        xlabel = 'Velocidade (km/h)'
    #title = 'Cumulative Distribution Function'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")   
    #plt.title(title, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=3)  # ,bbox_to_anchor=(-0.02, 1.15)

    fig.savefig(nameFile+'CDF.png', bbox_inches='tight')
    plt.close(fig)


plotPDF(x,x1,y,y1,'fuel')
plotPDF(x2,x3,y2,y3,'speed')
plotCDF1(x,cdf1,cdf2,'fuel')
plotCDF1(x2,cdf3,cdf4,'speed')