from dataclasses import dataclass, field
@dataclass
class ExecutionContext:
    run_id: str; variables: dict = field(default_factory=dict); event_bus: object|None=None
