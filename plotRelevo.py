from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import xml.dom.minidom
import random
import copy
import matplotlib.pyplot as plt
import matplotlib.markers as plm
import numpy as np
import json
import itertools

class Graficos:

	def __init__(self, nodes,edges,nameFile,X,Y,Z):
		self.name = nameFile			
		self.nodes = nodes
		self.edges = edges			
		self.Z = Z
		self.eixoZ = Z.copy()
		self.X = X
		self.Y = Y
		self.nos = []
		self.eixoX =[]
		self.eixoY =[]

	def setEixos(self):
		x = []
		y = []
		z = []
		for j in range(len(self.eixoZ)):
			if self.eixoZ[j][0] != ":":
				z.append(float(self.eixoZ[j][1]))
				x.append(float(self.X[j][1]))
				y.append(float(self.Y[j][1]))
		
		self.eixoZ = z
		self.eixoX = x
		self.eixoY = y

	def g3D(self):
			
		fig = plt.figure(2)
		ax = Axes3D(fig)

		surf = ax.plot_trisurf(self.eixoX, self.eixoY, self.eixoZ, cmap=cm.jet, linewidth=0.2, antialiased=True)
		fig.colorbar(surf, shrink=0.5, aspect=5)
		ax.set_xlabel('x (m)')
		ax.set_ylabel('y (m)')
		ax.set_zlabel('z (m)')		 						 				
		plt.savefig('surface.png')
		plt.show()
						

	def run(self):		
		self.setEixos()
		self.g3D()