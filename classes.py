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
    'X1': (269, 131),     # Bellarmine Field 
    'X2': (341, 527),     # Baseball Field 
    'X3': (667, 380),     # Ocampo Field
    'BEL': (140, 41),    # Bellarmine Hall 
    'ISO': (112, 165),    # ISO Complex 
    'SDC': (180, 256),    # SDC Complex 
    'XV': (327, 188),     # Xavier Hall 
    'FB': (298, 258),     # Faber Hall 
    'O': (289, 312),      # Old Rizal Library 
    'M': (359, 314),      # MVP Center 
    'K': (348, 234),      # Kostka Hall 
    'B': (382, 183),      # Berchmans Hall 
    'G': (443, 236),      # Gonzaga Hall 
    'C': (415, 300),      # Schmitt Hall 
    'P': (444, 384),      # PIPAC 
    'F': (380, 391),      # Faura 
    'D': (326, 391),      # Dela Costa Hall 
    'SS': (246, 381),     # SOSS Building 
    'LH': (259, 443),     # Leong Hall 
    'N': (319, 451),      # New Rizal Library
    'SEC-A': (547, 273),  # SEC A
    'SEC-BC': (530, 349), # SEC B and SEC C
    'MR': (597, 355),     # Matteo Ricci
    'JSEC': (572, 412),   # JSEC
    'CTC-SOM': (523, 456) # CTC SOM
}

NODE_KEY_MAPPING = [
    ('X1', 'Bellarmine Field (EAA)'),
    ('X2', 'Baseball Field (EAA)'),
    ('X3', 'Ocampo Field (EAA)'),
    ('BEL', 'Bellarmine Hall'),
    ('ISO', 'ISO Complex'),
    ('SDC', 'SDC Complex'),
    ('XV', 'Xavier Hall'),
    ('FB', 'Faber Hall'),
    ('O', 'Old Rizal Library'),
    ('M', 'MVP Center'),
    ('K', 'Kostka Hall'),
    ('B', 'Berchmans Hall'),
    ('G', 'Gonzaga Hall'),
    ('C', 'Schmitt Hall'),
    ('P', 'PIPAC'),
    ('F', 'Faura'),
    ('D', 'Dela Costa Hall'),
    ('SS', 'SOSS Building'),
    ('LH', 'Leong Hall'),
    ('N', 'New Rizal Library'),
    ('SEC-A', 'SEC A'),
    ('SEC-BC', 'SEC B and SEC C'),
    ('MR', 'Matteo Ricci'),
    ('JSEC', 'JSEC'),
    ('CTC-SOM', 'CTC SOM')
]

NODE_RADIUS = 7
START_NODE_COLOR = 'green'
EAA_NODE_COLOR = 'yellow'
DEFAULT_NODE_COLOR = 'red'
PATH_COLOR = 'orange'
PATH_WIDTH = 3
LABEL_COLOR = '#6cff04'
LABEL_FONT = ('Arial', 10, 'bold')

# store the currently selected start node
selected_start_node = None

CAMPUS_GRAPH = Graph(EDGE_LIST)
ALL_NODES = sorted(list(CAMPUS_GRAPH.vertices.keys()))
EAA_NODES = ['X1', 'X2', 'X3']

