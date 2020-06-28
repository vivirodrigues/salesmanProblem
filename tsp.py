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

	return matrix	

def getPossibilities(matrix):
	
	possibilites = []

	for j in range(len(matrix[0])):	
		if matrix[0][j]!= 0:
			possibilites.append(matrix[0][j])

	return possibilites

def replaceCities(path):

	newPop = []
	newVector = []

	for lin in range(len(path)):
		vectorCities = path[lin]		
		for i in range(len(vectorCities)):		
			if vectorCities[i] == 1:
				path[lin][i] = 'A'
			elif vectorCities[i] == 2:
				path[lin][i] = 'B'
			elif vectorCities[i] == 3:
				path[lin][i] = 'C'
			elif vectorCities[i] == 4:
				path[lin][i] = 'D'
			elif vectorCities[i] == 5:
				path[lin][i] = 'E'

	return path

if __name__ == '__main__':

	matrix = completeMatrix(matriz) # complete matrix csv
	possibilities = getPossibilities(matrix) # amount of cities, it depends on table (csv)
	print_matrix(matrix)
