from abc import ABC, abstractmethod

class A(ABC):
    def __init__(self, graph):
        self.graph = graph 

    @abstractmethod
    def solve(self, start, stop):
        pass

class AKT(A):
    def solve(self, start, stop):
        import heapq
        heap = [(0, start, [start])]  
        visited = set()
        while heap:
            cost, node, path = heapq.heappop(heap)
            if node == stop:
                return path, cost
            if node in visited:
                continue
            visited.add(node)
            for neighbor, weight in self.graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))
        return None, float('inf')

class AStar(A):
    def __init__(self, graph, heuristic):
        super().__init__(graph)
        self.heuristic = heuristic  

    def solve(self, start, stop):
        open_lst = set([start])
        closed_lst = set([])
        g_score = {start: 0}
        parent = {start: start}

        while open_lst:
            n = None
            for v in open_lst:
                if n is None or g_score[v] + self.heuristic.get(v,0) < g_score[n] + self.heuristic.get(n,0):
                    n = v

            if n is None:
                return None, float('inf')

            if n == stop:
                path = []
                while parent[n] != n:
                    path.append(n)
                    n = parent[n]
                path.append(start)
                path.reverse()
                return path, g_score[path[-1]]

            for (m, weight) in self.graph.get(n, []):
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    parent[m] = n
                    g_score[m] = g_score[n] + weight
                else:
                    if g_score.get(m,float('inf')) > g_score[n] + weight:
                        g_score[m] = g_score[n] + weight
                        parent[m] = n
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            open_lst.remove(n)
            closed_lst.add(n)

        return None, float('inf')

def main():
    n = 4
    if n == 3:
        graph = {
            'A': [('B',1), ('C',4)],
            'B': [('C',2)],
            'C': []
        }
        heuristic = {'A':1,'B':1,'C':1}
    else:  
        graph = {
            'A': [('B',1), ('C',4)],
            'B': [('C',2), ('D',5)],
            'C': [('D',1)],
            'D': []
        }
        heuristic = {'A':1,'B':2,'C':1,'D':0}

    print("=== AKT Algorithm ===")
    akt_solver = AKT(graph)
    path, cost = akt_solver.solve('A','D')
    print("Path:", path, "Cost:", cost)

    print("\n=== A* Algorithm ===")
    astar_solver = AStar(graph, heuristic)
    path, cost = astar_solver.solve('A','D')
    print("Path:", path, "Cost:", cost)

if __name__ == "__main__":
    main()

