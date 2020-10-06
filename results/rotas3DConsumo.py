from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import xml.dom.minidom
import random
import copy
import matplotlib.markers as plm
import numpy as np
import itertools
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

rotas = ['rotas2']
a = ['fuel1F','fuel2F','fuel3F']
b = ['fuelBFS']
c = ['mapBFS']#,'mapAstar','mapGA']
d = ['speed1F','speed2F','speed3F','speed1S','speed2S','speed3S']
#arquivo = 'Empirical_Probability_Density'

""" Map """
x = []
yx = []
yy = []
yz = []
yAngle = []

a2 = []
a1 = []
a3 = []
a4 = []

for i in c:
    #print("entrou aqui")
    with open('PDF/'+ i+'.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    x.append(np.array(list(map(int,data.keys()))))
    data = list(data.values())
    for j in data:
        a1.append(j.get('x'))
        a2.append(j.get('z'))
        a3.append(j.get('angle'))
        a4.append(j.get('y'))
    yx.append(np.array(list(a1)))
    #yx.append(list(a1))
    yy.append(np.array(list(a4)))
    #yy.append(list(a4))
    yz.append(np.array(list(a2)))
    #yz.append(list(a2))
    yAngle.append(np.array(list(a3)))

""" Fuel """
x = []
y = []
total = []
time = []
total1 = []

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

def plotTotal1(total, total2, nameFile):    
    print(total)
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

    z = total2[0]
          
    #maximo = max(max(y1),max(y),max(y2),max(y3))
    fig = plt.figure(figsize=(50,5))
    #plt.ylim(0, maximo+4) 
    plt.xlim(limInf, limSup)
    #plt.yscale('log', nonposy='clip')      
        
    #plt.bar(x - 0.59*space, y, label='BFS Fuzzy', color='tab:blue', width=0.1)
    plt.bar(x, z, label='BFS SUMO', color='darkblue', width=0.1)
    #plt.bar(x - 0.26*space, y1, label='DFS Fuzzy', color='tab:orange', width=0.1)
    #plt.bar(x - 0.1*space, z1, label='DFS SUMO', color='lightsalmon', width=0.1)        
    #plt.bar(x + 0.072*space, y2, label='A-star Fuzzy', color='tab:green', width=0.1)
    #plt.bar(x + 0.24*space, z2, label='A-star SUMO', color='darkgreen', width=0.1)
    #plt.bar(x + 0.39*space, y3, label='AG Fuzzy', color='tab:red', width=0.1)      
    #plt.bar(x + 0.54*space, z3, label='AG SUMO', color='darkred', width=0.1)      
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

def plotMap(x,yx,yz,nameFile):
    print("x",x)
    print("yx",yx)
    print("yz",yz)
    
    fig = plt.figure(figsize=(50,5))
    
    yMax = max(yz) + 20
    yMim =  min(yz) - 5

    xMax = max(x) + 2
    xMim =  min(x) - 1
    
    plt.xlim(xMim, xMax)
    plt.ylim(yMim, yMax)

    new = []
    for i in range(0,len(x)+2,20):      
        new.append(int(i))
    
    plt.xticks(new)

    #plt.xticks(rotation = "horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)                                                 
            
    plt.errorbar(x,yz, ls='-', label='SUMO',color='blue', zorder=3)
    #plt.errorbar(x[0],cdf2, ls='-', label='Fuzzy',color='green', zorder=3)
            
    #ylabel = 'Cumulative Distribution Function (%)'
    ylabel = 'Inclinação'
    #xlabel = 'Fuel Consumption (ml/s)'
    if nameFile == 'fuel':
        xlabel = 'Consumo de Combustível (ml/s)'
    else:
        xlabel = 'Distância (m)'
    #title = 'Cumulative Distribution Function'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")   
    #plt.title(title, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=3)  # ,bbox_to_anchor=(-0.02, 1.15)

    fig.savefig(nameFile+'1.png', bbox_inches='tight')
    plt.close(fig)

def g3D(x1,y1,z1):
            
        fig = plt.figure(2)
        ax = Axes3D(fig)

        surf = ax.plot_trisurf(x1, y1, z1, cmap=cm.jet, linewidth=0.2, antialiased=True)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_zlabel('z (m)')                                              
        plt.savefig('map.png')
        plt.show()

plotTotal1(list(x[0]),total,'fuelSumo')
#plotMap(x[0],yx[0],yz[0],'Map1')
#print(len(yx[0]))
#print(len(yy[0]))
#print(len(yz[0]))
#g3D(yx[0],yy[0],yz[0])
