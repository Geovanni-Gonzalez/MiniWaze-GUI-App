import heapq

class Pathfinder:
    @staticmethod
    def find_path(graph, start_id, end_id):
        """
        Dijkstra's Algorithm.
        Returns (path_list_of_nodes, total_cost)
        """
        start_node = graph.nodes.get(start_id)
        end_node = graph.nodes.get(end_id)

        if not start_node or not end_node:
            return None, 0

        # Reset graph state
        for node in graph.nodes.values():
            node.g_cost = float('inf')
            node.parent = None

        start_node.g_cost = 0
        priority_queue = [(0, start_node.id)] # (cost, node_id)
        
        visited = set()

        while priority_queue:
            current_cost, current_id = heapq.heappop(priority_queue)
            current_node = graph.nodes[current_id]

            if current_id in visited:
                continue
            visited.add(current_id)

            if current_id == end_id:
                return Pathfinder._reconstruct_path(current_node), current_cost

            for neighbor, weight in current_node.edges:
                if neighbor.id in visited:
                    continue

                new_cost = current_cost + weight
                if new_cost < neighbor.g_cost:
                    neighbor.g_cost = new_cost
                    neighbor.parent = current_node
                    heapq.heappush(priority_queue, (new_cost, neighbor.id))

        return None, float('inf') # No path found

    @staticmethod
    def _reconstruct_path(end_node):
        path = []
        current = end_node
        while current:
            path.append(current)
            current = current.parent
        return path[::-1] # Reverse
