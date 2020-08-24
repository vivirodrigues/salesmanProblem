import random
from random import randint
import numpy as np
import copy
import csv
import ConsumptionModel as cM
import fuzzy
import math
import mainS
import Map
import json
import bfs

class GA:	

	def __init__(self, csvFile, nodes, edges,inicio, destino, X, Y, Z):
		self.csv = csvFile
		self.matrix = []
		self.n_individuals = 7
		self.population = []
		self.fitness = []
		self.nodes = nodes
		self.edges = edges
		self.edgesV = {} #edges vizinhas
		self.limit = 5 # generation limit
		self.criterion = False
		self.bestFitness = 0
		self.fitnessDesired = 10000
		self.inicio = inicio
		self.destino = destino
		self.f_2 = fuzzy.Algorithm()
		self.map = Map.Map('SUMO2/map') # net file
		self.map.run()
		self.X = X
		self.Y = Y
		self.Z = Z
		self.totalFit = []
		self.totalPop = []
		self.bfs = bfs.Graph()

	def vizinho(self,inicio,objetivo):		
		adicionados = []				
		adicionados.append(inicio)
		print(self.edgesV)					

		i = 0
		while adicionados[-1] != objetivo:			
			possibilities = self.edgesV.get(str(adicionados[i]))			
			print("poss",possibilities,adicionados[i])
			maxi = 100000
			for j in possibilities:
				if str(j) not in adicionados:
					cost = self.verifyCosts(adicionados[i],j)
					if j == objetivo:
						cost = 0										
					if float(cost) < maxi:
						maxi = float(cost)
						choice = j
			if maxi != 100000:
				adicionados.append(str(choice))			
				i = i + 1
			else:
				print("erro")
				break
		
		return adicionados
		#return self.route

	def setInitialPop(self):
		for i in range(0,self.n_individuals):
			individual = self.h_bfs(self.inicio,self.destino)
			#individual = self.vizinho(self.inicio,self.destino)
			self.population.append(individual)	
	
	def h_bfs(self,inicio,objetivo):		
		rota = self.bfs.run(inicio,objetivo,self.nodes,self.edges)		
		return rota

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

	def cfitness(self,vectorIndividual):
		print("indi",vectorIndividual)
		edgesIndividual = self.map.getListEdges(vectorIndividual)
		print("edges",edgesIndividual)		
		consumption = mainS.main(edgesIndividual)		
		return consumption		

	def setFitnessPopulation(self,population):
		# population fitness (vector)
		len_pop = len(population)	
		fitness = []
		sum1 = 0

		for i in range(len_pop):		
			aptitude = self.cfitness(population[i])		
			fitness.append(aptitude)	
				
		return fitness
		

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

	def setBestIndividual(self,population):
		
		fit = self.setFitnessPopulation(population)		
		var = fit[0]
		index = 0

		for i in range(len(fit)):		
			if fit[i] < var:			
				var = fit[i]						
				index = i
		
		#print("Best individual:", self.population[index],self.fitness[index])
		self.bestFitness = fit[index]
		self.bestIndividual = population[index]
	
	def getBestIndividual(self):	
		return self.bestIndividual

	def roulette(self,randomNumber,population,fitness):
	
		selected = []
		sumAptitude = 0

		# sum of all valued of fitness
		for i in range(len(fitness)):
			sumAptitude += fitness[i]
		
		# create a list with the probability value about each individual to be selected
		probabilities = []
		
		for i in range(len(fitness)):
			probability = fitness[i]/sumAptitude
			probabilities.append(probability)	
			
		# sort in ascending order
		probabilities.sort()	

		# verify the interval of random number
		# sum_probabilities == 1 in the end of the loop
		sum_probabilities = 0
		for a in range(len(probabilities)):
			sum_probabilities += probabilities[a]				
			if float(randomNumber) <= sum_probabilities:								
				return population[a]


	def selectIndiv(self,amount,population,fitness):
	# select parents for crossover and select individual for mutation

		quant = 0
		selecteds = []
		indivAlreadyStored = False # to verify if the individual has already been stored

		while quant != amount: # about quantity of individuals must be selected
		
			randomNumber = random.random() # return the next random floating point number in the range [0.0, 1.0)		
			selected = self.roulette(randomNumber,population,fitness) # select one individual by roulette	
			
			if len(selecteds) > 0:
				for j in range(len(selecteds)):					
					if selecteds[j] == selected: # if the individual selected has already been stored
						if population[0] == population[1] == population[2]:# == self.population[3]:						
							indivAlreadyStored = False # if all individual is the same, the loop must be finished with any individual
						else:
							indivAlreadyStored = True
					else:
						indivAlreadyStored = False
				if indivAlreadyStored == False:
					selecteds.append(selected)
				else:
					print("a")	
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
				newPath = self.h_bfs(newPossib,self.destino)
				if newPath == "error":
					return individual			
				newIndividual = individual[0:indice1+1] + newPath
				#print("individual", individual)
				#print("new:",newIndividual)
				return newIndividual	
		return individual

	def crossover(self,individual1,individual2):
		
		ind1 = individual1.copy()
		ind2 = individual2.copy()

		if len(ind1) > 2 and len(ind2) > 2:
			ind1.remove(ind1[-1])
			ind1.remove(ind1[0])
			ind2.remove(ind2[-1])
			ind2.remove(ind2[0])

			child1 = []
			child2 = []
			temp1 = []
			temp2 = []

			a = random.choice(ind1)
			print("chosen",a)
			index1 = individual1.index(a)
			b = random.choice(ind2)
			print("chosen",b)
			index2 = individual2.index(b)

			child1 = individual1[0:index1]
			temp2 = individual1[index1:]			

			child2 = individual2[0:index2]
			temp1 = individual2[index2:]			

			child1 = child1 + temp1
			child2 = child2 + temp2

			child1 = self.correct(child1)
			child2 = self.correct(child2)										

			print("1",child1,"2",child2)
			return child1,child2			
	
	def setEdgesV(self):
		for i in self.nodes:
			self.edgesV.update([(i,{})])
			for j in self.nodes:
				if self.validateRoute(i,j) == True:
					item = self.edgesV.get(i)
					item = list(item)
					item.append(j)
					self.edgesV.update([(i,item)])

	def setEdgesV1(self):
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

	def validatePop(self,population):
		errors = [] # index of wrong individuals
		for i in range(len(population)):
			test = self.validateInd(population[i])
			if test == False:
				errors.append(i)		
		return errors

	def validateInd(self,individual):
		flag = True
		repeated = self.setRepeated(individual)
		if len(repeated) > 0:
			flag = False
		else:
			for i in range(len(individual)-1):
				test = self.validateRoute(individual[i],individual[i+1])
				if test == False:
					flag = False
		return flag

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

	def correct(self,individual):		
		indices = []
		repeated = []
		flag = False
		alell = len(individual)-1

		##### se o individuo não vai até o destino
		if individual[-1] != self.destino:
			newPath = self.h_bfs(individual[-1],self.destino)
			if newPath == "error":
				while alell > 0 and flag == False:
					newPath = self.h_bfs(individual[alell],self.destino)
					if newPath != "error":
						individual = individual[:alell] + newPath
						flag = True
					alell -= 1
				print("O individuo eh", individual)
			else:
				individual = individual + newPath[1:]
				print("Deu certo de cara", individual)

		##### se o individuo não começa no inicio
		flag = False
		alell = 1
		if individual[0] != self.inicio :
			newPath = self.h_bfs(self.inicio,individual[0])
			if newPath == "error":
				while alell < len(individual)-1 and flag == False:
					newPath = self.h_bfs(self.inicio,individual[alell])
					if newPath != "error":
						individual = newPath + individual[alell:]
						flag = True
					alell += 1
				print("O individuo eh haha", individual)
			else:
				individual = newPath + individual
				print("Deu certo de cara", individual)

		##### se tem dois genes que não estão conectados				
		#for i in range(0,len(individual)-2):
		i = 0
		flag = False
		alell = 0	
		while i < len(individual) - 1:
			if self.validateRoute(individual[i],individual[i+1]) == False:
				print("entrou aqui em",individual[i],individual[i+1])
				print("entrou aqui em",individual)
				possibilities = self.edgesV.get(individual[i])				
				if len(possibilities) > 0:
					chosen = random.choice(possibilities)
					newPath = self.h_bfs(chosen,self.destino)
					#print("new path", newPath)
					if newPath == "error":								
						
						while alell < i and flag == False:
							newPath = self.h_bfs(individual[alell],individual[i+1])
							print("nP",newPath)
							if newPath != "error":
								individual = individual[:alell] + newPath + individual[i+1:]
								print("O individuo ehhhhh", individual)
								flag = True
							alell += 1
						if flag == False:
							print("AAAAAAAAAAAAa")
							print(self.inicio,self.destino)							
							individual = self.h_bfs(self.inicio,self.destino)
						"""
						individual = self.h_bfs(self.inicio,self.destino)
						print("O individuo eh", individual)
						"""
					else:							
						individual = individual[:i+1] + newPath
						print("Deu certo de cara", individual)
			i += 1
				

		##### retirar genes repetidos
		repeated = self.setRepeated(individual)
		print("repeated",repeated)
		while len(repeated) > 0:
			new = []
			indices = [i for i, x in enumerate(individual) if x == repeated[0]]
			for j in range(len(individual)):				
				if j >= indices[0] and j < indices[-1]:
					pass
				else:
					new.append(individual[j])
			individual = new
			repeated = self.setRepeated(individual)

		# se tem repetido um do lado do outro
		n = 0
		while n < len(individual) - 1:			
			if individual[n] == individual[n+1]:
				individual.remove(individual[n])
			n += 1

		#print("indiv",individual)
		return individual
		
	def setRepeated(self,individual):
		repeated = []
		for i in range(0,len(individual)):
			if individual.count(str(individual[i])) > 1:
				repeated.append(str(individual[i]))
		return repeated

	def writeJson(self,content,file):
		with open(file+'.txt', 'w') as json_file:
  			json.dump(content, json_file)

	def nextGeneration(self):

		before = copy.deepcopy(self.population)		
		self.totalPop.append(before)
		points = []
		generation = []				

		# mutation
		amountIndividuals = 4
		typeMutation = 1
		selected = self.selectIndiv(amountIndividuals,before,self.fitness)		
		for a in range(amountIndividuals):
			mutated = self.mutation(selected[a], typeMutation)	
			generation.append(mutated)

		# crossover
		amountIndividuals = 2
		selected = self.selectIndiv(amountIndividuals,before,self.fitness)		
		for a in range(0,amountIndividuals,2):			
			child1,child2 = self.crossover(selected[a], selected[a+1])			
			generation.append(child1)
			generation.append(child2)
		
		
		# best individual	
		bestIndiv = self.setBestIndividual(before)
		#print("Best individual from last generation:", self.getBestIndividual())		
		generation.append(self.getBestIndividual())		
		
		errors = self.validatePop(generation)		
		if len(errors) < 1:
			self.population = generation
		else:
			generation1 = []
			new = []
			for j in range(len(generation)):
				print("antes", generation[j])
				new = self.correct(generation[j])
				print("depois", new)
				generation1.append(new)
				self.population = generation1

	def run(self):
		gen = 0
		self.setMatrix()		
		self.setEdgesV1()
		print(self.edgesV)		
		"""
		self.setInitialPop()
		#print(self.population)
		
		initial = self.population.copy()	
		#print("Population", self.population)
		while self.criterion != True:
			fitness = self.setFitnessPopulation(self.population)
			self.fitness = fitness
			self.totalFit.append(fitness)						
			self.nextGeneration()								
			if gen == self.limit:
				self.criterion = True				
			#elif self.bestFitness == self.fitnessDesired:
			#	self.criterion = True
			gen += 1
		print("initial pop", initial)
		print("Fitness last gen", self.fitness)
		print("The best route is:", self.getBestIndividual())
		self.writeJson(self.totalFit,'fitness')
		self.writeJson(self.totalPop,'population')
		return self.getBestIndividual()
		"""