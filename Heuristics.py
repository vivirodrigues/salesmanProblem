import random
import numpy as np
import copy
import csv

class Heuristics:

	def __init__(self, csvFile, nodes,X,Y,Z):
		self.csv = csvFile
		self.matrix = []		
		self.vector = []		
		self.nodes = nodes
		self.edgesV = {}
		self.X = X
		self.Y = Y
		self.Z = Z

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
	
	def getEdgesV(self):
		return self.edgesV

	def verifyCosts(self,a,b):
		cost = 0

		for i in range(len(self.matrix)):			
			if str(self.matrix[i][0]) == str(a):											
				for j in range(len(self.matrix[0])):
					if str(self.matrix[0][j]) == str(b):												
						cost = self.matrix[i][j]					
		return cost

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
					#if j == objetivo:
					#	cost = 0										
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

	def aStar(self,inicio,objetivo):		
		adicionados = []				
		adicionados.append(inicio)
		all1 = 0					

		i = 0
		while adicionados[-1] != objetivo:			
			possibilities = self.edgesV.get(adicionados[i])
			maxi = 100000
			for j in possibilities:
				if int(j) not in adicionados:
					cost1 = self.displacement(adicionados[i],j)
					cost2 = self.verifyCosts(adicionados[i],j)															
					cost = (all1 + float(cost2)) + cost1 # g(n) + h(n)
					if j == objetivo:
						cost = 0					
					if float(cost) < maxi:
						maxi = float(cost)
						choice = j
						currentCost = float(cost2)
			if maxi != 100000:
				adicionados.append(int(choice))	
				all1 += currentCost	
				i = i + 1
			else:
				print("erro")
				break
		
		self.route = adicionados
		return self.route

	def run(self):		
		self.setMatrix()		
		self.setEdgesV()				
		