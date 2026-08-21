import re
class TemplateResolver:
    pattern=re.compile(r"{{\s*([^}]+)\s*}}")
    @classmethod
    def resolve(cls, expression, state):
        current=state
        for key in expression.strip().split("."):
            if key=="output" and isinstance(current,dict) and "node_outputs" in state: continue
            current=current.get(key,"" ) if isinstance(current,dict) else getattr(current,key,"")
        return current
