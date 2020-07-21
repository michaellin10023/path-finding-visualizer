from collections import defaultdict 

class graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
    
    def bfs(self, start):
        visited = [False] * (len(self.graph))
        q = []
        q.append(start)
        visited[start] = True
        while q:
            temp = q.pop(0)
            print(temp)
            for neighbor in self.graph[temp]:
                if visited[neighbor] == False:
                    q.append(neighbor)
                    visited[neighbor] = True

g = graph()
g.add_edge(0,1)
g.add_edge(0,2)
g.add_edge(1,2)
g.add_edge(2,0)
g.add_edge(2,3)
g.add_edge(3,3)
g.bfs(2)




            


        