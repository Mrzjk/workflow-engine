from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
class NodePosition(BaseModel): x: float; y: float
class EdgeSchema(BaseModel): id: str; source: str; target: str; source_handle: str|None=None; target_handle: str|None=None
class BaseNode(BaseModel): model_config=ConfigDict(extra="forbid"); id: str; type: Literal["start","llm","tool","condition","code","knowledge","join","end"]; position: NodePosition; config: dict = Field(default_factory=dict)
class WorkflowSchema(BaseModel): version: str="1.0"; nodes: list[BaseNode]; edges: list[EdgeSchema]
class WorkflowCreate(BaseModel): agent_id: str; name: str; description: str|None=None; graph: WorkflowSchema
class LLMNodeConfig(BaseModel): provider: str="openai"; model: str; temperature: float=0.7; system_prompt: str=""; prompt: str
class ToolNodeConfig(BaseModel): tool_name: str; arguments: dict = Field(default_factory=dict)
class ConditionBranch(BaseModel): id: str; expression: str
class ConditionNodeConfig(BaseModel): branches: list[ConditionBranch]
class JoinNodeConfig(BaseModel): mode: Literal["all"]="all"
