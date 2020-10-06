def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))
"""
graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}
"""
graph = {'A': set(['B', 'D', 'E']),
         'B': set(['A', 'C', 'G']),
         'C': set(['B', 'D']),
         'D': set(['A', 'C', 'E']),
         'E': set(['A', 'D', 'F']),
         'F': set(['E', 'G', 'H']),
         'G': set(['B','F']),
         'H': set(['D', 'F'])         
         }
print(list(dfs_paths(graph, 'A', 'F'))) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
