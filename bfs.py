# baseado em: https://github.com/joeyajames/Python/blob/master/bfs.py
# https://www.youtube.com/watch?v=-uR7BSfNJko
# https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python

# Breath-First Search
class Vertex:
	def __init__(self, n):
		self.name = n
		self.neighbors = list()
		
		self.distance = 9999
		self.color = 'black'

		self.path = ''
	
	def add_neighbor(self, v):
		if v not in self.neighbors:
			self.neighbors.append(v)
			self.neighbors.sort()

class Graph:
	vertices = {}
	
	def add_vertex(self, vertex):
		if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
			self.vertices[vertex.name] = vertex
			return True
		else:
			return False
	
	def add_edge(self, u, v):
		if u in self.vertices and v in self.vertices:
			for key, value in self.vertices.items():
				if key == u:
					value.add_neighbor(v)
				if key == v:
					value.add_neighbor(u)
			return True
		else:
			return False
			
	def graphPath(self,dest):
		#for key in sorted(list(self.vertices.keys())):
		#	print(key + str(self.vertices[key].neighbors) + "  " + str(self.vertices[key].distance))
		
		lista = []
		lista.append(dest)
		prox = str(self.vertices[dest].path)
		#print("a",self.vertices['10'].path)			
		#print("prim prox",prox)
		for i in range(self.vertices[dest].distance):
			lista.append(str(prox))
			prox = str(self.vertices[str(prox)].path)
			#print("prox",prox)
		return lista

	"""
	def bfs(self, vert):
		q = list()
		vert.distance = 0
		vert.color = 'red'
		for v in vert.neighbors:
			self.vertices[v].distance = vert.distance + 1
			q.append(v)
		
		while len(q) > 0:
			u = q.pop(0)		
			node_u = self.vertices[u]
			node_u.color = 'red'
			
			for v in node_u.neighbors:
				node_v = self.vertices[v]
				if node_v.color == 'black':
					q.append(v)
					if node_v.distance > node_u.distance + 1:
						node_v.distance = node_u.distance + 1
	"""
	def bfs(self, vert, inicio):		
		q = list()
		vert.distance = 0
		vert.color = 'red'
		path = []

		for v in vert.neighbors:			
			self.vertices[v].distance = vert.distance + 1
			self.vertices[v].path = vert.name
			q.append(v)
		
		u = '000'
		while len(q) > 0: #and u != inicio:
			u = q.pop(0)
			node_u = self.vertices[u]
			node_u.color = 'red'
			
			for v in node_u.neighbors:				
				node_v = self.vertices[v]
				if node_v.color == 'black':
					q.append(v)					
					if node_v.distance > node_u.distance + 1:
						node_v.distance = node_u.distance + 1
						node_v.path = node_u.name
						#print(node_v.path,"Aquiii",node_u.name)
						
	def run(self,inicio,destino,vertices,arestas):	
		g = Graph()		
		b = Vertex(str(destino))
		g.add_vertex(b)		

		for i in range(len(vertices)):			
			g.add_vertex(Vertex(str(vertices[i])))

		for arestas in arestas:
			g.add_edge(arestas[:3], arestas[3:])			
			
		g.bfs(b,str(inicio))
		lista = g.graphPath(str(inicio))
		return lista


