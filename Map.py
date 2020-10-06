import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom
import random
import copy
import numpy as np

class Map:
    """ Defining edges and nodes based on the Map (net.xml file) """

    def __init__(self, nameNetFile):
        self.name = nameNetFile 
        self.matrix = []
        self.nodes = []
        self.edges = []
        self.costs = []
        self.edgesV = {}
        self.csvFile = "costs"
        self.Z = []
        self.X = []
        self.Y = []
        self.cNodes = []    

    def setEdges(self):
    	# salva em uma lista o id de todas as arestas existentes no cenário
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        edges = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            if i.nodeName == "edge":
                if i.getAttribute('id')[0] != ':': # edges automaticas que aparecem no .net
                    edges.append(i.getAttribute('id'))
        self.edges = edges

    def connectedNodes(self):
    	# verifica com que nó cada nó está conectado
        nodes1 = []
        for i in self.nodes:
            nodes1.append([i])
        #print(nodes1)
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        edges = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            if i.nodeName == "edge":
                if i.getAttribute('id')[0] != ':': # edges automaticas que aparecem no .net                    
                    to1 = i.getAttribute('to')                    
                    from1 = i.getAttribute('from')
                    indexTo = self.nodes.index(to1)
                    nodes1[indexTo].append(from1)

        self.cNodes = nodes1

    def getEdges(self):
        return self.edges

    def getListEdges(self,nodes):
    	# retorna uma lista de arestas de acordo com a lista de nós que é passada na entrada
        listEdges = []
        #print(nodes)        
        for i in range(len(nodes)-1):
            listEdges.append(str(nodes[i])+str(nodes[i+1]))                      
        return listEdges

    def setNodes(self):
    	# salvo o id de todos os nós do cenário em uma lista (atributo do objeto: self.nodes)
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        nodes = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            if i.nodeName == "junction":
                if i.getAttribute('id')[0]!= ':': # edges automaticas que aparecem no .net      
                    nodes.append(i.getAttribute('id'))
        self.nodes = sorted(nodes,key= int)#.sort()
        self.nodes = nodes
    
    def getNodes(self):
        return self.nodes

    def setZ(self):
    	# matriz com o id do nó e a posição desse nó no eixo z
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        cZ = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            cZ = []
            if i.nodeName == "junction":                
                cZ.append(i.getAttribute('id'))
                cZ.append(i.getAttribute('z'))
            if len(cZ) > 0 and cZ not in self.Z:                
                self.Z.append(cZ)
    
    def getZ(self):
        return self.Z

    def setX(self):     
    	# matriz com o id do nó e a posição desse nó no eixo x
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        cX = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            cX = []
            if i.nodeName == "junction":                
                cX.append(i.getAttribute('id'))
                cX.append(i.getAttribute('x'))
            if len(cX) > 0 and cX not in self.X:                
                self.X.append(cX)

    def getX(self):
        return self.X

    def setY(self):
    	# matriz com o id do nó e a posição desse nó no eixo y
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        cY = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            cY = []
            if i.nodeName == "junction":                    
                cY.append(i.getAttribute('id'))
                cY.append(i.getAttribute('y'))
            if len(cY) > 0 and cY not in self.Y:                
                self.Y.append(cY)

    def getY(self):
        return self.Y

    def validateEdge(self,i,f):
    	# verifica se existe aresta que permite um caminho direto entre os nós i e f da entrada da função
        name = str(i) + str(f)
        if name in self.edges:
            return True
        else:
            validate = False
            x = xml.dom.minidom.parse(self.name + '.net.xml')
            net = x.documentElement                     
            child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
            for i in child:
                if i.nodeName == "edge":
                    if i.getAttribute('id')[0]!= ':': # edges automaticas que aparecem no .net                      
                        from1 = i.getAttribute('from')
                        to1 = i.getAttribute('to')
                        if str(from1) == str(i) and str(to1) == str(f):
                            validate = True
            return validate

    def displacement(self,i,f):
    	# não está sendo usado
        
        if self.validateEdge(i,f) == True:
            
            xi = 0
            yi = 0
            zi = 0
            xf = 0
            yf = 0
            zf = 0

            for j in range(len(self.nodes)):
                if self.X[j][0] == str(i):
                    xi = self.X[j][1]
                    yi = self.Y[j][1]
                    zi = self.Z[j][1]
                elif self.X[j][0] == str(f):
                    xf = self.X[j][1]
                    yf = self.Y[j][1]
                    zf = self.Z[j][1]

            deltaX = float(xf) - float(xi)
            deltaY = float(yf) - float(yi)
            deltaZ = float(zf) - float(zi)
            deltaR = ((deltaX ** 2) + (deltaY ** 2) + (deltaZ ** 2)) ** 0.5         
            
            return deltaR       

        else:
            return ""

    def displacementDirect(self,i,f):
        # calcula a distância entre dois pontos que não estão conectados

        xi = 0
        yi = 0
        zi = 0
        xf = 0
        yf = 0
        zf = 0

        aX = np.array(self.X)
        aY = np.array(self.Y)
        aZ = np.array(self.Z)

        rX = np.where(aX == i)
        listCoordinatesRX = list(zip(rX[0], rX[1]))
        rY = np.where(aY == i)
        listCoordinatesRY = list(zip(rY[0], rY[1]))
        rZ = np.where(aZ == i)
        listCoordinatesRZ = list(zip(rZ[0], rZ[1]))

        pX = np.where(aX == f)
        listCoordinatesPX = list(zip(pX[0], pX[1]))
        pY = np.where(aY == f)
        listCoordinatesPY = list(zip(pY[0], pY[1]))
        pZ = np.where(aZ == f)
        listCoordinatesPY = list(zip(pY[0], pY[1]))
        
        xi = self.X[int(listCoordinatesRX[0][0])][1]
        yi = self.Y[int(listCoordinatesRY[0][0])][1]
        zi = self.Z[int(listCoordinatesRZ[0][0])][1]

        xf = self.X[int(listCoordinatesPX[0][0])][1]
        yf = self.Y[int(listCoordinatesPX[0][0])][1]
        zf = self.Z[int(listCoordinatesPX[0][0])][1]

        deltaX = float(xf) - float(xi)
        deltaY = float(yf) - float(yi)
        deltaZ = float(zf) - float(zi)
        deltaR = ((deltaX ** 2) + (deltaY ** 2) + (deltaZ ** 2)) ** 0.5         
        
        return deltaR 

    def displacement1(self,i,f):
    	# calcula a distância entre dois pontos que estão conectados
        
        if self.validateEdge(i,f) == True:

            xi = 0
            yi = 0
            zi = 0
            xf = 0
            yf = 0
            zf = 0

            aX = np.array(self.X)
            aY = np.array(self.Y)
            aZ = np.array(self.Z)

            rX = np.where(aX == i)
            listCoordinatesRX = list(zip(rX[0], rX[1])) # rX[0]: self.X[] | rX[1]: self.X[][]
            rY = np.where(aY == i)
            listCoordinatesRY = list(zip(rY[0], rY[1]))
            rZ = np.where(aZ == i)
            listCoordinatesRZ = list(zip(rZ[0], rZ[1]))

            pX = np.where(aX == f)
            listCoordinatesPX = list(zip(pX[0], pX[1]))
            pY = np.where(aY == f)
            listCoordinatesPY = list(zip(pY[0], pY[1]))
            pZ = np.where(aZ == f)
            listCoordinatesPY = list(zip(pY[0], pY[1]))
            
            xi = self.X[int(listCoordinatesRX[0][0])][1]
            yi = self.Y[int(listCoordinatesRY[0][0])][1]
            zi = self.Z[int(listCoordinatesRZ[0][0])][1]

            xf = self.X[int(listCoordinatesPX[0][0])][1]
            yf = self.Y[int(listCoordinatesPX[0][0])][1]
            zf = self.Z[int(listCoordinatesPX[0][0])][1]

            deltaX = float(xf) - float(xi)
            deltaY = float(yf) - float(yi)
            deltaZ = float(zf) - float(zi)
            deltaR = ((deltaX ** 2) + (deltaY ** 2) + (deltaZ ** 2)) ** 0.5         
            
            return deltaR
        else:
            return ""

    def setCosts(self):
        # salva uma lista com o custo de cada nó para cada nó        
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        cost = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            cost = []
            if i.nodeName == "edge":                    
                id1 = i.getAttribute('id')
                if id1 in self.edges:
                    from1 = i.getAttribute('from')
                    to1 = i.getAttribute('to')
                    cost.append(id1)
                    cost.append(self.displacement1(from1,to1))               
            if len(cost) > 0 and cost not in self.costs:
                self.costs.append(cost)                 

    def getCosts(self):
        return self.costs

    def setMatrix(self):  
    	# cria a matriz csv com todas as distâncias dos nós que estão conectados                  
        if len(self.nodes) > 0 and len(self.edges) > 0:
            nodes = self.nodes.copy()
            nodes.insert(0,"")
            self.matrix.append(sorted(nodes))       
            m = []
            for i in sorted(self.nodes):
                m = []
                m.append(i)
                for j in sorted(self.nodes):
                    m.append(self.displacement1(str(i),str(j)))
                    #print(i,j,self.displacement1(str(i),str(j)))
                self.matrix.append(m)
            with open(self.csvFile + '.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                for i in self.matrix:
                    writer.writerow(i)
            print(self.csvFile, ".csv created", sep="")
        else:
            print("Parâmetros não definidos")   
    """
    def setMatrix1(self):    
        if len(self.nodes) > 0 and len(self.edges) > 0:
            nodes = self.nodes.copy()
            nodes.insert(0,"")
            self.matrix.append(nodes)
            m = []
            for i in self.cNodes:
                m = [''] * (len(self.nodes) + 1)
                m.insert(0,str(i[0]))
                for j in range(1,len(i)):                    
                    index = self.nodes.index(str(i[j]))
                    m.insert(index+1,self.displacement1(str(i[0]),str(i[j])))
                    print(i[0],str(i[j]),self.displacement1(str(i[0]),str(i[j])))
                self.matrix.append(m)
            with open(self.csvFile + '.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                for i in self.matrix:
                    writer.writerow(i)
            print(self.csvFile, ".csv created", sep="")
        else:
            print("Parâmetros não definidos")
	"""
    def getMatrix(self):
        return self.matrix

    def setcsvFile(self,name):
        self.csvFile = name

    def getcsvFile(self):
        return self.csvFile

    def setEdgesV(self):
    	# cria um set com os nós conectados
        for i in self.nodes:
            self.edgesV.update([(i,{})])
            for j in self.nodes:
                if self.validateRoute(i,j) == True:
                    item = self.edgesV.get(i)
                    item = list(item)
                    item.append(j)
                    self.edgesV.update([(i,item)])

    def getEdgesV(self):
        return self.edgesV

    def validateRoute(self,a,b):
    	# verifica se a rota é viável
    	
        cost = 0
        
        if len(self.matrix) < 1:
            with open(self.csvFile + '.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                matrix = []
                for row in spamreader:      
                    matrix.append(row)
                self.matrix = matrix
               
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
        a = self.setNodes()
        b = self.setEdges()
        c = self.setX()
        d = self.setY()
        e = self.setZ()
        f = self.connectedNodes()
        g = self.setEdgesV()
        #h = self.setMatrix1()        