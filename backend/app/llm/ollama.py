from langchain_ollama import ChatOllama
def create_ollama(config, **_): return ChatOllama(model=config["model"], temperature=config.get("temperature",.7))
