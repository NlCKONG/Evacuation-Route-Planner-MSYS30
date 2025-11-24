from typing import Optional
import heapq

class Vertex:
    def __init__(self, key: str):
        self.key: str = key
        self.dist: float = float('inf')
        self.prev_vertex: Optional[Vertex] = None
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Vertex) and self.key == other.key
    
    def Reset(self) -> None:
        self.dist = float('inf')
        self.prev_vertex = None


class Edge:
    def __init__(self, u, v, weight):
        self.u: str = u
        self.v: str = v
        self.weight: float = weight
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Edge) and self.u == other.u and self.v == other.v and self.weight == other.weight

    def __lt__(self, other) -> bool:
        return self.weight < other.weight if isinstance(other, Edge) else False
    
    def __le__(self, other) -> bool:
        return self.weight <= other.weight if isinstance(other, Edge) else False
    
    def __gt__(self, other) -> bool:
        return self.weight > other.weight if isinstance(other, Edge) else False
    
    def __ge__(self, other) -> bool:
        return self.weight >= other.weight if isinstance(other, Edge) else False

class Graph:
    def __init__(self, edge_list: list[tuple[str, str, int]]):
        self.vertices: dict[str, Vertex] = {}
        self.adj: dict[str, list[tuple[str, float]]] = {}
        self.edges: list[Edge] = []

        for u, v, weight in edge_list:
            if u not in self.vertices:
                self.vertices[u] = Vertex(u)
                self.adj[u] = []
            if v not in self.vertices:
                self.vertices[v] = Vertex(v)
                self.adj[v] = []
            
            self.adj[u].append((v, weight))
            self.adj[v].append((u, weight))
            self.edges.append(Edge(u, v, weight))

def ResetGraph(graph: Graph) -> None:
    for vertex in graph.vertices.values():
        vertex.Reset()

def dijkstra(graph: Graph, start: str, end: str):

    if start not in graph.vertices or end not in graph.vertices:
        return [], float('inf')

    ResetGraph(graph)

    start_vertex = graph.vertices[start]
    start_vertex.dist = 0.0 

    queue: list[tuple[float, str]] = [(0.0, start)] 

    while queue:
        current_dist, current_key = heapq.heappop(queue)
        current_vertex = graph.vertices[current_key]

        if current_dist > current_vertex.dist:
            continue

        if current_key == end:
            route = reconstruct_path(graph.vertices[end])
            total_cost = graph.vertices[end].dist
            return route, total_cost

        for neighbor_key, weight in graph.adj[current_key]:
            neighbor_vertex = graph.vertices[neighbor_key]
            
            new_dist = current_dist + weight
            
            if new_dist < neighbor_vertex.dist:
                neighbor_vertex.dist = new_dist
                neighbor_vertex.prev_vertex = current_vertex
                heapq.heappush(queue, (new_dist, neighbor_key))

    return [], float('inf')

def reconstruct_path(end_vertex: Vertex) -> list[str]:
    path: list[str] = []
    current: Optional[Vertex] = end_vertex
    
    while current is not None:
        path.append(current.key)
        current = current.prev_vertex
        
    return path[::-1]

EDGE_LIST = [
    ('X1', 'XV', 4), ('X1', 'BEL', 5), ('ISO', 'BEL', 7), ('ISO', 'SDC', 4), ('X1', 'SDC', 6),
    ('B', 'XV', 1), ('K', 'XV', 1), ('FB', 'K', 2), ('FB', 'XV', 2), ('O', 'FB', 1),
    ('O', 'K', 4), ('O', 'M', 2), ('M', 'K', 3), ('G', 'K', 4), ('G', 'B', 3),
    ('C', 'M', 2), ('M', 'C', 2), ('SEC-A', 'G', 5), ('SEC-A', 'C', 6), ('P', 'C', 3),
    ('O', 'SDC', 7), ('SS', 'O', 4), ('SS', 'LH', 1), ('N', 'LH', 3), ('X2', 'N', 4),
    ('X2', 'LH', 6), ('X2', 'F', 7), ('D', 'F', 1), ('D', 'N', 3), ('P', 'F', 2),
    ('O', 'D', 4), ('M', 'D', 5), ('SEC-A', 'SEC-BC', 1), ('SEC-BC', 'MR', 1), ('JSEC', 'SEC-BC', 1),
    ('JSEC', 'CTC-SOM', 1), ('P', 'CTC-SOM', 3), ('X3', 'JSEC', 6), ('X3', 'MR', 5), ('X3', 'SEC-A', 10)
]

# Position of the nodes on the canvas (x, y)
# NOTE: We need to still fix the positions to match the actual campus map
# NOTE: And maybe add the campus map to the background of the canvas
NODE_POSITIONS = {
    'X1': (300, 100),     # Bellarmine Field
    'X2': (300, 550),     # Baseball Field
    'X3': (750, 500),     # Ocampo Field
    'BEL': (350, 150),    # Bellarmine Hall
    'ISO': (150, 250),    # ISO Complex
    'SDC': (250, 300),    # SDC Complex
    'XV': (400, 200),     # Xavier Hall
    'FB': (400, 250),     # Faber Hall
    'O': (400, 350),      # Old Rizal Library
    'M': (500, 300),      # MVP Center
    'K': (450, 250),      # Kostka Hall
    'B': (500, 250),      # Berchmans Hall
    'G': (550, 300),      # Gonzaga Hall
    'C': (550, 350),      # Schmitt Hall
    'P': (600, 350),      # PIPAC
    'F': (550, 500),      # Faura
    'D': (500, 500),      # Dela Costa Hall
    'SS': (350, 400),     # SOSS Building
    'LH': (300, 450),     # Leong Hall
    'N': (400, 500),      # New Rizal Library
    'SEC-A': (600, 400),  # SEC A
    'SEC-BC': (650, 400), # SEC B and SEC C
    'MR': (700, 450),     # Matteo Ricci
    'JSEC': (700, 500),   # JSEC
    'CTC-SOM': (650, 350) # CTC SOM
}
NODE_RADIUS = 7
START_NODE_COLOR = 'green'
EAA_NODE_COLOR = 'yellow'
DEFAULT_NODE_COLOR = 'red'
PATH_COLOR = 'orange'
PATH_WIDTH = 3

# Global variable to store the currently selected start node
selected_start_node = None

CAMPUS_GRAPH = Graph(EDGE_LIST)
ALL_NODES = sorted(list(CAMPUS_GRAPH.vertices.keys()))
EAA_NODES = ['X1', 'X2', 'X3']

