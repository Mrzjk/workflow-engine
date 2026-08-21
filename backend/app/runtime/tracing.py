"""In-memory trace recorder. Persistence belongs to RunService, not nodes."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
import uuid

@dataclass
class SpanRecord:
    id: str; node_id: str; node_type: str; input: dict; status: str = "running"; output: dict | None = None; error: str | None = None; started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc)); finished_at: datetime | None = None; _started: float = field(default_factory=perf_counter)
    @property
    def duration(self) -> float | None: return perf_counter() - self._started if self.finished_at is None else (self.finished_at-self.started_at).total_seconds()

class TraceRecorder:
    def __init__(self): self.spans: list[SpanRecord] = []
    def start(self, node_id: str, node_type: str, input_data: dict) -> SpanRecord:
        span=SpanRecord(id=str(uuid.uuid4()),node_id=node_id,node_type=node_type,input=input_data); self.spans.append(span); return span
    def finish(self, span: SpanRecord, output: dict | None = None, error: Exception | None = None) -> None:
        span.finished_at=datetime.now(timezone.utc); span.output=output; span.error=str(error) if error else None; span.status="failed" if error else "success"
