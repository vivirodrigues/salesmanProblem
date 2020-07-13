import Map
import GA

net = Map.Map('hello') # net file
genMatrix = net.run() # csv of costs created
csvName = net.getcsvFile() # name of csv file
geneticA = GA.GA(csvName)
test = geneticA.run()
