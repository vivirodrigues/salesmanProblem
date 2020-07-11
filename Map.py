import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom
import random

class Map:
	""" Defining edges and nodes based on the Map """

	def __init__(self, nameNetFile):
		self.name = nameNetFile	
		self.matrix = []
		self.nodes = []
		self.edges = []
		self.costs = []
		self.dictCosts = {}	

	def setEdges(self):
		x = xml.dom.minidom.parse(self.name + '.net.xml')
		net = x.documentElement			
		edges = []
		child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
		for i in child:
			if i.nodeName == "edge":
				edges.append(i.getAttribute('id'))
		self.edges = edges

	def getEdges(self):
		return self.edges

	def setNodes(self):
		x = xml.dom.minidom.parse(self.name + '.net.xml')
		net = x.documentElement			
		nodes = []
		child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
		for i in child:
			if i.nodeName == "junction":
				nodes.append(i.getAttribute('id'))
		self.nodes = nodes

	def getNodes(self):
		return self.nodes

	def setCosts(self):
		for i in self.edges:
			self.costs.append(random.uniform(0, 10))
		self.dictCosts = dict(zip(self.edges, self.costs))

	def getCosts(self):
		return self.costs

	def setMatrix(self):
		with open(self.name + '.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(self.nodes)
			lista = []
			linha = []	
			for i in range(len(self.nodes)):								
				lista.append(self.nodes[i])
				for j in range(len(self.nodes)):
					lista.append(self.costs[j])
		print(lista)

mat = Map('hello')
nodes = mat.setNodes()
#print(mat.getNodes())
edges = mat.setEdges()
#print(mat.getEdges())
costs = mat.setCosts()
print(mat.getCosts())
matrix = mat.setMatrix()
