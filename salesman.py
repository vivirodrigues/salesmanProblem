import random
import numpy as np
import copy
import csv


with open('distances.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	matriz = []
	for row in spamreader:		
		matriz.append(row)	

def print_matrix(M):  
  for lin in M:
    print(" ".join([str(i) for i in lin]))

def completeMatrix(matrix):
	for i in range(len(matrix)):		
		initialPoint = matrix[i][0]
		for j in range(len(matrix[0])):	
			finalPoint = matrix[0][j]		
			if matrix[i][j] == "":
				cost = matrix[j][i]				
				if cost == "":
					cost = 0
				matrix[i][j] = cost
	#print_matrix(matrix)
	return matrix	

def getPossibilities(matrix):
	
	possibilites = []

	for j in range(len(matrix[0])):	
		if matrix[0][j]!= 0:
			possibilites.append(matrix[0][j])

	return possibilites

def replaceCities(population):
	newPop = []
	newVector = []

	for lin in range(len(population)):
		vectorCities = population[lin]		
		for i in range(len(vectorCities)):		
			if vectorCities[i] == 1:
				population[lin][i] = 'A'
			elif vectorCities[i] == 2:
				population[lin][i] = 'B'
			elif vectorCities[i] == 3:
				population[lin][i] = 'C'
			elif vectorCities[i] == 4:
				population[lin][i] = 'D'
			elif vectorCities[i] == 5:
				population[lin][i] = 'E'

	return population	

def verifyCosts(matrix,initial,final):
	
	cost = 0

	for i in range(len(matrix)):
		if matrix[i][0] == initial:
			initialPoint = i
			for j in range(len(matrix[0])):
				if matrix[0][j] == final:
					finalPoint = j
					cost = matrix[initialPoint][finalPoint]					
					if cost == "":						
						cost = 0	
	return cost

def calc_aptitude(matrix,vectorIndividual):
	
	len_individual = len(vectorIndividual)	
	cost = 0
	sum1 = 0

	for i in range(len_individual):		
		if i < len_individual-1:		
			cost = verifyCosts(matrix,vectorIndividual[i],vectorIndividual[i+1])			
			sum1 = sum1 + float(cost)
		
	cost = 1/sum1	
	#print("Cost of individual ", vectorIndividual,": ", cost)

	return cost

def fitnessPopulation(matrix,population):
	
	len_pop = len(population)	
	fitness = []
	sum1 = 0

	for i in range(len_pop):
		
		aptitude = calc_aptitude(matrix,population[i])		
		fitness.append(aptitude)	
		
	return fitness

# decreases all aptitude values by the minimum value
def windowing(fitness):
        
    newList = []
    min1 = min(fitness)
    for i in range(len(fitness)):
        value = fitness[i] - min1
        newList.append(value)
    return newList

# exponential transformation
def expTransformation(fitness):

    newList = []

    for i in range(len(fitness)):
        value = fitness[i] + 1
        value1 = value ** (1/2)
        newList.append(value1)
    return newList

# linear normalization
def linearNormFuction(fitness):
	
	idSort = np.argsort(fitness)	
	N = 20 # increment
	i=0

	for idValue in idSort:
		fitness[i] = (idValue)* N + 1
		i=i+1	
	
	return fitness

def bestIndividual(fitness,population):
		
	var = fitness[0]
	index = 0

	for i in range(len(fitness)):		
		if fitness[i] > var:			
			var = fitness[i]						
			index = i
	
	#print("Best individual: ", aptitude[indice])
	return population[index]

def roulette(aptitude,randomNumber,population):
	
	selected = []
	sumAptitude = 0

	# sum of all valued of aptitude
	for i in range(len(aptitude)):
		sumAptitude += aptitude[i]
	
	# create a list with the probability value about each individual to be selected
	probabilities = []
	
	for i in range(len(aptitude)):
		probability = aptitude[i]/sumAptitude
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

# select parents for crossover and select individual for mutation
def selectIndiv(aptitude,amount,population):
		
	quant = 0
	selecteds = []
	indivAlreadyStored = False # to verify if the individual has already been stored

	while quant != amount: # about quantity of individuals must be selected
	
		randomNumber = random.random() # return the next random floating point number in the range [0.0, 1.0)		
		selected = roulette(aptitude,randomNumber,population) # select one individual by roulette	
		
		if len(selecteds) > 0:
			for j in range(len(selecteds)):					
				if selecteds[j] == selected: # if the individual selected has already been stored
					if population[0] == population[1] == population[2] == population[3]:						
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
	
	newAllele = random.randrange(minAllele, maxAllele+1, 1)
	newLocus = random.randrange(0, len(vector), 1)
	vector[newLocus] = newAllele
	
	return vector

# 1 : swap mutation
# 2 : seq swap
def mutation(individual, points, typ):
	
	if typ == 1:
		
		#print("Individual before swap mutation:", individual)	
		newIndividual = []
		value1 = individual[points[0]]
		value2 = individual[points[1]]

		for i in range(len(individual)):
			if i == points[0]:
				newIndividual.append(value2)
			elif i == points[1]:
				newIndividual.append(value1)
			else:
				newIndividual.append(individual[i])
		
		#print("Individual after swap mutation:", newIndividual)

		return newIndividual
	
	# seq swap
	elif typ == 2:
		
		#print("Individual before swap mutation:", individual)
		points.sort()		
		newIndividual = []		
		a1 = []
		a2 = []
		a3 = []

		for i in range(len(individual)):
			if i <= points[0]:
				a1.append(individual[i])
			elif i < points[1]:
				a2.append(individual[i])
			else:
				a3.append(individual[i])
			
		newIndividual = a3 + a2 + a1
		#print("Individual after swap mutation:", newIndividual)

		return newIndividual

def recombinationCrossover(parents,points):
	
	child1 = []
	child2 = []
	father1 = parents[0]
	father2 = parents[1]

	if len(points) == 1:
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
	
	elif len(points) == 2:

		for i in range(len(father1)):
			if i <= points[0]:
				child1.append(father1[i])								
				child2.append(father2[i])
			elif i <= points[1]:
				child1.append(father2[i])								
				child2.append(father1[i])
			else:
				child1.append(father1[i])								
				child2.append(father2[i])

	return child1,child2

def adjustVector(population,possibilities):

	newPop = []			
	repeated = []
	missing = []	
	len_individual = 0
	
	for i in range(len(population)):
		vectorIndividual = population[i]
		len_individual = len(vectorIndividual)
		for j in range(len(possibilities)):
			if vectorIndividual.count(possibilities[j]) < 1:
				missing.append(possibilities[j])
			elif vectorIndividual.count(possibilities[j]) > 1:			
				repeated.append(possibilities[j])

		vectorIndividual = replace(vectorIndividual,missing,repeated)
		newPop.append(vectorIndividual)

	return newPop
	

def replace(vectorIndividual,missing,repeated):
			
	for i in range(len(vectorIndividual)):		
		for j in range(len(repeated)):
			if vectorIndividual[i] == repeated[j] and len(missing)>0:
				var = random.choice(missing)			
				vectorIndividual[i] = var
				missing.remove(var)				
		
	return vectorIndividual

def nextGeneration(fitness, lastGen):

	before = copy.deepcopy(lastGen)
	points = []
	generation = []
	length = len(fitness)
	points.append(random.randrange(0, length, 1))
	points.append(random.randrange(0, length, 1))
	
	# crossover
	amountParents = 2
	selecteds = selectIndiv(fitness,amountParents,lastGen)
	#print("Selected individuals for crossover:",selecteds)
	children = recombinationCrossover(selecteds,points)
	#print("Children:", children)
	generation.append(children[0])
	generation.append(children[1])

	# mutation
	amountIndividuals = 1
	typeMutation = 2 # sequencial swap
	selected = selectIndiv(fitness,amountIndividuals,lastGen)
	#mutated = generativeFunction(selected,0,7)
	#print("Selected individual(s) for mutation:", selected)
	mutated = mutation(selected, points, typeMutation)	
	generation.append(mutated)
	
	# best individual	
	bestIndiv = bestIndividual(fitness,before)
	#print("Best individual from last generation:", bestIndiv)
	generation.append(bestIndiv)

	return generation

###################################################################################################

if __name__ == '__main__':

	matrix = completeMatrix(matriz) # complete matrix csv
	possibilities = getPossibilities(matrix) # it depends on table (csv)
	#print("Possibilities",possibilities)
	
	populationInitial = [[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[1,2,4,3,5]]
	population = replaceCities(populationInitial)
	#print("Initial population:", population)			
	
	limit = 200
	end = False
	generation = 1
	
	while end != True:

		fitnessPop = fitnessPopulation(matrix,population)
		#linear = linearNormFuction(fitnessPop)
		#aptitudeWindow = windowing(fitnessPop)	
		#aptitudeExpTransf = expTransformation(aptitudeWindow)			
		nextGen = nextGeneration(fitnessPop,population)				
		population = adjustVector(nextGen,possibilities)		

		if 	fitnessPop[3]==1/11:
			print("You got it")					
			end = True		

		if generation > limit:
			print("Limit of generations reached")
			end = True		
					
		result = population[3]

		generation += 1

	print("Generation",generation)
	print("Result: ", result, "Aptitude:", fitnessPop[3])
