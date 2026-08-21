from app.nodes.condition import ExpressionEvaluator
def test_condition(): assert ExpressionEvaluator().evaluate('x > 1',{'x':2})
