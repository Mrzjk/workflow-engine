import ast
from .base import BaseNode
class ConditionEvaluationError(ValueError): pass
class ExpressionEvaluator:
    allowed=(ast.Expression,ast.BoolOp,ast.UnaryOp,ast.Compare,ast.Name,ast.Load,ast.Constant,ast.And,ast.Or,ast.Not,ast.Gt,ast.GtE,ast.Lt,ast.LtE,ast.Eq,ast.NotEq)
    def evaluate(self,expression,variables):
        tree=ast.parse(expression,mode="eval")
        if not all(isinstance(n,self.allowed) for n in ast.walk(tree)): raise ConditionEvaluationError("unsafe condition expression")
        return self.visit(tree.body,variables)
    def visit(self,n,v):
        if isinstance(n,ast.Constant):return n.value
        if isinstance(n,ast.Name):return v.get(n.id)
        if isinstance(n,ast.BoolOp): return all(self.visit(x,v) for x in n.values) if isinstance(n.op,ast.And) else any(self.visit(x,v) for x in n.values)
        if isinstance(n,ast.UnaryOp):return not self.visit(n.operand,v)
        if isinstance(n,ast.Compare):
            a=self.visit(n.left,v); b=self.visit(n.comparators[0],v); return {ast.Gt:a>b,ast.GtE:a>=b,ast.Lt:a<b,ast.LtE:a<=b,ast.Eq:a==b,ast.NotEq:a!=b}[type(n.ops[0])]
class ConditionNode(BaseNode):
    node_type="condition"
    async def execute(self,state):
        context={**state.get("variables",{}),"input":state.get("input"),"node_outputs":state.get("node_outputs",{})}
        matches=[b["id"] for b in self.config.get("branches",[]) if ExpressionEvaluator().evaluate(b["expression"],context)]
        return {"output":matches,"branches":matches}
