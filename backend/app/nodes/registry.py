from .start import StartNode
from .end import EndNode
from .llm import LLMNode
from .tool import ToolNode
from .condition import ConditionNode
from .code import CodeNode
from .knowledge import KnowledgeNode
from .join import JoinNode
NODE_REGISTRY={"start":StartNode,"llm":LLMNode,"tool":ToolNode,"condition":ConditionNode,"code":CodeNode,"knowledge":KnowledgeNode,"join":JoinNode,"end":EndNode}
def register_node(name,cls): NODE_REGISTRY[name]=cls
