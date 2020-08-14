import random
from random import randint
import numpy as np
import copy
import csv

class GA:	

	def __init__(self, csvFile, nodes, inicio, destino):
		self.csv = csvFile
		self.matrix = []
		self.n_individuals = 3
		self.population = []
		self.fitness = []
		self.nodes = nodes
		self.edgesV = {}
		self.limit = 10 # generation limit
		self.criterion = False
		self.bestFitness = 0
		self.fitnessDesired = 10000
		self.inicio = inicio
		self.destino = destino

	def setInitialPop(self):
		for i in range(0,self.n_individuals):
			individual = self.aStar(self.inicio,self.destino)
			self.population.append(individual)

	def aStar(self,inicio,destino):		
		adicionados = []				
		adicionados.append(inicio)						

		i = 0
		while adicionados[-1] != destino:			
			possibilities = self.edgesV.get(adicionados[i])
			maxi = 100000
			for j in possibilities:
				if int(j) not in adicionados:
					cost = self.verifyCosts(adicionados[i],j)
					if j == destino:
						cost = 0										
					if float(cost) < maxi:
						maxi = float(cost)
						choice = j
			if maxi != 100000:
				adicionados.append(int(choice))			
				i = i + 1
			else:
				#print("erro")
				return "error"
				break				
		return adicionados


	def setMatrix(self):
		with open(self.csv + '.csv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			matrix = []
			for row in spamreader:		
				matrix.append(row)
		self.matrix = matrix

	def getMatrix(self):
		return self.matrix	

	def verifyCosts(self,a,b):
		cost = 0

		for i in range(len(self.matrix)):			
			if str(self.matrix[i][0]) == str(a):											
				for j in range(len(self.matrix[0])):
					if str(self.matrix[0][j]) == str(b):												
						cost = self.matrix[i][j]					
		return cost

	def calc_fitness(self,vectorIndividual):
		# individual fitness
		len_individual = len(vectorIndividual)	
		cost = 0
		sum1 = 0

		for i in range(len_individual):		
			if i < len_individual-1:		
				cost = self.verifyCosts(vectorIndividual[i],vectorIndividual[i+1])				
				sum1 = sum1 + float(cost)
		
		cost = 1/sum1	
		#print("cost of individual", vectorIndividual, cost)

		return cost

	def setFitnessPopulation(self):
		# population fitness (vector)
		len_pop = len(self.population)	
		fitness = []
		sum1 = 0

		for i in range(len_pop):		
			aptitude = self.calc_fitness(self.population[i])		
			fitness.append(aptitude)	
				
		self.fitness = fitness

	def getFitnessPopulation(self):
		return self.fitness

	def windowing(self):
		# decreases all aptitude values by the minimum value        
	    newList = []
	    min1 = min(self.fitness)
	    for i in range(len(self.fitness)):
	        value = self.fitness[i] - min1
	        newList.append(value)
	    return newList

	def expTransformation(self):
		# exponential transformation
	    newList = []
	    for i in range(len(self.fitness)):
	        value = self.fitness[i] + 1
	        value1 = value ** (1/2)
	        newList.append(value1)
	    return newList


	def linearNormFuction(self):
		# linear normalization
		idSort = np.argsort(self.fitness)	
		N = 20 # increment
		i=0
		for idValue in idSort:
			self.fitness[i] = (idValue)* N + 1
			i=i+1	
		return self.fitness

	def setBestIndividual(self):
		var = self.fitness[0]
		index = 0

		for i in range(len(self.fitness)):		
			if self.fitness[i] > var:			
				var = self.fitness[i]						
				index = i
		
		#print("Best individual:", self.population[index],self.fitness[index])
		self.bestFitness = self.fitness[index]
		self.bestIndividual = self.population[index]
	
	def getBestIndividual(self):	
		return self.bestIndividual

	def roulette(self,randomNumber):
	
		selected = []
		sumAptitude = 0

		# sum of all valued of fitness
		for i in range(len(self.fitness)):
			sumAptitude += self.fitness[i]
		
		# create a list with the probability value about each individual to be selected
		probabilities = []
		
		for i in range(len(self.fitness)):
			probability = self.fitness[i]/sumAptitude
			probabilities.append(probability)	
			
		# sort in ascending order
		probabilities.sort()	

		# verify the interval of random number
		# sum_probabilities == 1 in the end of the loop
		sum_probabilities = 0
		for a in range(len(probabilities)):
			sum_probabilities += probabilities[a]				
			if float(randomNumber) <= sum_probabilities:								
				return self.population[a]


	def selectIndiv(self,amount):
	# select parents for crossover and select individual for mutation		
		quant = 0
		selecteds = []
		indivAlreadyStored = False # to verify if the individual has already been stored

		while quant != amount: # about quantity of individuals must be selected
		
			randomNumber = random.random() # return the next random floating point number in the range [0.0, 1.0)		
			selected = self.roulette(randomNumber) # select one individual by roulette	
			
			if len(selecteds) > 0:
				for j in range(len(selecteds)):					
					if selecteds[j] == selected: # if the individual selected has already been stored
						if self.population[0] == self.population[1] == self.population[2]:# == self.population[3]:						
							indivAlreadyStored = False # if all individual is the same, the loop must be finished with any individual
						else:
							indivAlreadyStored = True
					else:
						indivAlreadyStored = False
				if indivAlreadyStored == False:
					selecteds.append(selected)	
			else:
				selecteds.append(selected)
			quant = len(selecteds)		
			
		if len(selecteds) > 1:
			return selecteds
		elif len(selecteds) == 1: # if it is just one individual, it is not returned inside other list
			return selecteds[0]	

	def mutation(self,individual,typ):
		#print("individual", individual)		
		indiv1 = individual.copy()
		valid = 0
		falg = False
		options = []
		indices = []

		if typ == 1:
			for i in range(1,len(individual)-1):			
				if self.validateRoute(individual[i-1],individual[i+1]) == True: # testa se eh possivel remover algum noh
					valid = i
			if valid != 0: # se for possivel remover um noh
				#print("removing", individual[valid])
				newIndividual = indiv1.remove(individual[valid])
				return newIndividual
		# se n é possivel remover, entao muda o caminho para o mesmo destino
		for i in range(0,len(individual)-2): # n faz sentido substituir o penultimo
			possibilities = self.edgesV.get(individual[i])				
			if len(possibilities) > 1:
				options.append(individual[i])
				indices.append(i)
		#print("options",options)
		#print("indices",indices)
		if len(options) > 0:
			chosen = random.choice(options)
			#print("chosen",chosen)
			indice = options.index(chosen)
			indice1 = indices[indice]
			#print("individuo",individual[indice1])				
			possibilities1 = self.edgesV.get(chosen)
			#print("new possibilities",possibilities1)
			if individual[indice1 + 1] in possibilities1: possibilities1.remove(individual[indice1 + 1]) #possibilities1.remove(individual[indice1 + 1])
			if indice1 > 0 and individual[indice1 - 1] in possibilities1: possibilities1.remove(individual[indice1 - 1])
			#print("new possibilities again",possibilities1)
			if len(possibilities1) > 0:
				newPossib = random.choice(possibilities1)
				newPath = self.aStar(newPossib,self.destino)
				if newPath == "error":
					return individual			
				newIndividual = individual[0:indice1+1] + newPath
				#print("individual", individual)
				#print("new:",newIndividual)
				return newIndividual	
		return individual
	
	def setEdgesV(self):
		for i in self.nodes:
			self.edgesV.update([(i,{})])
			for j in self.nodes:
				if self.validateRoute(i,j) == True:
					#print(i," e", j)			
					item = self.edgesV.get(i)
					#print("item", item)
					#print("set",j)
					item = list(item)
					#print(item)
					item.append(j)
					#new = set(item).union(set(j))
					#print("new", item)
					self.edgesV.update([(i,item)])				
	
	def getEdgesV(self):
		return self.edgesV


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

	def nextGeneration(self):

		#before = copy.deepcopy(self.population)
		points = []
		generation = []				

		# mutation
		amountIndividuals = 2
		typeMutation = 1 # sequencial swap
		selected = self.selectIndiv(amountIndividuals)		
		for a in range(amountIndividuals):
			mutated = self.mutation(selected[a], typeMutation)	
			generation.append(mutated)
		
		# best individual	
		bestIndiv = self.setBestIndividual()
		#print("Best individual from last generation:", self.getBestIndividual())
		generation.append(self.getBestIndividual())		
		
		#e = self.adjustVector(generation)
		self.population = generation

	def run(self):
		gen = 0
		self.setMatrix()		
		self.setEdgesV()
		#print(self.matrix)		
		self.setInitialPop()
		#print(len(self.population))
		print("Population", self.population)
		#self.adjustVector(self.population) # initial population
		while self.criterion != True:
			self.setFitnessPopulation()
			#print(self.fitness)
			self.nextGeneration()
			print(self.population)
			if gen == self.limit:
				self.criterion = True
			elif self.bestFitness == self.fitnessDesired:
				self.criterion = True
			gen += 1
		print("The best route is:", self.getBestIndividual())
		return self.getBestIndividual()
