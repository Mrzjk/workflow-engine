from collections import defaultdict, deque
class GraphAnalyzer:
    def __init__(self, graph):
        self.nodes={n.id:n for n in graph.nodes}; self.edges=graph.edges; self.parents_map=defaultdict(list); self.children_map=defaultdict(list)
        for e in self.edges: self.parents_map[e.target].append(e.source); self.children_map[e.source].append(e.target)
    def get_parents(self,n): return self.parents_map[n]
    def get_children(self,n): return self.children_map[n]
    def get_roots(self): return [n for n in self.nodes if not self.parents_map[n]]
    def get_leaves(self): return [n for n in self.nodes if not self.children_map[n]]
    def is_reachable(self, source, target):
        seen={source}; q=deque([source])
        while q:
            x=q.popleft()
            if x==target:return True
            for y in self.children_map[x]:
                if y not in seen: seen.add(y); q.append(y)
        return False
    def detect_cycles(self):
        temp=set(); perm=set(); cycles=[]
        def visit(x,path):
            if x in temp: cycles.append(path[path.index(x):]); return
            if x in perm:return
            temp.add(x)
            for y in self.children_map[x]: visit(y,path+[y])
            temp.remove(x); perm.add(x)
        for n in self.nodes: visit(n,[n])
        return cycles
    def topological_sort(self):
        indeg={n:len(self.parents_map[n]) for n in self.nodes}; q=deque([n for n,d in indeg.items() if d==0]); out=[]
        while q:
            n=q.popleft(); out.append(n)
            for c in self.children_map[n]: indeg[c]-=1; q.extend([c] if indeg[c]==0 else [])
        return out
    def find_parallel_groups(self): return [v for v in self.children_map.values() if len(v)>1]
    def find_join_nodes(self): return [n for n in self.nodes if self.nodes[n].type=="join"]
