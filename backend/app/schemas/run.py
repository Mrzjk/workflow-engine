from pydantic import BaseModel
class RunCreate(BaseModel): input: str
class RunEvent(BaseModel): run_id: str; event: str; node_id: str|None=None; node_type: str|None=None; timestamp: str; data: dict = {}
