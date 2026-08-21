from .base import BaseNode
from app.tools import ToolRegistry
from app.template import TemplateRenderer
class ToolNode(BaseNode):
    node_type="tool"
    async def execute(self,state):
        args={k:TemplateRenderer().render(str(v),state) for k,v in self.config.get("arguments",{}).items()}
        return {"output":await ToolRegistry.get(self.config["tool_name"]).ainvoke(args),"input":args}
