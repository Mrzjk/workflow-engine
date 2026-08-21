from pydantic import BaseModel
class ToolRead(BaseModel): id: str; name: str; description: str|None=None
