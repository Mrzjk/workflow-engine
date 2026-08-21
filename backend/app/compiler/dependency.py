from .graph_analyzer import GraphAnalyzer
def dependency_map(graph): return {n.id: GraphAnalyzer(graph).get_parents(n.id) for n in graph.nodes}
