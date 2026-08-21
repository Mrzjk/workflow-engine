from .builtin.demo_tool import demo_tool
TOOL_REGISTRY={"demo_tool":demo_tool}
class ToolRegistry:
    @classmethod
    def get(cls,name):
        if name not in TOOL_REGISTRY: raise KeyError(f"unknown tool: {name}")
        return TOOL_REGISTRY[name]
    @classmethod
    def all(cls): return TOOL_REGISTRY
