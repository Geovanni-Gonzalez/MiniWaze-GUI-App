class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value  # 0, L, N, S, R, C, SF, ND
        self.id = f"{x},{y}"
        self.edges = []
        self.h_cost = 0  # Heuristic for A* (optional, using Dijkstra first)
        self.g_cost = float('inf')
        self.parent = None

    def add_edge(self, target_node, weight):
        self.edges.append((target_node, weight))

    def __repr__(self):
        return f"Node({self.id}, {self.value})"

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, x, y, value):
        node = Node(x, y, value)
        self.nodes[node.id] = node
        return node

    def get_node(self, x, y):
        return self.nodes.get(f"{x},{y}")
    
    def get_all_nodes(self):
        return list(self.nodes.values())

    def reset_costs(self):
        for node in self.nodes.values():
            self.g_cost = float('inf')
            self.parent = None
