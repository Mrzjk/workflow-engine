"""Small SDK surface used by exported Workflow Studio Python source."""
class Workflow:
    def __init__(self,name): self.name=name; self.nodes=[]; self.edges=[]
    def _node(self,type,**config): self.nodes.append({"type":type,**config}); return config.get("id")
    def llm(self,**config): return self._node("llm",**config)
    def tool(self,**config): return self._node("tool",**config)
    def condition(self,**config): return self._node("condition",**config)
    def join(self,**config): return self._node("join",**config)
    def knowledge(self,**config): return self._node("knowledge",**config)
    def code(self,**config): return self._node("code",**config)
    def connect(self,source,target): self.edges.append((source,target))
    def compile(self): return self
