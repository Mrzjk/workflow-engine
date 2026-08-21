from langchain_core.messages import SystemMessage, HumanMessage
from .base import BaseNode
from app.llm import LLMFactory
from app.template import TemplateRenderer
class LLMNode(BaseNode):
    node_type="llm"
    async def execute(self,state):
        r=TemplateRenderer(); prompt=r.render(self.config.get("prompt","{{ input }}"),state); model=LLMFactory.create(self.config)
        response=await model.ainvoke([SystemMessage(content=self.config.get("system_prompt","")),HumanMessage(content=prompt)])
        return {"output":response.content,"prompt":prompt,"model":self.config.get("model")}
