from app.template import TemplateRenderer
def test_template(): assert TemplateRenderer().render('{{ input }}',{'input':'x'})=='x'
