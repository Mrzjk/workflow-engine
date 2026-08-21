from .resolver import TemplateResolver
class TemplateRenderer:
    def render(self, template: str, state: dict) -> str:
        return TemplateResolver.pattern.sub(lambda m: str(TemplateResolver.resolve(m.group(1),state)),template)
