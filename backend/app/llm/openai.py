from langchain_openai import ChatOpenAI


def create_openai(config, api_key=None, base_url=None):
    return ChatOpenAI(
        model=config["model"],
        temperature=config.get("temperature", 0.7),
        api_key=api_key,
        base_url=base_url,
        streaming=True,
    )
