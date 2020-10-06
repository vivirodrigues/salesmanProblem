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

"""
031 172
001 187
112 092
119 024
147 099
"""

inicio = '001'
print("Iniciando de:", inicio)
objetivo = '187'
print("Objetivo é", objetivo)


h_bfs = bfs.Graph()
bfss = h_bfs.run(inicio,objetivo,nodes,edges)
print("BFS",bfss)

h_astar = astar.main(edgesV,nodes,inicio,objetivo,file)
print("A-star",h_astar)

# Rotas para o sumo
edgesBFS = net.getListEdges(bfss)
print("Route BFS:",edgesBFS)
edgesASTAR = net.getListEdges(h_astar)
print("Route A*:",edgesASTAR)

print("Executando a BFS")
consumption1 = mainSumo.main(edgesBFS,'BFS')
#print("Executando a DFS")
#consumption2 = mainSumo.main(edgesDFS,'2S')
print("Executando a A-star")
consumption3 = mainSumo.main(edgesASTAR,'Astar')

#print("model",consumption1,consumption2,consumption3)
print("model",consumption1,consumption3)


geneticA = GA.GA(csvName,nodes,edges,inicio, objetivo,X,Y,Z)#,inicio,objetivo)
test = geneticA.run()

# printar o grafico de relevo:
# obs: arquivo plotRelevo.py precisa estar na raiz da pasta (e não na pasta results)
#grafico = plotRelevo.Graficos(nodes,edges,'SUMO/saida',X,Y,Z)
#run = grafico.run()