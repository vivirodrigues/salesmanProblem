import random
from random import randint
import numpy as np
import copy
import csv

class GA:
	"""	

	Do ponto a ate o d
	pop1 = [a c b d]		fitness = 12
	pop2 = [a c d]			fitness = 15
	pop3 = [a e i d]		fitness = 10

	pop1 + pop3 = [a c i d] -> [a i d] or [a c e i d]
	pop1 mutaded = [a b d] or [a c b e d]


	"""

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
		"""for i in range(0,self.n_individuals):
			result = []
			while len(result) != len(self.nodes):
				r = randint(0, len(self.nodes)-1)
				if r not in result:
					result.append(r)
			self.population.append(result)
		"""
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

	def getAngle(self,i,f):
		xi = 0
		yi = 0
		zi = 0
		xf = 0
		yf = 0
		zf = 0
		
		for j in range(len(self.X)):
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
		tan = deltaZ/deltaX		
		angle = math.degrees(math.atan(tan))
		
		return angle

	def calculate_real_fuel(self,speed,accel,slope):
	    modelo = cM.ModelConsumption(speed, accel, slope)
	    consumption = modelo.run()
	    instant_fuel = consumption
	       
	    return instant_fuel

	def fitness1(self,vectorIndividual):
		angle = 0
		inf10 = 0
		consumption = 0
		accel = 0
		time = 0

		for i in range(0,len(vectorIndividual)-1):
			angle = self.getAngle(vectorIndividual[i],vectorIndividual[i+1]) # ok sumo
			print("slope",angle)		
			length = self.displacement(vectorIndividual[i],vectorIndividual[i+1])									
			speed = 27.52#self.f_2.findSpeed(angle, inf10)			
			time = 7		
			for j in range(int(time)):
				consumption += self.calculate_real_fuel(speed,accel,angle)
				print(consumption)

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

	def generativeFunction(vector, minAllele, maxAllele):
		# mutation
		newAllele = random.randrange(minAllele, maxAllele+1, 1)
		newLocus = random.randrange(0, len(vector), 1)
		vector[newLocus] = newAllele
	
		return vector

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
			
	def recombination(self,parents,typ):
	
		child1 = []
		child2 = []
		father1 = parents[0]
		father2 = parents[1]
		f1 = father1.remove(father1[-1])
		f1 = father1.remove(father1[0])
		f2 = father2.remove(father2[-1])
		f2 = father2.remove(father2[0])

		if typ == 1:
			intersec = set(f1).intersection(set(f2))
			if intersec > 0:
				intersec = list(intersec)
				chosen = random.choice(intersec)

		for i in range(len(father1)):
			if i <= points:
				child1.append(father1[i])			
			else:			
				child2.append(father1[i])
		
		for i in range(len(father2)):
			if i <= points:
				child2.append(father2[i])
			else:
				child1.append(father2[i])
				

		return child1,child2

	def adjustVector(self,population):

		newPop = []			
		repeated = []
		missing = []	
		len_individual = 0
		
		for i in range(len(population)):
			repeated = []
			missing = []
			vectorIndividual = population[i]
			len_individual = len(vectorIndividual)
			for j in range(len(self.nodes)):
				if vectorIndividual.count(int(self.nodes[j])) < 1:
					missing.append(int(self.nodes[j]))
				elif vectorIndividual.count(int(self.nodes[j])) > 1:					
					repeated.append(int(self.nodes[j]))

			vectorIndividual = self.complete(vectorIndividual,missing,repeated)
			newPop.append(vectorIndividual)

		return newPop

	def complete(self,vectorIndividual,missing,repeated):		
		for i in range(len(vectorIndividual)):		
			for j in range(len(repeated)):
				if str(vectorIndividual[i]) == str(repeated[j]) and len(missing)>0:
					var = random.choice(missing)			
					vectorIndividual[i] = var
					missing.remove(var)						
		vectorIndividual = self.replace(vectorIndividual)
		return vectorIndividual

	
	def replace(self, individual):	
		adicionados = []
		for i in range(0,len(individual)-1):
			modif = False
			if self.validateRoute(individual[i],individual[i+1]) == False: # se o primeiro e o segundo n estiverem ok
				possibilities = self.edgesV.get(str(individual[i])) # vê com quem o primeiro se conecta
				if len(possibilities) > 0:
					print("a",individual[i])
					print(possibilities)
					z = 0
					while modif == False:
						var = random.choice(list(possibilities)) # escolhe aleatoriamente uma conexao p o 1º						
						"""#print("var", var)
						z += 1
						if z > 5 and i > 1:
							rem1 = adicionados.pop()
							print(rem1,"removido")
							rem2 = adicionados.pop()
							print(rem2,"removido")
							print(i)
							i -= 2
							modif = True
						else:"""
						for j in range(len(individual)): # procura esse nó no individuo							
							if str(individual[j]) == str(var) and int(var) not in adicionados:
								#print("var", var)
								#print(str(var) not in adicionados)
								individual[j] = individual[i+1] # nó é substituido
								individual[i+1] = int(var) # completa o swap
								adicionados.append(individual[i])
								modif = True						
				else:
					print(individual[i])
					print(possibilities)
			print("adicionados",adicionados)
		return individual
	"""

	def replace(self, individual):
		new = []
		i = 0
		while len(new) != len(individual):			
			new.append(individual[i])
			if self.validateRoute(individual[i],individual[i+1]) == True: # se o primeiro e o segundo estiverem ok
				pass
			else:
				possibilities = self.edgesV.get(str(individual[i])) # vê com quem o primeiro se conecta
				print(individual[i])
				print(possibilities)
				if len(possibilities) > 0:
					var = random.choice(list(possibilities)) # escolhe aleatoriamente uma conexao p o 1º
					if var not in new:
						print("var",var)
						for j in range(i+1,len(individual)): # procura esse nó no individuo
							if str(individual[j]) == str(var):
								print("entrou aq")
								individual[j] = individual[i+1] # nó é substituido
								individual[i+1] = int(var) # completa o swap
								i += 1								
					else:
						print("entrou aqui com", new)
						for j in range(len(individual)): # procura esse nó no individuo
							if str(individual[j]) == str(var):
								individual[j] = individual[i+1] # nó é substituido
								individual[i+1] = int(var) # completa o swap
								new.remove(var)
								i += 1
				else:
					print("poss - 1",individual[i])
			#i += 1
			if i == len(individual)-1:
				i = 0
			#print(new)
		return new
	
	"""
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
		length = len(self.fitness)
		#points.append(random.randrange(0, length, 1))
		#points.append(random.randrange(0, length, 1))
		
		""" crossover
		amountParents = 2
		selecteds = self.selectIndiv(amountParents)
		#print("Selected individuals for crossover:",selecteds)
		children = self.recombinationCrossover(selecteds,points)
		#print("Children:", children)
		generation.append(children[0])
		generation.append(children[1]) """

		# mutation
		amountIndividuals = 2
		typeMutation = 1 # sequencial swap
		selected = self.selectIndiv(amountIndividuals)
		#print("Selected",selected)
		#mutated = generativeFunction(selected,0,7)
		#print("Selected individual(s) for mutation:", selected)
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
		
				
		