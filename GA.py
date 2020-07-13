import random
import numpy as np
import copy
import csv

class GA:

	def __init__(self, csvFile):
		self.csv = csvFile
		self.matrix = []

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

  def run(self):
		self.setMatrix()				
