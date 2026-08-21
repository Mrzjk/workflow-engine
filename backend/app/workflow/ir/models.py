"""Canonical, UI-independent representation of a Workflow."""
from pydantic import BaseModel, Field
from typing import Literal

class MetadataIR(BaseModel): name: str = "Untitled Workflow"; description: str = ""; tags: list[str] = Field(default_factory=list)
class VariableIR(BaseModel): name: str; type: str = "string"; default: object | None = None
class ConditionIR(BaseModel): expression: str; branch: str | None = None
class NodeIR(BaseModel): id: str; type: Literal["start","llm","tool","condition","code","knowledge","join","end"]; name: str = ""; config: dict = Field(default_factory=dict); position: dict[str,float] | None = None
class EdgeIR(BaseModel): id: str; source: str; target: str; condition: ConditionIR | None = None
class WorkflowIR(BaseModel): version: str = "1.0"; metadata: MetadataIR = Field(default_factory=MetadataIR); variables: dict[str,VariableIR] = Field(default_factory=dict); nodes: list[NodeIR]; edges: list[EdgeIR]
