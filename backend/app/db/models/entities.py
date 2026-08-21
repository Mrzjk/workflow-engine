import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
def uid() -> str: return str(uuid.uuid4())
class Timestamped(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
class User(Timestamped):
    __tablename__="users"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); email: Mapped[str]=mapped_column(String(255),unique=True); password_hash: Mapped[str]=mapped_column(String(255)); role: Mapped[str]=mapped_column(String(32),default="user")
class Workflow(Timestamped):
    __tablename__="workflows"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); owner_id: Mapped[str|None]=mapped_column(ForeignKey("users.id")); name: Mapped[str]=mapped_column(String(255)); description: Mapped[str|None]=mapped_column(Text); visibility: Mapped[str]=mapped_column(String(32),default="private"); review_status: Mapped[str]=mapped_column(String(32),default="draft")
class WorkflowVersion(Base):
    __tablename__="workflow_versions"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); workflow_id: Mapped[str]=mapped_column(ForeignKey("workflows.id")); version: Mapped[int]=mapped_column(Integer); status: Mapped[str]=mapped_column(String(32),default="draft"); graph_json: Mapped[dict]=mapped_column(JSON); created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Tool(Timestamped):
    __tablename__="tools"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); name: Mapped[str]=mapped_column(String(255),unique=True); description: Mapped[str|None]=mapped_column(Text); config: Mapped[dict]=mapped_column(JSON,default=dict)
class Model(Base):
    __tablename__="models"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); provider: Mapped[str]=mapped_column(String(64)); name: Mapped[str]=mapped_column(String(128)); config: Mapped[dict]=mapped_column(JSON,default=dict)
class WorkflowRun(Base):
    __tablename__="workflow_runs"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); workflow_id: Mapped[str]=mapped_column(String(36)); workflow_version_id: Mapped[str]=mapped_column(String(36)); input: Mapped[str]=mapped_column(Text); output: Mapped[dict|None]=mapped_column(JSON); status: Mapped[str]=mapped_column(String(32),default="queued"); started_at: Mapped[datetime|None]=mapped_column(DateTime); finished_at: Mapped[datetime|None]=mapped_column(DateTime)
class WorkflowTrace(Base):
    __tablename__="workflow_traces"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); workflow_id: Mapped[str]=mapped_column(ForeignKey("workflows.id")); workflow_run_id: Mapped[str]=mapped_column(ForeignKey("workflow_runs.id"),unique=True); status: Mapped[str]=mapped_column(String(32),default="running"); input: Mapped[dict]=mapped_column(JSON); output: Mapped[dict|None]=mapped_column(JSON); error: Mapped[str|None]=mapped_column(Text); started_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); finished_at: Mapped[datetime|None]=mapped_column(DateTime)
class TraceSpan(Base):
    __tablename__="trace_spans"; id: Mapped[str]=mapped_column(String(36),primary_key=True); trace_id: Mapped[str]=mapped_column(ForeignKey("workflow_traces.id")); node_id: Mapped[str]=mapped_column(String(128)); node_type: Mapped[str]=mapped_column(String(64)); input: Mapped[dict]=mapped_column(JSON); output: Mapped[dict|None]=mapped_column(JSON); status: Mapped[str]=mapped_column(String(32)); error: Mapped[str|None]=mapped_column(Text); duration: Mapped[float|None]=mapped_column(Float); started_at: Mapped[datetime]=mapped_column(DateTime); finished_at: Mapped[datetime|None]=mapped_column(DateTime)
class NodeRun(Base):
    __tablename__="node_runs"; id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); run_id: Mapped[str]=mapped_column(ForeignKey("workflow_runs.id")); node_id: Mapped[str]=mapped_column(String(128)); node_type: Mapped[str]=mapped_column(String(64)); input: Mapped[dict|None]=mapped_column(JSON); output: Mapped[dict|None]=mapped_column(JSON); status: Mapped[str]=mapped_column(String(32)); error: Mapped[str|None]=mapped_column(Text); duration: Mapped[float|None]=mapped_column(Float); started_at: Mapped[datetime|None]=mapped_column(DateTime); finished_at: Mapped[datetime|None]=mapped_column(DateTime)
