import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

class Matrix:
	""" Defining edges and nodes based matrix """

	def __init__(self, nameMatrix):
		self.name = nameMatrix
		self.matrix = []
		self.points = []
		self.edges = []

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
					if self.matrix[i][j] != "":					
						name = self.points[i] + "to" + self.points[j]
						name1 = self.points[j] + "to" + self.points[i]
						if name not in self.edges:
							self.edges.append(name)
		else:
			print("Pontos não identificados")

	def getEdges(self):
		return self.edges

	def createNodes(self):
		nodes = Element('nodes')
		child = SubElement(nodes, 'node',{x=xis,y=ipslon})

	def run(self):
		matrix = mat.setMatrix()				
		points = mat.setPoints()
		edges = mat.setEdges()
		print(mat.getEdges())
	

mat = Matrix('distances1')
a = mat.run()

