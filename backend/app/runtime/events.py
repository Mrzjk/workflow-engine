from dataclasses import dataclass, field
from datetime import datetime, timezone
@dataclass
class RuntimeEvent:
    run_id: str; event: str; node_id: str|None=None; node_type: str|None=None; data: dict=field(default_factory=dict); timestamp: str=field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def as_dict(self): return self.__dict__
