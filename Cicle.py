import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom
import random
import copy
from operator import itemgetter, attrgetter

class Cicle:
	""" Defining a route that runs through all nodes """

	def __init__(self, csvFile, nodes, edges, X, Y, Z):
		self.csv = csvFile
		self.X = X
		self.Y = Y
		self.Z = Z
		self.matrix = []
		self.edges = edges
		self.edgesV = {}
		self.graph = []
		self.keys = []
		self.graphO = []
		self.route = []
		self.nodes = nodes

	def setMatrix(self):
		with open(self.csv + '.csv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			matrix = []
			for row in spamreader:		
				matrix.append(row)
		self.matrix = matrix

	def getMatrix(self):
		return self.matrix

	def validateRoute(self,a,b):
		cost = 0

		for i in range(len(self.matrix)):			
			if str(self.matrix[i][0]) == str(a):								
				initialPoint = i
				for j in range(len(self.matrix[0])):
					if str(self.matrix[0][j]) == str(b):
						finalPoint = j
						cost = self.matrix[initialPoint][finalPoint]					
						if cost == "":						
							return False
						else:
							return True

	def setEdgesV(self):
		for i in self.nodes:
			self.edgesV.update([(i,{})])
			for j in self.nodes:
				if self.validateRoute(i,j) == True:
					item = self.edgesV.get(i)					
					item = list(item)					
					item.append(j)					
					self.edgesV.update([(i,item)])
		self.graph = list(self.edgesV.values())
		self.keys =  list(self.edgesV.keys())		

	def verifyCosts(self,a,b):
		cost = 0

		for i in range(len(self.matrix)):			
			if str(self.matrix[i][0]) == str(a):											
				for j in range(len(self.matrix[0])):
					if str(self.matrix[0][j]) == str(b):												
						cost = self.matrix[i][j]					
		return cost

	
	def order(self):
		order = ()		
		col = []
		graphO = []
		# cria uma lista de tuplas (custo, vizinho) para cada nó de origem
		for i in range(len(self.graph)):			
			lin = []			
			for j in self.graph[i]:
				# verifica-se o custo do nó até o vizinho
				cost = self.verifyCosts(self.keys[i],j)				
				order = (float(cost),j)
				# adiciona a tupla (custo, vizinho) em uma lista
				lin.append(order)
				# re-ordena a lista em ordem crescente de custos
				lin.sort(key=lambda x: x[0])			
			col.append(lin)
		
		# cria uma lista com os vizinhos de cada nó de origem ordenados por custo - ordem crescente
		for i in col:
			lin = []
			for x,y in i:				
				lin.append(y)
			graphO.append(lin)		
		
		self.graphO = graphO

	def dfs(self):
		def dfs_recursiva(grafo, vertice,i):
			visitados.append(vertice)
			for vizinho in grafo[i]:
				if vizinho not in visitados:
					i = self.findIndex(vizinho)
					dfs_recursiva(grafo, vizinho,i)
		visitados = []
		vertice = self.keys[17]
		dfs_recursiva(self.graphO, vertice,17)
		self.route = visitados		
	
	def complete(self):
		rota = self.route.copy()		
		i = 0
		while i != len(rota)-1:		
			if self.validateRoute(rota[i],rota[i+1]) == False:
				subrota = self.greedy(rota[i],rota[i+1])
				j = i + 1
				c = 1
				while j < i + len(subrota):
					rota.insert(j,subrota[c])
					c += 1
					j += 1
			i += 1		
		self.route = rota
	
	def validateRoute(self,a,b):
		cost = 0

		for i in range(len(self.matrix)):			
			if str(self.matrix[i][0]) == str(a):								
				initialPoint = i
				for j in range(len(self.matrix[0])):
					if str(self.matrix[0][j]) == str(b):
						finalPoint = j
						cost = self.matrix[initialPoint][finalPoint]					
						if cost == "":						
							return False
						else:
							return True

	def vizinho(self,inicio,objetivo):		
		adicionados = []				
		adicionados.append(inicio)						

		i = 0
		while adicionados[-1] != objetivo:			
			possibilities = self.edgesV.get(adicionados[i])
			maxi = 100000
			for j in possibilities:
				if int(j) not in adicionados:
					cost = self.verifyCosts(adicionados[i],j)
					if j == objetivo:
						cost = 0										
					if float(cost) < maxi:
						maxi = float(cost)
						choice = j
			if maxi != 100000:
				adicionados.append(int(choice))			
				i = i + 1
			else:
				print("erro")
				break
		
		adicionados
		return adicionados

	def greedy(self,inicio,objetivo):		
		adicionados = []				
		adicionados.append(inicio)						

		i = 0
		while adicionados[-1] != objetivo:			
			possibilities = self.edgesV.get(adicionados[i])
			maxi = 100000
			for j in possibilities:
				if int(j) not in adicionados:
					cost = self.displacement(adicionados[i],j)					
					if j == objetivo:
						cost = 0										
					if float(cost) < maxi:
						maxi = float(cost)
						choice = j
			if maxi != 100000:
				adicionados.append(int(choice))			
				i = i + 1
			else:
				print("erro")
				break
		
		self.route = adicionados
		return self.route

	def displacement(self,i,f):

		xi = 0
		yi = 0
		zi = 0
		xf = 0
		yf = 0
		zf = 0

		for j in range(len(self.nodes)):
			if self.X[j][0] == str(i):
				xi = self.X[j][1]
				yi = self.Y[j][1]
				zi = self.Z[j][1]
			elif self.X[j][0] == str(f):
				xf = self.X[j][1]
				yf = self.Y[j][1]
				zf = self.Z[j][1]

		deltaX = float(xf) - float(xi)
		deltaY = float(yf) - float(yi)
		deltaZ = float(zf) - float(zi)
		deltaR = ((deltaX ** 2) + (deltaY ** 2) + (deltaZ ** 2)) ** 0.5
		
		return deltaR

	def stop(self,lista):
		new = self.removeRepetidosLista(lista)		
		var = 0
		for i in self.edges:
			c = new.count(str(i))			
			if c > 0:
				var += 1
		if var == len(self.edges):			
			return True
		else:
			return False

	def removeRepetidosLista(self,lista):
	    t = []
	    [ t.append(item) for item in lista if not t.count(item) ]	    
	    return t

	def findIndex(self,a):
		for i in range(len(self.keys)):
			if self.keys[i] == a:
				return i	   

	def run(self):		
		self.setMatrix()		
		self.setEdgesV()
		self.order()				
		self.dfs()
		self.complete()				
		return self.route				
