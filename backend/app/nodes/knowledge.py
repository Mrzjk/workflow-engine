from .base import BaseNode
from app.knowledge import MockRetriever
from app.template import TemplateRenderer
class KnowledgeNode(BaseNode):
    node_type="knowledge"
    async def execute(self,state): return {"output":await MockRetriever().retrieve(TemplateRenderer().render(self.config.get("query","{{ input }}"),state),self.config.get("top_k",3))}
