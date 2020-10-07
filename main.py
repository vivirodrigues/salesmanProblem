import Map
import random
import GA
import bfs
import dfs
import astar
import plotRelevo
import mainSumo

# configuration
file = 'SUMO/map'
net = Map.Map(file) # net file
genMatrix = net.run() # csv created (costs)
csvName = net.getcsvFile()
nodes = net.getNodes()
edges = net.getEdges()
X = net.getX()
Y = net.getY()
Z = net.getZ()
edgesV = net.getEdgesV()

# GA
nIndividuals = 7
limitGen = 20

points = [('031','172'),('001','187'),('112','092'),('119','024'),('147','099')]

code = 1

for i in points:

	inicio = i[0]
	print("Iniciando de:", inicio)
	objetivo = i[1]
	print("Objetivo é", objetivo)

	h_bfs = bfs.Graph()
	bfss = h_bfs.run(inicio,objetivo,nodes,edges)
	print("BFS",bfss)

	h_astar = astar.main(edgesV,nodes,inicio,objetivo, net)
	print("A-star",h_astar)

	# Rotas para o sumo
	edgesBFS = net.getListEdges(bfss)
	print("Route BFS:",edgesBFS)
	edgesASTAR = net.getListEdges(h_astar)
	print("Route A*:",edgesASTAR)

	print("Executando a BFS")
	consumption1 = mainSumo.main(edgesBFS,'BFS', code)
	print("Executando a A-star")
	consumption3 = mainSumo.main(edgesASTAR,'Astar', code)

	geneticA = GA.GA(csvName, nodes, edges, inicio, objetivo, nIndividuals, limitGen, net, code)#,inicio,objetivo)
	test = geneticA.run()

	code += 1
