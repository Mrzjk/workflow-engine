from app.core.config import settings
from .openai import create_openai
from .ollama import create_ollama
class LLMExecutionError(RuntimeError): pass
class LLMFactory:
    @classmethod
    def create(cls, config):
        provider=config.get("provider",settings.default_llm_provider)
        if provider in {"openai","qwen","deepseek","vllm","openai_compatible"}:
            prefixes={"qwen":"qwen","deepseek":"deepseek"}; p=prefixes.get(provider,"openai")
            return create_openai(config, getattr(settings,f"{p}_api_key",settings.openai_api_key),getattr(settings,f"{p}_base_url",settings.openai_base_url))
        if provider=="ollama": return create_ollama(config)
        raise LLMExecutionError(f"unsupported provider: {provider}")
