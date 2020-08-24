import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.dom.minidom
import random
import copy

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

    def setEdges(self):
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        edges = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            if i.nodeName == "edge":
                if i.getAttribute('id')[0]!= ':': # edges automaticas que aparecem no .net
                    edges.append(i.getAttribute('id'))
        self.edges = edges

    def getEdges(self):
        return self.edges

    def getListEdges(self,nodes):
        #print(self.edges)
        listEdges = []
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE] 
        for m in range(len(nodes)-1):
            #print("buscando",str(nodes[m]),"to",str(nodes[m+1]))               
            for i in child:
                if i.nodeName == "edge":
                    if i.getAttribute('id')[0]!= ':': # edges automaticas que aparecem no .net                      
                        from1 = i.getAttribute('from')
                        to1 = i.getAttribute('to')
                        #print("from",str(from1),"to",str(to1))         
                        if str(from1) == str(nodes[m]) and str(to1) == str(nodes[m+1]):
                            #print("entrou")
                            listEdges.append(i.getAttribute('id'))
                            break                       
        return listEdges

    def setNodes(self):
        x = xml.dom.minidom.parse(self.name + '.net.xml')
        net = x.documentElement         
        nodes = []
        child = [i for i in net.childNodes if i.nodeType == x.ELEMENT_NODE]
        for i in child:
            if i.nodeName == "junction":
                if i.getAttribute('id')[0]!= ':': # edges automaticas que aparecem no .net      
                    nodes.append(i.getAttribute('id'))
        self.nodes = nodes

    def getNodes(self):
        return self.nodes

    def setZ(self):     
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

    def setCosts(self):
        
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
                    cost.append(self.displacement(from1,to1))               
            if len(cost) > 0 and cost not in self.costs:
                self.costs.append(cost)                 

    def getCosts(self):
        return self.costs

    def setMatrix(self):                    
        if len(self.nodes) > 0 and len(self.edges) > 0:
            nodes = self.nodes.copy()
            nodes.insert(0,"")
            self.matrix.append(nodes)       
            m = []
            for i in self.nodes:
                m = []
                m.append(i)
                for j in self.nodes:                
                    m.append(self.displacement(str(i),str(j)))
                self.matrix.append(m)
            with open(self.csvFile + '.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                for i in self.matrix:
                    writer.writerow(i)
            print(self.csvFile, ".csv created", sep="")
        else:
            print("Parâmetros não definidos")   

    def getMatrix(self):
        return self.matrix

    def setcsvFile(self,name):
        self.csvFile = name

    def getcsvFile(self):
        return self.csvFile

    def setEdgesV(self):
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
        f = self.setEdgesV()
        #g = self.setMatrix()       