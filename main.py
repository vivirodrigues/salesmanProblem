import Map
import Cicle
import Heuristics
import random
import graficos

# configuration
net = Map.Map('SUMO/map') # net file
genMatrix = net.run() # csv created (costs)
csvName = net.getcsvFile()
nodes = net.getNodes()
edges = net.getEdges()
X = net.getX()
Y = net.getY()
Z = net.getZ()

# nó inicial e final
"""
seeds map:
inicio = 17 objetivo = 45
inicio = 2 objetivo = 29
inicio = 26 objetivo = 34
inicio = 28 objetivo = 6
inicio = 28 objetivo = 7
inicio = 10 objetivo = 15
inicio = 2 objetivo = 9
inicio = 38 objetivo = 9
inicio = 44 objetivo = 28
inicio = 9 objetivo = 12
inicio = 37 objetivo = 16
"""
inicio = int(random.choice(nodes))
print("Iniciando de:", inicio)
objetivo = int(random.choice(nodes))
print("Objetivo é", objetivo)

# heuristicas
heuristics = Heuristics.Heuristics(csvName,nodes,X,Y,Z)
run = heuristics.run()
route1 = heuristics.greedy(inicio,objetivo)
route2 = heuristics.aStar(inicio,objetivo)
route3 = heuristics.vizinho(inicio,objetivo)

# Rotas para o sumo
listEdges1 = net.getListEdges(route1)
print("Route Greedy:",listEdges1)
listEdges2 = net.getListEdges(route2)
print("Route A*:",listEdges2)
listEdges3 = net.getListEdges(route3)
print("Vizinho:",listEdges3)

# Ciclo
ciclo = Cicle.Cicle(csvName,nodes,edges,X,Y,Z)
route = ciclo.run()
listEdges = net.getListEdges(route)
print("Ciclo:",listEdges)

# grafico
grafico = graficos.Graficos(nodes,edges,'SUMO/Results/rota2_vizinho',X,Y,Z)
run = grafico.run()

