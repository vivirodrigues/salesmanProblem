import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom

class Matrix:
	""" Defining edges and nodes based on the matrix """

	def __init__(self, nameMatrix):
		self.name = nameMatrix		
		self.matrix = []
		self.points = []
		self.edges = []
		self.costs = []
		self.dictCosts = {}

	def setMatrix(self):
		with open(self.name + '.csv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			matrix = []
			for row in spamreader:		
				matrix.append(row)
			self.matrix = matrix	
	
	def getMatrix(self):
		return self.matrix

	def setPoints(self):
		if len(self.matrix) > 0:
			points = []
			for j in range(len(self.matrix[0])):	
				if self.matrix[0][j]!= 0:				
					points.append(self.matrix[0][j])

			self.points = points
		else:
			print("Matriz não identificada")

	def getPoints(self):
		return self.points

	def setEdges(self):
		if len(self.points) > 0:
			for i in range(1,len(self.matrix)):				
				for j in range(1,len(self.matrix[0])): 
					# there is a cost between these edges?
					if self.matrix[i][j] != "":
						# if exists a cost between these edges, there is a path between then			
						name = self.points[i] + "to" + self.points[j]						
						if name not in self.edges:
							self.edges.append(name)
		else:
			print("Pontos não identificados")

	def getEdges(self):
		return self.edges

	def setCosts(self):		
		if len(self.edges) > 0:
			for i in range(1,len(self.matrix)):				
				for j in range(1,len(self.matrix[0])): 					
					if self.matrix[i][j] != "": # there is a cost between these edges
						self.costs.append(self.matrix[i][j])
						
			self.dictCosts = dict(zip(self.edges, self.costs))
		else:
			print("Caminhos não identificados")
	
	def getCosts(self):
		return self.costs

	def getDictCosts(self):
		return self.dictCosts

	def isSubList(self,edges):		
		if set(edges).issubset(set(self.edges)):
			return True
		#elif set(self.edges).issubset(set(edges)):
		#	return True
		else:
			return False

mat = Matrix('distances1')
a = mat.run()
matrix = mat.setMatrix()				
points = mat.setPoints()
edges = mat.setEdges()		
costs = mat.setCosts()		
