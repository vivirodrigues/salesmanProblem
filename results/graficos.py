from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import xml.dom.minidom
import random
import copy
import matplotlib.pyplot as plt
import matplotlib.markers as plm
import numpy as np
import json
import itertools

class Graficos:

	def __init__(self, nodes,edges,nameFile,X,Y,Z):
		self.name = nameFile			
		self.nodes = nodes
		self.edges = edges			
		self.Z = Z
		self.eixoZ = Z.copy()
		self.X = X
		self.Y = Y
		self.nos = []
		self.eixoX =[]
		self.eixoY =[]

	def setEixos(self):
		x = []
		y = []
		z = []
		for j in range(len(self.eixoZ)):
			if self.eixoZ[j][0] != ":":
				z.append(float(self.eixoZ[j][1]))
				x.append(float(self.X[j][1]))
				y.append(float(self.Y[j][1]))
		
		self.eixoZ = z
		self.eixoX = x
		self.eixoY = y



	def setMetricas(self):
		x = xml.dom.minidom.parse(self.name + '.xml')
		net = x.documentElement			
		tempo = []
		co = []
		co2 = []
		nox = []
		pmx = []
		fuel = []
		lane = []
		child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
		for i in child:
			if i.nodeName == "timestep":
				tempo.append(i.getAttribute('time'))
				emissao = [j for j in i.childNodes if j.nodeType == x.ELEMENT_NODE]
				for j in emissao:
					if j.nodeName == "vehicle":
						if j.getAttribute('lane')[0] != ":":
							id1 = j.getAttribute('id')
							co.append(j.getAttribute('CO'))
							co2.append(j.getAttribute('CO2'))
							nox.append(j.getAttribute('NOx'))
							pmx.append(j.getAttribute('PMx'))
							fuel.append(j.getAttribute('fuel'))
							lan = j.getAttribute('lane')
							# retirar o '_0' do id da via
							palavra = ''
							for c in range(0,len(lan)-2):
								palavra += lan[c]
							lane.append(palavra)

		self.tempo = tempo
		self.id = id1
		self.co = co
		self.co2 = co2
		self.fuel = fuel
		self.lane = lane
		self.nox = nox
		self.pmx = pmx

	def organizaMetricas(self):
		for i in range(len(self.lane)):
			if not 'to' in self.lane[i]:
				del self.lane[i]
				del self.co[i]
				del self.co2[i]
				del self.fuel[i]
				del self.nox[i]
				del self.pmx[i]

	def quantidadeLanes(self):
	    t = []
	    [ t.append(item) for item in self.lane if not t.count(item) ]	    
	    return t

	def somar(self):

		lanes = self.quantidadeLanes()
		co = []
		co2 = []
		fuel = []
		nox = []
		pmx = []
		nos = []
		tempo = []

		for i in lanes:
			somaCO = 0
			somaCO2 = 0
			somaFuel = 0
			somaNOX = 0
			somaPMX = 0
			time = 0

			for j in range(len(self.lane)):				
				if self.lane[j] == i:
					somaCO += float(self.co[j])
					somaCO2 += float(self.co2[j])
					somaNOX += float(self.nox[j])
					somaPMX += float(self.pmx[j])
					somaFuel += float(self.fuel[j])
					for a in range(len(self.lane[j])):
						if self.lane[j][a] == 't':
							position = a
					no = self.lane[j][:position]
					time = float(self.tempo[j])
				if i == lanes[0]:
					tempo.append(int(time))
					nos.append(no)
					co.append(somaCO)
					co2.append(somaCO2)
					nox.append(somaNOX)
					pmx.append(somaPMX)
					fuel.append(somaFuel)
			
			tempo.append(int(time))
			nos.append(no)
			co.append(somaCO)
			co2.append(somaCO2)
			nox.append(somaNOX)
			pmx.append(somaPMX)
			fuel.append(somaFuel)

		tempo.insert(0,0)
		co.insert(0,0)	
		co2.insert(0,0)
		fuel.insert(0,0)
		nox.insert(0,0)
		pmx.insert(0,0)

		self.co = co
		self.co2 = co2
		self.fuel = fuel		
		self.nox = nox
		self.pmx = pmx
		self.nos = nos
		self.tempo = tempo

	def getZ(self):
		
		z = []
		for i in self.nos:
			for j in self.Z:
				if str(i) == str(j[0]):
					z.append(float(j[1]))
		self.Z = z
		self.Z.insert(0,self.Z[0])

		
	def plotCombustivel(self):
		
		y_y_std = []
		
		for i in self.tempo:
			y_y_std.append(0)
	
		fig = plt.figure(1)

		
		xMax = self.tempo[-1] + 5
		xMim = -5
		#plt.yscale('log')
		plt.xlim(xMim, xMax)

		plt.xticks(rotation = "horizontal")

		plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    												
						
		plt.errorbar(self.tempo,self.fuel, ls='solid', label='Combustível',color='blue',yerr=y_y_std, zorder=3)
			
		namePlot = "grafico"
		ylabel = 'Consumo de Combustível (ml/s)'
		xlabel = 'Tempo (s)'		
		title = 'Consumo de Combustível ao longo do tempo - Rota 2' 

		plt.ylabel(ylabel, fontweight="bold")
		plt.xlabel(xlabel, fontweight="bold") 	
		plt.title(title, fontweight="bold")

		plt.legend(numpoints=1, loc="lower right", ncol=4)

		fig.savefig(namePlot+'.png', bbox_inches='tight')
		plt.close(fig)

		return True

	def plotAll(self):
		
		y_y_std = []
		
		for i in self.tempo:
			y_y_std.append(0)
	
		fig = plt.figure(1)

		
		xMax = self.tempo[-1] + 10
		xMim = -10
		plt.yscale('log')
		plt.xlim(xMim, xMax)

		plt.xticks(rotation = "horizontal")

		plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    												
						
		plt.errorbar(self.tempo,self.co, ls='solid', label='CO',color='m',yerr=y_y_std, zorder=3)
		plt.errorbar(self.tempo,self.co2, ls='solid', label='CO2',color='blue',yerr=y_y_std, zorder=3)
		plt.errorbar(self.tempo,self.nox, ls='solid', label='NOx',color='red',yerr=y_y_std, zorder=3)
			
		namePlot = "poluentes"
		ylabel = 'Emissão de poluentes (mg/s)'
		xlabel = 'Tempo (s)'		
		title = 'Emissão de poluentes ao longo do tempo - Rota 2' 

		plt.ylabel(ylabel, fontweight="bold")
		plt.xlabel(xlabel, fontweight="bold") 	
		plt.title(title, fontweight="bold")

		plt.legend(numpoints=1, loc="lower right", ncol=4)

		fig.savefig(namePlot+'.png', bbox_inches='tight')
		plt.close(fig)

		return True

	def g3D(self):
			
		fig = plt.figure(2)
		ax = Axes3D(fig)

		surf = ax.plot_trisurf(self.eixoX, self.eixoY, self.eixoZ, cmap=cm.jet, linewidth=0.2, antialiased=True)
		fig.colorbar(surf, shrink=0.5, aspect=5)
		ax.set_xlabel('x (m)')
		ax.set_ylabel('y (m)')
		ax.set_zlabel('z (m)')		 						 				
		plt.savefig('surface.pdf')
		plt.show()
						

	def run(self):
		self.setMetricas()		
		self.organizaMetricas()
		self.somar()
		self.getZ()
		self.plotAll()
		self.setEixos()
		
