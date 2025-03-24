import networkx as nx

class DeadlockDetector:
    def __init__(self):
        """Initialize a directed graph for resource allocation."""
        self.graph = nx.DiGraph()

    def add_process(self, process_id, resource_id):
        """Add an edge from a process to a resource (request)."""
        self.graph.add_edge(process_id, resource_id)
    
    def add_resource(self, resource_id, process_id):
        """Add an edge from a resource to a process (allocation)."""
        self.graph.add_edge(resource_id, process_id)
    
    def detect_deadlock(self):
        """Detect cycles in the resource allocation graph (deadlock detection)."""
        try:
            cycle = nx.find_cycle(self.graph, orientation='original')
            return True, cycle  # Deadlock detected
        except nx.NetworkXNoCycle:
            return False, []  # No deadlock
    
    def get_graph_structure(self):
        """Return the graph structure for visualization."""
        return {
            "nodes": [{"id": node} for node in self.graph.nodes()],
            "links": [{"source": edge[0], "target": edge[1]} for edge in self.graph.edges()]
        }

# Example usage (for testing)
if __name__ == "__main__":
    detector = DeadlockDetector()

    # Simulate a deadlock scenario
    detector.add_process("P1", "R1")
    detector.add_resource("R1", "P2")
    detector.add_process("P2", "R2")
    detector.add_resource("R2", "P1")  # Circular dependency

    deadlock, cycle = detector.detect_deadlock()
    
    if deadlock:
        print("Deadlock detected! Cycle:", cycle)
    else:
        print("No deadlock detected.")

    # Print graph structure
    print("Graph Structure:", detector.get_graph_structure())
