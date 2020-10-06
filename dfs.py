# https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/

#Depth-First Search
class DFS:

    def dfs_paths(self,graph, start, goal):
        stack = [(start, [start])]
        while stack:
            #print(stack)          
            (vertex, path) = stack.pop()
            for next in graph[vertex] - set(path):
                if next == goal:                    
                    return path + [next]

                else:
                    stack.append((next, path + [next]))
    
    def run(self,inicio,destino,edgesV): 
        graph = {valor: set(edgesV[valor]) for valor in edgesV}
        path = list(self.dfs_paths(graph, inicio, destino))
        #print(path)
        return path